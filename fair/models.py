from enum import Enum
from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.utils.crypto import get_random_string
from django.utils import timezone

from lib.image import UploadToDirUUID
from people.models import DietaryRestriction


def get_common_name(self):
    return (
        "%s %s" % (self.first_name, self.last_name)
        if self.first_name and self.last_name
        else self.username
    )


User.add_to_class("__str__", get_common_name)


def current_fair():
    try:
        return Fair.objects.get(current=True).id
    except Exception:
        return None


def default_name():
    return "Armada %d" % (date.today().year)


def get_random_32_length_string():
    return get_random_string(32)


class RegistrationPeriod(Enum):
    BEFORE_IR = 1
    IR = 2
    BETWEEN_IR_AND_CR = 3
    CR = 4
    AFTER_CR = 5
    FAIR = 6
    AFTER_FAIR = 7

    def __str__(self):
        if self == RegistrationPeriod.BEFORE_IR:
            return "before_initial_registration"
        elif self == RegistrationPeriod.IR:
            return "initial_registration"
        elif self == RegistrationPeriod.BETWEEN_IR_AND_CR:
            return "between_ir_and_cr"
        elif self == RegistrationPeriod.CR:
            return "complete_registration"
        elif self == RegistrationPeriod.AFTER_CR:
            return "after_complete_registration"
        elif self == RegistrationPeriod.FAIR:
            return "fair"
        elif self == RegistrationPeriod.AFTER_FAIR:
            return "after_fair"
        else:
            return self.name


class Fair(models.Model):
    name = models.CharField(max_length=100, default=default_name)
    year = models.IntegerField(default=date.today().year)
    description = models.TextField(max_length=500, default=default_name)

    registration_start_date = models.DateTimeField(null=False, blank=False)
    registration_end_date = models.DateTimeField(null=False, blank=False)
    registration_acceptance_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="The date when the companies will be able to see if they have been accepted or not.",
    )
    complete_registration_start_date = models.DateTimeField(null=False, blank=False)
    complete_registration_close_date = models.DateTimeField(null=False, blank=False)
    events_start_date = models.DateTimeField(
        null=True, help_text="The date when events will start"
    )
    events_end_date = models.DateTimeField(null=True)

    current = models.BooleanField(default=False)

    product_lunch_ticket = models.ForeignKey(
        "accounting.Product", blank=True, null=True, on_delete=models.SET_NULL
    )

    companies_ticket_deadline = models.DateTimeField(null=True, blank=True)
    companies_ticket_deadline.help_text = "After this date the companies will no longer be able to create or edit their lunch or banquet tickets on their registration page."

    def get_period(self):
        time = timezone.now()

        if time < self.registration_start_date:
            return RegistrationPeriod.BEFORE_IR
        elif time >= self.registration_start_date and time < self.registration_end_date:
            return RegistrationPeriod.IR
        elif (
            time >= self.registration_end_date
            and time < self.registration_acceptance_date
        ):
            return RegistrationPeriod.BETWEEN_IR_AND_CR
        elif (
            time >= self.registration_acceptance_date
            and time < self.complete_registration_start_date
        ):
            return RegistrationPeriod.BETWEEN_IR_AND_CR
        elif (
            time >= self.complete_registration_start_date
            and time < self.complete_registration_close_date
        ):
            return RegistrationPeriod.CR
        elif (
            time >= self.complete_registration_close_date
            and time < self.events_start_date
        ):
            return RegistrationPeriod.AFTER_CR
        elif time >= self.events_start_date and time < self.events_end_date:
            return RegistrationPeriod.FAIR
        elif time >= self.events_end_date:
            return RegistrationPeriod.AFTER_FAIR

    def is_member_of_fair(self, user):
        if user.is_superuser:
            return True

        for recruitment_period in self.recruitmentperiod_set.all():
            if recruitment_period.recruitmentapplication_set.filter(
                user=user, status="accepted"
            ).exists():
                return True

        return False

    def save(self, *args, **kwargs):
        if self.current:
            for fair in Fair.objects.filter(current=True):
                fair.current = False
                fair.save()
            self.current = True
        super(Fair, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class FairDay(models.Model):
    fair = models.ForeignKey(Fair, on_delete=models.CASCADE)
    date = models.DateField(blank=False, null=False, max_length=255)

    class Meta:
        default_permissions = []
        ordering = ["-fair", "date"]

    def __str__(self):
        return str(self.date)


class OrganizationGroup(models.Model):
    fair = models.ForeignKey(Fair, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return "[%s] - %s" % (self.fair, self.name)

    class Meta:
        ordering = ["-fair", "name"]


class Partner(models.Model):
    name = models.CharField(max_length=50)
    fair = models.ForeignKey(Fair, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to=UploadToDirUUID("partners", "logo"))
    url = models.CharField(max_length=300)
    main_partner = models.BooleanField()

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class LunchTicketTime(models.Model):
    day = models.ForeignKey(FairDay, on_delete=models.CASCADE)
    name = models.CharField(blank=False, null=False, max_length=255)

    class Meta:
        default_permissions = []
        ordering = ["day", "name"]

    def __str__(self):
        return str(self.day) + " " + self.name


class LunchTicket(models.Model):
    fair = models.ForeignKey(Fair, on_delete=models.CASCADE)
    token = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        default=get_random_32_length_string,
        unique=True,
    )
    used = models.BooleanField(default=False, blank=False, null=False)
    email_address = models.EmailField(
        blank=True, null=True, max_length=255, verbose_name="E-mail address"
    )
    comment = models.CharField(blank=True, null=True, max_length=255)
    company = models.ForeignKey(
        "companies.Company", on_delete=models.CASCADE, blank=True, null=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    day = models.ForeignKey(FairDay, on_delete=models.CASCADE)
    time = models.ForeignKey(
        LunchTicketTime, on_delete=models.SET_NULL, blank=True, null=True
    )
    dietary_restrictions = models.ManyToManyField(DietaryRestriction, blank=True)
    other_dietary_restrictions = models.CharField(max_length=75, blank=True, null=True)
    sent = models.BooleanField(blank=False, null=False, default=False)

    def get_ticket_type(self):
        return "student" if self.user else "company"

    def __str__(self) -> str:
        return f"{str(self.company)} - {str(self.day)}"

    class Meta:
        permissions = [("lunchtickets", "Manage lunch tickets")]
        default_permissions = []
        ordering = ["-fair", "pk"]


class LunchTicketScan(models.Model):
    lunch_ticket = models.ForeignKey(LunchTicket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, blank=False, null=False)

    class Meta:
        default_permissions = []


class LunchTicketSend(models.Model):
    lunch_ticket = models.ForeignKey(LunchTicket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    email_address = models.EmailField(max_length=255, verbose_name="E-mail address")

    class Meta:
        default_permissions = []
