from django.db import models
from django.forms import ValidationError
from lib.image import UploadToDirUUID
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.utils.crypto import get_random_string

from accounting.models import Order
from banquet.models import Banquet, Participant
from recruitment.models import RecruitmentApplication
from fair.models import Fair, FairDay
from people.models import DietaryRestriction
from django.contrib.postgres.fields import JSONField


def get_random_32_length_string():
    return get_random_string(32)


class CatalogueIndustry(models.Model):
    industry = models.CharField(blank=False, max_length=255)
    category = models.ForeignKey(
        "CatalogueCategory", blank=True, null=True, on_delete=models.CASCADE
    )
    include_in_form = models.BooleanField(default=True)
    include_in_form.help_text = (
        "The alternative is only visible in forms if this attribute is checked."
    )

    def __str__(self):
        return self.industry

    class Meta:
        verbose_name_plural = "Catalogue industries"
        default_permissions = []
        ordering = ["category", "industry"]


class CatalogueValue(models.Model):
    value = models.CharField(blank=False, max_length=255)
    include_in_form = models.BooleanField(default=True)
    include_in_form.help_text = (
        "The alternative is only visible in forms if this attribute is checked."
    )

    def __str__(self):
        return self.value

    class Meta:
        default_permissions = []
        ordering = ["value"]


class CatalogueEmployment(models.Model):
    employment = models.CharField(blank=False, max_length=255)
    include_in_form = models.BooleanField(default=True)
    include_in_form.help_text = (
        "The alternative is only visible in forms if this attribute is checked."
    )

    def __str__(self):
        return self.employment

    class Meta:
        default_permissions = []
        ordering = ["employment"]


class CatalogueLocation(models.Model):
    location = models.CharField(blank=False, max_length=255)
    include_in_form = models.BooleanField(default=True)
    include_in_form.help_text = (
        "The alternative is only visible in forms if this attribute is checked."
    )

    def __str__(self):
        return self.location

    class Meta:
        default_permissions = []
        ordering = ["location"]


class CatalogueBenefit(models.Model):
    benefit = models.CharField(blank=False, max_length=255)
    include_in_form = models.BooleanField(default=True)
    include_in_form.help_text = (
        "The alternative is only visible in forms if this attribute is checked."
    )

    def __str__(self):
        return self.benefit

    class Meta:
        default_permissions = []
        ordering = ["benefit"]


class CatalogueCompetence(models.Model):
    competence = models.CharField(blank=False, max_length=255)
    category = models.ForeignKey(
        "CatalogueCategory", blank=True, null=True, on_delete=models.CASCADE
    )
    include_in_form = models.BooleanField(default=True)
    include_in_form.help_text = (
        "The alternative is only visible in forms if this attribute is checked."
    )

    def __str__(self):
        return self.competence

    class Meta:
        default_permissions = []
        ordering = ["category", "competence"]


class CatalogueCategory(models.Model):
    category = models.CharField(blank=False, max_length=255)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name_plural = "Catalogue categories"
        default_permissions = []
        ordering = ["category"]


class Location(models.Model):
    fair = models.ForeignKey(Fair, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "exhibitors.Location", on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(blank=False, null=False, max_length=255)
    background = models.ImageField(
        upload_to=UploadToDirUUID("locations"), null=True, blank=True
    )
    people_count_enabled = models.BooleanField(default=False)
    people_count = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["fair", "parent__name", "name"]
        unique_together = [["fair", "name"]]

    def __str__(self):
        return ((str(self.parent) + " -> ") if self.parent else "") + self.name


# A company (or organisation) participating in a fair
class Exhibitor(models.Model):
    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE)
    fair = models.ForeignKey("fair.Fair", on_delete=models.CASCADE)
    contact_persons = models.ManyToManyField(User, blank=True)
    contact = models.ForeignKey(
        "companies.CompanyContact", null=True, blank=True, on_delete=models.CASCADE
    )
    tier = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        choices=[
            ("1", "Bronze"),
            ("2", "Silver"),
            ("3", "Gold"),
        ],
    )
    application_status = models.CharField(
        blank=False,
        null=False,
        max_length=255,
        default="0",
        choices=[
            ("0", "pending"),
            ("1", "accepted"),
            ("2", "rejected"),
            ("3", "reserve"),
            
        ],
    )
    booth_height = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="Height of the booth (cm)"
    )
    electricity_total_power = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="Estimated power consumption (W)"
    )
    electricity_socket_count = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="Number of sockets"
    )
    electricity_equipment = models.TextField(
        blank=True, null=True, verbose_name="Description of equipment"
    )
    check_in_timestamp = models.DateTimeField(blank=True, null=True)
    check_in_comment = models.TextField(blank=True, null=True)
    check_in_user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name="check_in_user",
        on_delete=models.SET_NULL,
    )
    catalogue_about = models.TextField(blank=True, null=True, max_length=600)
    catalogue_purpose = models.TextField(blank=True, null=True, max_length=600)
    catalogue_logo_squared = models.ImageField(
        upload_to=UploadToDirUUID("exhibitors", "catalogue_logo_squared"), blank=True
    )
    catalogue_logo_freesize = models.ImageField(
        upload_to=UploadToDirUUID("exhibitors", "catalogue_logo_freesize"), blank=True
    )
    catalogue_contact_name = models.CharField(
        blank=True, null=True, max_length=255, verbose_name="Contact person's name"
    )
    catalogue_contact_email_address = models.EmailField(
        blank=True,
        null=True,
        max_length=255,
        verbose_name="Contact person's e-mail address",
    )
    catalogue_contact_phone_number = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        verbose_name="Contact person's phone number",
    )
    catalogue_industries = models.ManyToManyField(CatalogueIndustry, blank=True)
    catalogue_values = models.ManyToManyField(CatalogueValue, blank=True)
    catalogue_employments = models.ManyToManyField(CatalogueEmployment, blank=True)
    catalogue_benefits = models.ManyToManyField(CatalogueBenefit, blank=True)
    catalogue_competences = models.ManyToManyField(CatalogueCompetence, blank=True)
    catalogue_locations = models.ManyToManyField(CatalogueLocation, blank=True)
    catalogue_cities = models.TextField(blank=True, null=True, max_length=400)
    catalogue_average_age = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="Average age of employees"
    )
    catalogue_founded = models.PositiveIntegerField(blank=True, null=True)
    fair_location = models.ForeignKey(
        Location, blank=True, null=True, on_delete=models.SET_NULL
    )
    map_coordinates = JSONField(blank=True, null=True)
    vyer_position = models.CharField(blank=True, null=True, max_length=255)
    flyer = models.FileField(
        upload_to="exhibitors/flyers/%Y%m%d/", default=None, blank=True, null=True
    )

    deadline_complete_registration = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Deviating deadline for complete registration",
    )

    placement_wishes = [
        (None, "No preference"),
        ("MIXED", "Mixed with companies from other industries"),
        ("SIMILAR", "Next to similar companies"),
    ]

    placement_wish = models.CharField(
        choices=placement_wishes, blank=True, null=True, max_length=255
    )
    placement_comment = models.TextField(
        blank=True,
        null=True,
        verbose_name="Additional wishes regarding placement at the fair",
    )

    transport_information_read = models.BooleanField(
        null=False,
        default=False,
    )

    transport_to_statuses = [
        ("NOT_BOOKED", "Not booked"),
        ("BOOKED", "Booked"),
        ("ARKAD", "Transported by Arkad"),
        ("NOT_APPLICABLE", "Not applicable"),
        ("EXCEPTION", "Exception"),
        ("IN_CONTACT", "In contact"),
        ("IN_CONTACT_ARMADA", "In contact by Armada"),
        ("STURE", "Sture"),
        ("BY_HAND", "Carried by hand"),
    ]

    transport_to = models.CharField(
        choices=transport_to_statuses,
        null=False,
        blank=False,
        default="NOT_BOOKED",
        max_length=30,
    )

    transport_from_statuses = [
        ("NOT_BOOKED", "Not booked"),
        ("BOOKED", "Booked"),
        ("NOT_APPLICABLE", "Not applicable"),
        ("EXCEPTION", "Exception"),
        ("IN_CONTACT", "In contact"),
        ("STURE", "Sture"),
        ("BY_HAND", "Carried by hand"),
    ]

    transport_from = models.CharField(
        choices=transport_from_statuses,
        null=False,
        blank=False,
        default="NOT_BOOKED",
        max_length=30,
    )
    transport_comment = models.TextField(blank=True, null=True)

    @property
    def count_lunch_tickets(self):
        count_ordered = 0

        for order in Order.objects.filter(
            purchasing_company=self.company, product=self.fair.product_lunch_ticket
        ):
            count_ordered += order.quantity

        count_created = LunchTicket.objects.filter(company=self.company).count()

        return {"ordered": count_ordered, "created": count_created}

    @property
    def count_banquet_tickets(self):
        count_ordered = 0
        count_created = 0

        for banquet in Banquet.objects.filter(fair=self.fair):
            if banquet.product is not None:
                for order in Order.objects.filter(
                    purchasing_company=self.company, product=banquet.product
                ):
                    count_ordered += order.quantity

            count_created += Participant.objects.filter(
                banquet=banquet, company=self.company
            ).count()

        return {"ordered": count_ordered, "created": count_created}

    @property
    def fair_location_special(self):
        for locationSpecial in FairLocationSpecial.objects.filter(fair=self.fair):
            allExhibitors = locationSpecial.exhibitors.all()
            for exh in allExhibitors:
                if exh == self:
                    return locationSpecial
        return None

    @property
    def climate_compensation(self):
        for order in Order.objects.filter(
            purchasing_company=self.company, product__name="Climate compensation"
        ):
            return True
        return False

    def __str__(self):
        return "%s at %s" % (self.company.name, self.fair.name)

    class Meta:
        default_permissions = []
        ordering = ["company__name"]
        permissions = [
            ("base", "View the Exhibitors tab"),
            ("view_all", "Always view all exhibitors"),
            ("create", "Create new exhibitors"),
            ("modify_contact_persons", "Modify contact persons"),
            ("modify_transport", "Modify transport details"),
            ("modify_check_in", "Modify check in"),
            ("modify_details", "Modify details"),
            ("modify_booths", "Modify booths"),
            ("people_count", "Count people in locations"),
            ("modify_coordinates", "Modify coordinates"),
            ("modify_fair_location", "Modify Fair Location"),
            ("modify_application_status", "Modify Application Status"),
        ]


class FairLocationSpecial(models.Model):
    name = models.CharField(blank=True, null=True, max_length=255)
    fair = models.ForeignKey("fair.Fair", on_delete=models.CASCADE)
    exhibitors = models.ManyToManyField(Exhibitor, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Special location"
        default_permissions = []


class ExhibitorView(models.Model):
    """
    A special model that houses information which fields a certain user wants to see in /fairs/%YEAR/exhibitors view
    """

    selectable_fields = {
        "contact_persons": "Contact persons",
        "transport_to": "Transport to the fair",
        "transport_from": "Transport from the fair",
        "transport_comment": "Transport comment",
        "placement_wish": "Placement wish",
        "placement_comment": "Placement comment",
        "electricity_total_power": "Total power (W)",
        "electricity_socket_count": "Socket count",
        "electricity_equipment": "Electricity equipment",
        "booth_height": "Booth height (cm)",
        "count_lunch_tickets": "Lunch tickets",
        "count_banquet_tickets": "Banquet tickets",
        "check_in_timestamp": "Check in",
        "check_in_comment": "Check in comment",
        "booths": "Booths",
        "fair_location": "Fair location",
        "fair_location_special": "Special Location",
        "coordinates": "Coordinates",
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choices = models.TextField()

    def create(self):
        self.choices = "contact_persons transport_from transport_to count_lunch_tickets count_banquet_tickets"
        self.save()

        return self

    class Meta:
        default_permissions = []


class LocationTick(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    change = models.IntegerField()
    new_people_count = models.IntegerField()


class Booth(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(blank=False, null=False, max_length=255)
    boundaries = models.PolygonField(blank=True, null=True)

    class Meta:
        ordering = ["location", "name"]
        unique_together = [["location", "name"]]

    def __str__(self):
        return str(self.location) + " -> " + self.name


class ExhibitorInBooth(models.Model):
    exhibitor = models.ForeignKey(Exhibitor, on_delete=models.CASCADE)
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE)
    days = models.ManyToManyField(FairDay)
    comment = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ["exhibitor", "booth"]
        unique_together = [["exhibitor", "booth"]]

    def __str__(self):
        return str(self.exhibitor) + " in " + str(self.booth)
