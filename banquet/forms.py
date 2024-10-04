from django import forms
from django.forms import (
    ModelForm,
    Form,
    ModelMultipleChoiceField,
    ModelChoiceField,
    ChoiceField,
)

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

from django.contrib.auth.models import User
import re
import csv

from people.models import DietaryRestriction

from .models import (
    DietaryPreference,
    Participant,
    InvitationGroup,
    Invitation,
    AfterPartyInvitation,
    AfterPartyTicket,
    TableMatching,
    MatchingProgram,
    MatchingInterest,
    MatchingYear,
)
from exhibitors.models import (
    CatalogueIndustry,
    CatalogueCompetence,
    CatalogueValue,
    CatalogueLocation,
    CatalogueEmployment,
    CatalogueCategory,
)


def fix_phone_number(n):
    if n is None:
        return None

    n = n.replace(" ", "")
    n = n.replace("-", "")

    if n.startswith("00"):
        n = "+" + n[2:]
    if n.startswith("0"):
        n = "+46" + n[1:]

    return n


class ParticipantForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        participant = kwargs.pop("instance", None)
        banquet = participant.banquet

        # Set empty_label to None to remove the default "------"
        self.fields["dietary_preference"].empty_label = None

        if banquet:
            self.fields["dietary_preference"].help_text = (
                "We do not serve meat. Our options are exclusively fish, vegetarian, or vegan dishes."
            )
            self.fields["dietary_preference"].queryset = self.get_dietary_preferences(
                banquet
            )

        self.fields["dietary_restrictions"].queryset = self.get_dietary_restrictions()

    def get_dietary_restrictions(self):
        return DietaryRestriction.objects.filter(show_in_banquet=True)

    def get_dietary_preferences(self, banquet):
        # Custom function to retrieve dietary preferences for the given banquet
        return DietaryPreference.objects.filter(banquet=banquet)

    def clean(self):
        super(ParticipantForm, self).clean()

        if "phone_number" in self.cleaned_data:
            self.cleaned_data["phone_number"] = fix_phone_number(
                self.cleaned_data["phone_number"]
            )

        return self.cleaned_data

    def is_valid(self):
        valid = super(ParticipantForm, self).is_valid()

        if not valid:
            return valid

        phone_number = self.cleaned_data.get("phone_number")

        if phone_number is not None and not re.match(r"\+[0-9]+$", phone_number):
            self.add_error(
                "phone_number", "Must only contain numbers and a leading plus."
            )
            valid = False

        return valid

    class Meta:
        model = Participant
        fields = [
            "name",
            "email_address",
            "phone_number",
            "dietary_preference",
            "dietary_restrictions",
            "other_dietary_restrictions",
            "alcohol",
        ]

        widgets = {
            "name": forms.TextInput(attrs={"readonly": "readonly"}),
            "email_address": forms.TextInput(attrs={"readonly": "readonly"}),
            "dietary_preference": forms.RadioSelect(),
            "dietary_restrictions": forms.CheckboxSelectMultiple(),
            "other_dietary_restrictions": forms.TextInput(),
            "alcohol": forms.RadioSelect(),
        }

        help_texts = {
            "other_dietary_restrictions": "Please leave empty if no other restrictions.",
        }


class ParticipantAdminForm(forms.ModelForm):
    def clean(self):
        super(ParticipantAdminForm, self).clean()

        if "phone_number" in self.cleaned_data:
            self.cleaned_data["phone_number"] = fix_phone_number(
                self.cleaned_data["phone_number"]
            )

        return self.cleaned_data

    def is_valid(self):
        valid = super(ParticipantAdminForm, self).is_valid()

        if not valid:
            return valid

        company = self.cleaned_data.get("company")
        user = self.cleaned_data.get("user")
        name = self.cleaned_data.get("name")
        email_address = self.cleaned_data.get("email_address")
        phone_number = self.cleaned_data.get("phone_number")

        if company is not None and user is not None:
            self.add_error("company", "Cannot have both a company and a user.")
            self.add_error("user", "Cannot have both a company and a user.")
            valid = False

        if phone_number is not None and not re.match(r"\+[0-9]+$", phone_number):
            self.add_error(
                "phone_number", "Must only contain numbers and a leading plus."
            )
            valid = False

        if user is not None and name is not None:
            self.add_error("name", "Must be empty if a user is selected.")
            valid = False

        if user is not None and email_address is not None:
            self.add_error("email_address", "Must be empty if a user is selected.")
            valid = False

        if user is None and name is None:
            self.add_error("name", "Must be given if no user is selected.")
            valid = False

        if user is None and email_address is None:
            self.add_error("email_address", "Must be given if no user is selected.")
            valid = False

        return valid

    class Meta:
        model = Participant
        fields = [
            "seat",
            "company",
            "user",
            "name",
            "email_address",
            "phone_number",
            "dietary_restrictions",
            "other_dietary_restrictions",
            "alcohol",
            "giveaway",
        ]

        help_texts = {
            "name": "Only enter a name if you do not select a user.",
            "email_address": "Only enter an e-mail address if you do not select a user.",
            "giveaway": "Only applies to company tickets, default should be No for all other tickets.",
        }

        labels = {
            "giveaway": "The company plan to give this ticket to a student",
        }

        widgets = {
            "dietary_restrictions": forms.CheckboxSelectMultiple(),
            "other_dietary_restrictions": forms.TextInput(),
            "alcohol": forms.RadioSelect(),
            "giveaway": forms.RadioSelect(),
        }


class ImportInvitationsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.banquet = kwargs.pop("banquet")
        super().__init__(*args, **kwargs)

    excel_text = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 10, "cols": 100}),
        label="Paste Excel data here",
    )
    send_email = forms.BooleanField(
        label="Send invitation emails",
        required=False,
        initial=False,
        help_text="Send an invitation email to the invitees.",
    )
    group = forms.ModelChoiceField(
        queryset=InvitationGroup.objects.all(),
        label="Select a group to add these invitations to",
        required=False,
    )

    def clean_excel_text(self):
        rows = [row.rstrip() for row in self.cleaned_data.get("excel_text").split("\n")]
        rows = [row for row in rows if len(row) > 0]
        reader = csv.DictReader(rows, delimiter="\t")

        required_field_headers = ["price", "name", "email"]
        required_not_found = []
        for field in required_field_headers:
            if field not in reader.fieldnames:
                required_not_found.append(field)

        if len(required_not_found) > 0:
            raise forms.ValidationError(
                "The following required fields were not found in the data: {}".format(
                    ", ".join(required_not_found)
                )
            )

        validator = EmailValidator()
        rows = [row for row in reader]

        for row in rows:
            if row["email"] == None:
                row["invalid_email"] = True
                row["email"] = ""
            else:
                try:
                    validator(row["email"])
                except ValidationError:
                    row["invalid_email"] = True

            if row["name"] == None or len(row["name"]) == 0:
                row["invalid_name"] = True
                row["name"] = ""

            if row["price"] == None or row["price"] == "":
                row["price"] = 0
            elif not row["price"].isdigit():
                row["invalid_price"] = True

            duplicate = Invitation.objects.filter(
                email_address=row["email"], banquet=self.banquet
            ).first()
            if duplicate != None:
                row["duplicate"] = duplicate

        return rows


class InvitationForm(forms.ModelForm):
    send_email = forms.BooleanField(
        label="Send invitation email",
        required=False,
        initial=False,
        help_text="Send an invitation email to the invitee.",
    )

    def clean(self):
        super(InvitationForm, self).clean()

        if "phone_number" in self.cleaned_data:
            self.cleaned_data["phone_number"] = fix_phone_number(
                self.cleaned_data["phone_number"]
            )

        return self.cleaned_data

    def is_valid(self):
        valid = super(InvitationForm, self).is_valid()

        if not valid:
            return valid

        user = self.cleaned_data.get("user")
        name = self.cleaned_data.get("name")
        email_address = self.cleaned_data.get("email_address")

        if user is not None:
            if name is not None:
                self.add_error("name", "Leave this empty if you select a user.")
                valid = False

            if email_address is not None:
                self.add_error(
                    "email_address", "Leave this empty if you select a user."
                )
                valid = False

        else:
            if name is None or len(name) == 0:
                self.add_error("name", "Either select a user or provide a name.")
                valid = False

            if email_address is None or len(email_address) == 0:
                self.add_error(
                    "email_address",
                    "Either select a user or provide an e-mail address.",
                )
                valid = False

        return valid

    def save(self, *args, **kwargs):
        invitation = super(InvitationForm, self).save(*args, **kwargs)

        if invitation.participant is not None:
            if invitation.user is None:
                invitation.participant.name = invitation.name
                invitation.participant.email_address = invitation.email_address

            else:
                invitation.participant.name = None
                invitation.participant.email_address = None

            invitation.participant.save()

        return invitation

    class Meta:
        model = Invitation
        fields = [
            "group",
            "user",
            "name",
            "email_address",
            "reason",
            "deadline",
            "price",
            "part_of_matching",
        ]

        help_texts = {
            "reason": "Not shown to the invitee.",
            "deadline": "Leave blank to get the group's default deadline.",
            "price": "Enter an integer price in SEK.",
            "part_of_matching": "This person is subject to the banquet placement matching functionality.",
        }

        widgets = {"deadline": forms.DateInput(attrs={"type": "date"})}


class InvitationSearchForm(forms.Form):
    status_choices = [
        ("GOING", "Going"),
        ("HAS_NOT_PAID", "Has not paid"),
        ("NOT_GOING", "Not going"),
        ("PENDING", "Pending"),
    ]

    matching_status_choices = [
        (None, "Any"),
        (True, "Part of matching"),
        (False, "Not part of matching"),
    ]

    statuses = forms.MultipleChoiceField(
        choices=status_choices, widget=forms.CheckboxSelectMultiple(), required=False
    )
    groups = forms.ModelMultipleChoiceField(
        queryset=InvitationGroup.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
        label="Show only invitations belonging to any of these groups",
        required=False,
    )
    matching_statuses = forms.ChoiceField(
        choices=matching_status_choices,
        widget=forms.RadioSelect(),
        label="Show only invitations that are / are not subject to the matching functionality",
        required=False,
    )


class AfterPartyInvitationForm(forms.ModelForm):
    class Meta:
        model = AfterPartyInvitation
        fields = ["name", "email_address"]

        labels = {
            "name": "Friend's full name",
            "email_address": "Friend's email address",
        }


class AfterPartyTicketForm(forms.ModelForm):
    class Meta:
        model = AfterPartyTicket
        fields = ["name", "email_address", "inviter"]

        labels = {
            "name": "Your full name",
            "inviter": "Did someone in Armada recommend you about this after party? Write first name and last name.",
        }


class InternalParticipantForm(forms.ModelForm):
    """
    Form for internal users to register for the banquet
    certain fields are disabled as they are prefilled in view
    """

    class Meta:
        model = Participant
        # Is still something we send back in view but handled without user input
        exclude = ["banquet", "company", "user"]

        widgets = {
            "name": forms.TextInput(attrs={"readonly": "readonly"}),
            "email_address": forms.TextInput(attrs={"readonly": "readonly"}),
            "phone_number": forms.TextInput(attrs={"readonly": "readonly"}),
            "dietary_restrictions": forms.CheckboxSelectMultiple(),
            "other_dietary_restrictions": forms.TextInput(),
            "alcohol": forms.RadioSelect(),
        }

        help_texts = {
            "other_dietary_restrictions": "Please leave empty if no other restrictions.",
        }


class ParticipantTableMatchingForm(ModelForm):
    # custom defined field subclass to overwrite string representation
    class IncludeCategoryChoiceFieldMultiple(ModelMultipleChoiceField):
        def label_from_instance(self, choice):
            return str(choice)

    class IncludeCategoryChoiceFieldSingle(ModelChoiceField):
        def label_from_instance(self, choice):
            return str(choice)

    matching_program = IncludeCategoryChoiceFieldSingle(
        queryset=MatchingProgram.objects.filter(include_in_form=True),
        widget=forms.RadioSelect,
        label="What are you studying?",
        empty_label="I don't want to participate in matching",
        required=False,
    )

    matching_interests = IncludeCategoryChoiceFieldMultiple(
        queryset=MatchingInterest.objects.filter(include_in_form=True),
        widget=forms.CheckboxSelectMultiple,
        label="What are your interests? (Yes, all of them :) )",
        required=False,
    )

    matching_year = IncludeCategoryChoiceFieldSingle(
        queryset=MatchingYear.objects.filter(include_in_form=True),
        widget=forms.RadioSelect,
        label="What year will you graduate?",
        empty_label="I don't want to participate in matching",
        required=False,
    )

    class Meta:
        model = TableMatching
        fields = ["matching_program", "matching_interests", "matching_year"]


# Previous implementation of the MatchingForm
""" class ParticipantTableMatchingForm(ModelForm):
	# custom defined field subclass to overwrite string representation
	class IncludeCategoryChoiceField(ModelMultipleChoiceField):
		def label_from_instance(self, choice):
			if choice.category:
				return str(choice.category) + ' - ' + str(choice)
			else:
				return str(choice)
    matching = 2


    catalogue_industries = IncludeCategoryChoiceField(
		queryset = CatalogueIndustry.objects.filter(include_in_form = True),
		widget = forms.CheckboxSelectMultiple,
		label = 'Which industries would you like to work in?',
		required = False)
	catalogue_competences = IncludeCategoryChoiceField(
		queryset = CatalogueCompetence.objects.filter(include_in_form = True),
		widget = forms.CheckboxSelectMultiple,
		label = 'What competences do you have?',
		required = False)
	catalogue_values = forms.ModelMultipleChoiceField(
		queryset = CatalogueValue.objects.filter(include_in_form = True),
		widget = forms.CheckboxSelectMultiple,
		label = 'Select up to three values that you are interested in.',
		required = False)
	catalogue_employments = forms.ModelMultipleChoiceField(
		queryset = CatalogueEmployment.objects.filter(include_in_form = True),
		widget = forms.CheckboxSelectMultiple,
		label = 'What kind of employments are you looking for?',
		required = False)
	catalogue_locations = forms.ModelMultipleChoiceField(
		queryset = CatalogueLocation.objects.filter(include_in_form = True),
		widget = forms.CheckboxSelectMultiple,
		label = 'Where would you like to work?',
		required = False)"""


class ExternalParticipantForm(forms.ModelForm):
    """
    External participant fills in personal info (invitation page)
    """

    class Meta:
        model = Participant
        exclude = ["banquet", "company", "user", "seat"]
        widgets = {
            "name": forms.TextInput(attrs={"readonly": "readonly"}),
            "email_address": forms.TextInput(attrs={"readonly": "readonly"}),
            "dietary_restrictions": forms.CheckboxSelectMultiple(),
            "dietary_restictions_other": forms.TextInput(),
            "alcohol": forms.RadioSelect(),
        }


class SendInvitationForm(forms.ModelForm):
    """
    Banquet administrator sends out invite
    """

    def __init__(self, *args, **kwargs):
        # would like to do as in conact list however I can't get user object in that case
        # but this works also although not pretty
        super(SendInvitationForm, self).__init__(*args, **kwargs)
        self.fields["user"].queryset = User.objects.exclude(
            groups__isnull=True
        ).order_by("last_name")

    class Meta:
        model = Invitation
        exclude = ["banquet", "participant", "denied", "token"]
