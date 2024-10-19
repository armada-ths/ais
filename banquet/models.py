import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.crypto import get_random_string

from accounting.models import Product
from companies.models import Company
from fair.models import Fair
from lib.image import UploadToDirUUID
from people.models import DietaryRestriction


def get_random_32_length_string():
    return get_random_string(32)


class Banquet(models.Model):
    fair = models.ForeignKey(Fair, on_delete=models.CASCADE)
    name = models.CharField(max_length=75, blank=False, null=False)
    date = models.DateTimeField()
    afterparty_date = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=75, blank=True, null=True)
    dress_code = models.CharField(max_length=255, blank=True, null=True)
    caption_phone_number = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Caption for the phone number field",
    )
    caption_dietary_restrictions = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Caption for dietary restrictions",
    )
    product = models.ForeignKey(
        Product,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Product to link the banquet with",
    )
    background = models.ImageField(
        upload_to=UploadToDirUUID("banquets", "map"), blank=True, null=True
    )
    point_size = models.DecimalField(
        blank=True, null=True, max_digits=11, decimal_places=10
    )
    afterparty_price = models.PositiveIntegerField(
        default=0, verbose_name="After Party Price (SEK)"
    )  # can be zero
    afterparty_price_discount = models.PositiveIntegerField(
        default=0, verbose_name="After Party Discounted Price (SEK)"
    )  # can be zero

    def __str__(self):
        return self.name


class Table(models.Model):
    banquet = models.ForeignKey(Banquet, on_delete=models.CASCADE)
    name = models.CharField(max_length=75, blank=False, null=False)

    class Meta:
        unique_together = [["banquet", "name"]]
        ordering = ["banquet", "name"]

    def __str__(self):
        return str(self.banquet) + " - " + self.name


class Seat(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    name = models.CharField(max_length=75, blank=False, null=False)
    top = models.IntegerField(blank=True, null=True)
    left = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = [["table", "name"]]
        ordering = ["table", "name"]

    def __str__(self):
        return self.table.name + " " + self.name


class MatchingProgram(models.Model):
    program = models.CharField(blank=False, max_length=255)
    include_in_form = models.BooleanField(blank=True)
    include_in_form.help_text = (
        "The alternative is only visible in forms if this attribute is checked."
    )

    def __str__(self):
        return self.program

    class Meta:
        default_permissions = []
        ordering = ["program"]


class MatchingInterest(models.Model):
    interest = models.CharField(blank=False, max_length=255)
    include_in_form = models.BooleanField(blank=True)
    include_in_form.help_text = (
        "The alternative is only visible in forms if this attribute is checked."
    )

    def __str__(self):
        return self.interest

    class Meta:
        default_permissions = []
        ordering = ["interest"]


class MatchingYear(models.Model):
    year = models.CharField(blank=False, max_length=255)
    include_in_form = models.BooleanField(blank=True)
    include_in_form.help_text = (
        "The alternative is only visible in forms if this attribute is checked."
    )

    def __str__(self):
        return self.year

    class Meta:
        default_permissions = []
        ordering = ["year"]


class DietaryPreference(models.Model):
    name = models.CharField(max_length=255)
    order = models.IntegerField(default=0)
    banquet = models.ForeignKey(Banquet, on_delete=models.CASCADE)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Participant(models.Model):
    token = models.CharField(
        max_length=32, unique=True, default=get_random_32_length_string
    )
    banquet = models.ForeignKey(Banquet, on_delete=models.CASCADE)
    company = models.ForeignKey(
        Company, blank=True, null=True, on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=75, blank=True, null=True
    )  # None if a user is provided, required for others
    email_address = models.EmailField(
        max_length=75, blank=True, null=True, verbose_name="E-mail address"
    )  # None if a user is provided, required for others
    phone_number = models.CharField(
        max_length=75, blank=True, null=True
    )  # None if a user is provided, required for others
    dietary_restrictions = models.ManyToManyField(DietaryRestriction, blank=True)
    dietary_preference = models.ForeignKey(
        DietaryPreference, null=True, on_delete=models.CASCADE
    )
    other_dietary_restrictions = models.CharField(max_length=75, blank=True, null=True)
    alcohol = models.BooleanField(choices=[(True, "Yes"), (False, "No")], default=True)
    seat = models.OneToOneField(Seat, blank=True, null=True, on_delete=models.CASCADE)
    charge_stripe = models.CharField(
        max_length=255, blank=True, null=True
    )  # set if the participant has paid for their participation
    ticket_scanned = models.BooleanField(default=False, blank=False, null=False)
    giveaway = models.BooleanField(
        choices=[(True, "Yes"), (False, "No")], default=False, blank=False, null=False
    )  # Indicates that the company may give their ticket away to a student
    has_paid = models.BooleanField(default=False, blank=False, null=False)

    def __str__(self):
        return (
            (self.name + " (" + self.company.name + ")")
            if self.company
            else (self.name if self.name else str(self.user))
        )


class TableMatching(models.Model):
    # Previous year of tablematching
    """
    catalogue_industries = models.ManyToManyField('exhibitors.CatalogueIndustry', blank = True)
    catalogue_competences = models.ManyToManyField('exhibitors.CatalogueCompetence', blank = True)
    catalogue_values = models.ManyToManyField('exhibitors.CatalogueValue', blank = True)
    catalogue_employments = models.ManyToManyField('exhibitors.CatalogueEmployment', blank = True)
    catalogue_locations = models.ManyToManyField('exhibitors.CatalogueLocation', blank = True)
    """
    matching_interests = models.ManyToManyField(MatchingInterest, blank=True)
    matching_program = models.ForeignKey(
        MatchingProgram, blank=True, null=True, on_delete=models.SET_NULL
    )
    matching_year = models.ForeignKey(
        MatchingYear, null=True, on_delete=models.SET_NULL
    )
    participant = models.ForeignKey(
        Participant, blank=True, null=True, on_delete=models.CASCADE
    )  # filled in when the participant has been created from this invitation

    def __str__(self):
        name = str(self.participant)
        return name


class InvitationGroup(models.Model):
    banquet = models.ForeignKey(Banquet, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Invitation(models.Model):
    banquet = models.ForeignKey(Banquet, on_delete=models.CASCADE)
    group = models.ForeignKey(InvitationGroup, on_delete=models.CASCADE)
    token = models.CharField(
        max_length=255, null=False, blank=False, default=uuid.uuid4, unique=True
    )
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="banquet_invitation_user",
    )
    participant = models.ForeignKey(
        Participant, blank=True, null=True, on_delete=models.CASCADE
    )  # filled in when the participant has been created from this invitation
    name = models.CharField(max_length=75, blank=True, null=True)
    email_address = models.CharField(max_length=75, blank=True, null=True)
    reason = models.CharField(max_length=75, blank=True, null=True)
    price = models.PositiveIntegerField(verbose_name="Price (SEK)")  # can be zero
    denied = models.BooleanField(default=False)
    deadline = models.DateField(null=True, blank=True)
    part_of_matching = models.BooleanField(
        default=False, choices=[(True, "Yes"), (False, "No")]
    )  # Indicates that this person is to fill in information for the matching functionality
    has_sent_mail = models.BooleanField(default=False)

    @property
    def deadline_smart(self):
        return self.deadline if self.deadline is not None else self.group.deadline

    @property
    def status(self):
        if self.participant is not None:
            if (self.price > 0) and (not self.participant.has_paid):
                return "HAS_NOT_PAID"
            else:
                return "GOING"
        elif self.denied:
            return "NOT_GOING"
        else:
            return "PENDING"

    @classmethod
    def create(cls, banquet, participant, name, email_address, reason, price, user):
        return cls(
            banquet=banquet,
            participant=participant,
            name=name,
            email_address=email_address,
            reason=reason,
            price=price,
            user=user,
        )

    def __str__(self):
        return self.name if self.name is not None else str(self.user)


class AfterPartyInvitation(models.Model):
    banquet = models.ForeignKey(Banquet, on_delete=models.CASCADE)
    inviter = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=75, verbose_name="Full name")
    email_address = models.EmailField(max_length=75, verbose_name="E-mail address")
    used = models.BooleanField(default=False)

    class Meta:
        unique_together = [
            "banquet",
            "email_address",
        ]  # One person can only have one invite to each banquet

    def __str__(self):
        return str(self.name)


class AfterPartyTicket(models.Model):
    banquet = models.ForeignKey(
        Banquet, on_delete=models.CASCADE, null=True, blank=True
    )
    token = models.CharField(
        max_length=255, null=False, blank=False, default=uuid.uuid4, unique=True
    )
    name = models.CharField(max_length=75, blank=False, null=False)
    email_address = models.EmailField(
        max_length=75, blank=False, null=False, verbose_name="E-mail address"
    )
    charge_stripe = models.CharField(max_length=255, blank=True, null=True)
    paid_timestamp = models.DateTimeField(null=True, blank=True)
    paid_price = models.PositiveIntegerField(null=True, blank=True)
    has_paid = models.BooleanField(default=False, blank=False, null=False)
    email_sent = models.BooleanField(default=False, blank=False, null=False)
    inviter = models.CharField(
        max_length=75, null=True, blank=True, verbose_name="Full name of the inviter"
    )

    def __str__(self):
        return (
            str(self.name) + " <" + str(self.email_address) + "> -- " + str(self.token)
        )
