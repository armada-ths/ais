from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string

from accounting.models import Product
from fair.models import Fair
from lib.image import UploadToDirUUID
from people.models import Profile


class Event(models.Model):
    fair = models.ForeignKey(Fair, on_delete=models.CASCADE)
    name = models.CharField(max_length=75, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    registration_end_date = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=75, blank=True, null=True)
    food = models.CharField(max_length=75, blank=True, null=True)
    signup_cr = models.BooleanField(
        blank=False, null=False, verbose_name="Let company representatives sign up"
    )
    signup_s = models.BooleanField(
        blank=False, null=False, verbose_name="Let students sign up"
    )
    open_for_signup = models.BooleanField(
        blank=False, null=False, verbose_name="Event is currently open for sign up"
    )
    company_product = models.ForeignKey(
        Product,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Product to link the event with",
    )
    teams_create_cr = models.BooleanField(
        blank=False, null=False, verbose_name="Let company representatives create teams"
    )
    teams_create_s = models.BooleanField(
        blank=False, null=False, verbose_name="Let students create teams"
    )
    teams_participate_cr = models.BooleanField(
        blank=False,
        null=False,
        verbose_name="Let company representatives join or leave teams",
    )
    teams_participate_s = models.BooleanField(
        blank=False, null=False, verbose_name="Let students join or leave teams"
    )
    teams_default_max_capacity = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="Default max number of team members"
    )  # None => no limit

    event_max_capacity = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="Event max capacity"
    )  # None => no limit

    fee_s = models.PositiveIntegerField(
        default=0, blank=False, null=False, verbose_name="Sign-up fee for students"
    )
    published = models.BooleanField(
        blank=False, null=False, verbose_name="The event is published on the website"
    )
    contact_person = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE
    )
    external_event_link = models.CharField(max_length=255, blank=True, null=True)
    picture = models.ImageField(
        upload_to=UploadToDirUUID("events", "pictures"), blank=True, null=True
    )

    def is_full(self):
        if self.event_max_capacity is None:
            return False

        return self.number_of_signups() >= self.event_max_capacity

    def number_of_signups(self):
        return self.participant_set.count()

    class Meta:
        ordering = ["date_start", "name"]

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
    fee = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="Fee to participate"
    )  # None => default student fee (Event.fee_s)
    date = models.DateTimeField(auto_now_add=True)


class Team(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=75, blank=False, null=False)
    max_capacity = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="Max number of team members"
    )  # None => no limit
    allow_join_cr = models.BooleanField(
        default=True,
        blank=False,
        null=False,
        verbose_name="Allow company representatives to join the team",
    )
    allow_join_s = models.BooleanField(
        default=True,
        blank=False,
        null=False,
        verbose_name="Allow students to join the team",
    )

    def is_full(self):
        return self.number_of_members() >= self.max_capacity

    def number_of_members(self):
        return self.teammember_set.count()

    def __str__(self):
        return self.name


def get_random_32_length_string():
    return get_random_string(32)


class Participant(models.Model):
    event = models.ForeignKey(Event, blank=False, null=True, on_delete=models.CASCADE)
    name = models.CharField(
        blank=True, null=True, max_length=255
    )  # None for students, required for company representatives
    email_address = models.CharField(
        blank=True, null=True, max_length=255
    )  # None for students, required for company representatives
    phone_number = models.CharField(
        blank=True, null=True, max_length=255
    )  # None for students, required for company representatives
    user_cr = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE, related_name="user_cr"
    )  # either this one...
    user_s = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE, related_name="user_s"
    )  # ...or this one
    stripe_charge_id = models.CharField(
        max_length=50, blank=True, null=True
    )  # None for company representatives, filled in if the
    # student has payed using Stripe
    fee_payed_s = models.BooleanField(default=False)
    attended = models.NullBooleanField(
        blank=True, null=True, verbose_name="The participant showed up to the event"
    )
    signup_complete = models.BooleanField(
        blank=False,
        null=False,
        default=False,
        verbose_name="The participant has completed signup",
    )
    check_in_token = models.CharField(
        max_length=32, unique=True, default=get_random_32_length_string
    )
    timestamp = models.DateTimeField(blank=True, null=True, auto_now_add=True)

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

    def has_checked_in(self):
        return self.participantcheckin_set.count() > 0

    def team(self):
        return (
            self.teammember_set.first().team
            if self.teammember_set.first() is not None
            else None
        )

    def __str__(self):
        if self.user_s:
            return self.user_s.get_full_name()
        elif self.user_cr:
            return self.user_cr.get_full_name()
        else:
            return self.name


class ParticipantCheckIn(models.Model):
    timestamp = models.DateTimeField(
        null=True,
        auto_now_add=True,
        verbose_name="When the participant checked in at the event",
    )
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)


class TeamMember(models.Model):
    team = models.ForeignKey(Team, blank=False, null=False, on_delete=models.CASCADE)
    participant = models.ForeignKey(
        Participant, blank=False, null=False, on_delete=models.CASCADE
    )
    leader = models.BooleanField(blank=False, null=False, default=False)

    def __str__(self):
        return self.participant.__str__() + self.team.__str__()


class TeamInvitation(models.Model):
    team = models.ForeignKey(Team, blank=False, null=False, on_delete=models.CASCADE)
    invitee = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class SignupQuestion(models.Model):
    QUESTION_TYPES = (
        ("text_field", "Short Text"),
        ("text_area", "Long Text"),
        ("single_choice", "Single Choice"),
        ("multiple_choice", "Multiple Choice"),
        ("student_program", "Student Program"),
        ("file_upload", "File Upload"),
    )

    class Meta:
        ordering = ["pk"]

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    type = models.CharField(
        blank=False, null=False, choices=QUESTION_TYPES, max_length=20
    )
    question = models.TextField(blank=False, null=False)
    required = models.BooleanField(blank=False, null=False)
    options = ArrayField(models.TextField(blank=False, null=False), default=list)


class SignupQuestionAnswerFile(models.Model):
    file = models.FileField(upload_to=UploadToDirUUID("events", "files"))


class SignupQuestionAnswer(models.Model):
    signup_question = models.ForeignKey(
        SignupQuestion, blank=False, null=False, on_delete=models.CASCADE
    )
    participant = models.ForeignKey(
        Participant, blank=False, null=False, on_delete=models.CASCADE
    )
    answer = models.TextField()  # Used for 'text_field' and 'text_area'
    file = models.ForeignKey(
        SignupQuestionAnswerFile,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ["signup_question__pk"]
