from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

from accounting.models import Product
from fair.models import Fair
from people.models import Profile


class Event(models.Model):
    fair = models.ForeignKey(Fair, on_delete=models.CASCADE)
    name = models.CharField(max_length=75, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    location = models.CharField(max_length=75, blank=True, null=True)
    signup_cr = models.BooleanField(blank=False, null=False, verbose_name='Let company representatives sign up')
    signup_s = models.BooleanField(blank=False, null=False, verbose_name='Let students sign up')
    open_for_signup = models.BooleanField(blank=False, null=False, verbose_name='Event is currently open for sign up')
    company_product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE,
                                        verbose_name='Product to link the event with')
    teams_create_cr = models.BooleanField(blank=False, null=False, verbose_name='Let company representatives create teams')
    teams_create_s = models.BooleanField(blank=False, null=False, verbose_name='Let students create teams')
    teams_participate_cr = models.BooleanField(blank=False, null=False, verbose_name='Let company representatives join or leave teams')
    teams_participate_s = models.BooleanField(blank=False, null=False, verbose_name='Let students join or leave teams')
    teams_default_max_capacity = models.PositiveIntegerField(blank=True, null=True,
                                                             verbose_name='Default max number of team members')  # None => no limit
    fee_s = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name='Sign-up fee for students')
    published = models.BooleanField(blank=False, null=False, verbose_name='The event is published on the website')
    requires_invitation = models.BooleanField(blank=False, null=False, verbose_name='Participants need an invitation to sign up')
    contact_person = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    external_event_link = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['date_start', 'name']

    def __str__(self):
        return self.name

    @property
    def is_future(self):
        return timezone.now() < self.date_start

    @property
    def is_past(self):
        return timezone.now() > self.date_end


class Invitation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    invitee = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    fee = models.PositiveIntegerField(blank=True, null=True, verbose_name='Fee to participate')  # None => default student fee (Event.fee_s)
    date = models.DateTimeField(auto_now_add=True)


class Team(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=75, blank=False, null=False)
    max_capacity = models.PositiveIntegerField(blank=True, null=True, verbose_name='Max number of team members')  # None => no limit
    allow_join_cr = models.BooleanField(default=True, blank=False, null=False,
                                        verbose_name='Allow company representatives to join the team')
    allow_join_s = models.BooleanField(default=True, blank=False, null=False, verbose_name='Allow students to join the team')

    def is_full(self):
        return self.number_of_members() >= self.max_capacity

    def number_of_members(self):
        return self.teammember_set.count()

    def __str__(self):
        return self.name


class Participant(models.Model):
    event = models.ForeignKey(Event, blank=False, null=True, on_delete=models.CASCADE)
    name = models.CharField(blank=True, null=True, max_length=255)  # None for students, required for company representatives
    email_address = models.CharField(blank=True, null=True, max_length=255)  # None for students, required for company representatives
    phone_number = models.CharField(blank=True, null=True, max_length=255)  # None for students, required for company representatives
    user_cr = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='user_cr')  # either this one...
    user_s = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='user_s')  # ...or this one
    stripe_charge_id = models.CharField(max_length=50, blank=True, null=True)  # None for company representatives, filled in if the
    # student has payed using Stripe
    fee_payed_s = models.BooleanField(default=False)
    attended = models.NullBooleanField(blank=True, null=True, verbose_name='The participant showed up to the event')
    signup_complete = models.BooleanField(blank=False, null=False, default=False, verbose_name='The participant has completed signup')

    # Name, email and phone number can be stored either in this model or in the user model depending on if this is a student or not,
    # so we define these help functions to get them easier

    def assigned_name(self):
        if self.user_s:
            return self.user_s.get_full_name()
        else:
            return self.name

    def assigned_email(self):
        if self.user_s:
            return self.user_s.email
        else:
            return self.email_address

    def assigned_phone_number(self):
        if self.user_s:
            return Profile.objects.get(user=self.user_s).phone_number
        else:
            return self.phone_number

    def __str__(self):
        if self.user_s:
            return self.user_s.get_full_name()
        elif self.user_cr:
            return self.user_cr.get_full_name()
        else:
            return self.name


class TeamMember(models.Model):
    team = models.ForeignKey(Team, blank=False, null=False, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, blank=False, null=False, on_delete=models.CASCADE)
    leader = models.BooleanField(blank=False, null=False, default=False)

    class Meta:
        unique_together = ('team', 'leader')

    def __str__(self):
        return self.participant.__str__() + self.team.__str__()


class TeamInvitation(models.Model):
    team = models.ForeignKey(Team, blank=False, null=False, on_delete=models.CASCADE)
    invitee = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class SignupQuestion(models.Model):
    QUESTION_TYPES = (
        ('text_field', 'Short Text'),
        ('text_area', 'Long Text'),
        ('single_choice', 'Single Choice'),
        ('multiple_choice', 'Multiple Choice')
    )

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    type = models.CharField(blank=False, null=False, choices=QUESTION_TYPES, max_length=20)
    question = models.TextField(blank=False, null=False)
    required = models.BooleanField(blank=False, null=False)
    options = ArrayField(models.TextField(blank=False, null=False), default=[])


class SignupQuestionAnswer(models.Model):
    signup_question = models.ForeignKey(SignupQuestion, blank=False, null=False, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, blank=False, null=False, on_delete=models.CASCADE)
    answer = models.TextField()  # Used for 'text_field' and 'text_area'
