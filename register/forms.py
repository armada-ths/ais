import re, datetime

from django.forms import (
    TextInput,
    Select,
    RadioSelect,
    ModelForm,
    Form,
    BooleanField,
    ModelMultipleChoiceField,
    CheckboxSelectMultiple,
    ValidationError,
    IntegerField,
    CharField,
    ChoiceField,
)
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe, format_html
from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth.models import User

from companies.models import Group, Company
from exhibitors.models import (
    Exhibitor,
    CatalogueIndustry,
    CatalogueCompetence,
    CatalogueValue,
    CatalogueBenefit,
    CatalogueLocation,
    CatalogueEmployment,
)
from banquet.models import Participant as BanquetParticipant
from fair.models import Fair, LunchTicket, FairDay


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


def fix_url(url):
    if url is None:
        return None

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    return url


class InitialInterestsRegistrationForm(Form):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.filter(allow_registration=True, fair__current=True),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label="",
    )


class InitialCommentForm(Form):
    text_input = forms.CharField(required=False)
    text_input.label = "Comment regarding your additional interests"


class InitialRegistrationForm(Form):
    agreement_accepted = BooleanField(required=True)
    agreement_accepted.label = "I have read the binding contract and agree to terms, and I am also authorized to register my organization for THS Armada 2023 and sign this contract."

    gdpr_accepted = BooleanField(required=True)
    gdpr_accepted.label = "THS Armada would like to process personal data about you and your organization to be able to contact you in conjunction with complete registration and send you information regarding the fair of 2023. The data we intend to collect and the process is forename, surname, the title of your organization, phone number, and email address. You decide for yourself if you want to leave any additional information to us. The data will only be processed by the project group in THS Armada and by THS Management. The data will be saved in the Armada Internal Systems, AIS. You are, according to GDPR (General Data Protection Regulation), entitled to receive information regarding what personal data we process and how we process these. You also have the right to request a correction as to what personal data we are processing about you. \nI consent for THS Armada to process my personal data in accordance with the above."


class CompleteCompanyDetailsForm(ModelForm):
    class Meta:
        model = Company
        fields = [
            "name",
            "identity_number",
            "invoice_name",
            "general_email_address",
            "invoice_address_line_1",
            "invoice_address_line_2",
            "invoice_address_line_3",
            "invoice_zip_code",
            "invoice_city",
            "invoice_country",
            "invoice_reference",
            "invoice_email_address",
        ]

        labels = {
            "identity_number": "Organization's corporate identity number",
            "general_email_address": "If available, please provide a non-personal e-mail address for future contact between Armada and your organization",
            "invoice_address_line_1": "Invoice address line 1 (required to sign contract)",
            "invoice_zip_code": "Invoice zip code (required to sign contract)",
            "invoice_city": "Invoice city (required to sign contract)",
            "invoice_country": "Invoice country (required to sign contract)",
        }

        help_texts = {
            "name": "Your company's every-day name; the name students will know you by.",
            "general_email_address": "This is to simplify the process of reaching out to your organization for the upcoming years' fairs.",
            "invoice_name": "This should be your company's complete legal name.",
            "invoice_reference": "Name of your reference, your Purchase Order Number or equivalent.",
            "invoice_email_address": "If you enter an e-mail address here, the invoice will be sent only through e-mail. Leave the field blank to receive the invoice by regular mail.",
        }

    def clean(self):
        super(CompleteCompanyDetailsForm, self).clean()

        if (
            "invoice_zip_code" in self.cleaned_data
            and self.cleaned_data["invoice_zip_code"] is not None
            and re.match(r"[0-9]{5}$", self.cleaned_data["invoice_zip_code"])
        ):
            self.cleaned_data["invoice_zip_code"] = (
                self.cleaned_data["invoice_zip_code"][0:3]
                + " "
                + self.cleaned_data["invoice_zip_code"][3:5]
            )

        if (
            "invoice_email_address" in self.cleaned_data
            and self.cleaned_data["invoice_email_address"] is not None
        ):
            self.cleaned_data["invoice_email_address"] = self.cleaned_data[
                "invoice_email_address"
            ].lower()

        if (
            "general_email_address" in self.cleaned_data
            and self.cleaned_data["general_email_address"] is not None
        ):
            self.cleaned_data["general_email_address"] = self.cleaned_data[
                "general_email_address"
            ].lower()

        return self.cleaned_data

    def is_valid(self):
        valid = super(CompleteCompanyDetailsForm, self).is_valid()

        if not valid:
            return valid

        invoice_zip_code = self.cleaned_data.get("invoice_zip_code")
        invoice_country = self.cleaned_data.get("invoice_country")

        if (
            invoice_zip_code is not None
            and invoice_country is not None
            and invoice_country == "SWEDEN"
            and not re.match(r"[0-9]{3} [0-9]{2}$", invoice_zip_code)
        ):
            self.add_error("invoice_zip_code", "Invalid Swedish zip code.")
            valid = False

        if (
            invoice_zip_code is not None
            and invoice_country is not None
            and invoice_country == "NORWAY"
            and not re.match(r"[0-9]{4}$", invoice_zip_code)
        ):
            self.add_error("invoice_zip_code", "Invalid Norwegian zip code.")
            valid = False

        return valid


class CompleteLogisticsDetailsForm(ModelForm):
    class Meta:
        model = Exhibitor
        fields = [
            "booth_height",
            "electricity_total_power",
            "electricity_socket_count",
            "electricity_equipment",
            "placement_wish",
            "placement_comment",
        ]

        widgets = {
            "electricity_equipment": forms.Textarea(attrs={"rows": 5}),
            "placement_wish": forms.RadioSelect,
            "placement_comment": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "We will consider your wish of placement, but we cannot give any guarantees.",
                }
            ),
        }

        labels = {
            "booth_height": "Height of the booth (cm) (required to sign contract)",
            "electricity_total_power": "Estimated power consumption (W) (required to sign contract)",
            "electricity_socket_count": "Number of sockets (required to sign contract)",
        }

        help_texts = {
            "electricity_total_power": """
				If possible, please provide the actual power consumption figures of the
				equipment you plan to bring.
				Typical power requirements of common devices are presented in a table below this form.
				1000 W is included in the Base kit. If you require additional electricity,
				remember to add "Additional Electricity" in the Products section below.""",
            "booth_height": '230 cm is included in the Base kit. If you want additional height, remember to add "Additional Booth Height" in the Products section below.',
            "placement_wish": 'We will use the industry information you provide in the section "Exhibitor catalogue" to facilitate your placement wish. If you have other wishes for industry segmentation please provide a comment below.',
        }

    def is_valid(self):
        valid = super(CompleteLogisticsDetailsForm, self).is_valid()

        if not valid:
            return valid

        booth_height = self.cleaned_data.get("booth_height")

        if booth_height is not None and (booth_height < 10 or booth_height > 1000):
            self.add_error(
                "booth_height", "The boot height must be between 10 and 1000 cm."
            )
            valid = False

        return valid


class CompleteLogisticsDetailsFormWithCheckbox(CompleteLogisticsDetailsForm):
    class Meta(CompleteLogisticsDetailsForm.Meta):
        fields = ["confirmation_box"] + CompleteLogisticsDetailsForm.Meta.fields

    confirmation_box = forms.BooleanField(
        required=False,
        label="<strong>I have read the information regarding booth equipment and transportation above and I am aware of the services offered. (required to sign contract)</strong>",
    )

    def is_valid(self):
        valid = super(CompleteLogisticsDetailsFormWithCheckbox, self).is_valid()
        if not valid:
            return valid

        box_checked = self.cleaned_data.get("confirmation_box")
        if not box_checked:
            self.add_error("confirmation_box", "Please check this box.")
            valid = False

        return valid


class CompleteCatalogueDetailsForm(ModelForm):
    # custom defined field subclass to overwrite string representation
    class IncludeCategoryChoiceField(ModelMultipleChoiceField):
        def label_from_instance(self, choice):
            if choice.category:
                return str(choice.category) + " - " + str(choice)
            else:
                return str(choice)

    catalogue_industries = IncludeCategoryChoiceField(
        queryset=CatalogueIndustry.objects.filter(include_in_form=True),
        widget=forms.CheckboxSelectMultiple,
        label="Which main fields of studies apply to your company’s business?",
        required=False,
    )
    # UNCOMMENT THE BELOW ONES IF YOU WANT TO INCLUDE THEM IN THE FINAL REGISTRATION PAGE (COMPLETE REGISTRATION), ALSO REMOVE THE ABOVE ONE TO AVOID DUPLICATE
    # catalogue_industries = IncludeCategoryChoiceField(
    #    queryset=CatalogueIndustry.objects.filter(include_in_form=True),
    #    widget=forms.CheckboxSelectMultiple,
    #    label='Which industries does your company work in?',
    #    required=False)
    # catalogue_competences = IncludeCategoryChoiceField(
    #    queryset=CatalogueCompetence.objects.filter(include_in_form=True),
    #    widget=forms.CheckboxSelectMultiple,
    #    label='What competences is your company looking for?',
    #    required=False)
    # catalogue_values = forms.ModelMultipleChoiceField(
    #    queryset=CatalogueValue.objects.filter(include_in_form=True),
    #    widget=forms.CheckboxSelectMultiple,
    #    label='Select up to three values that apply to the company.',
    #    required=False)
    catalogue_employments = forms.ModelMultipleChoiceField(
        queryset=CatalogueEmployment.objects.filter(include_in_form=True),
        widget=forms.CheckboxSelectMultiple,
        label="What kind of employments does your company offer?",
        required=False,
    )
    catalogue_locations = forms.ModelMultipleChoiceField(
        queryset=CatalogueLocation.objects.filter(include_in_form=True),
        widget=forms.CheckboxSelectMultiple,
        label="Where does your company operate?",
        required=False,
    )

    # catalogue_benefits = forms.ModelMultipleChoiceField(
    # 	queryset = CatalogueBenefit.objects.filter(include_in_form = True),
    # 	widget = forms.CheckboxSelectMultiple,
    # 	label = 'Which benefits does your company offer its employees?',
    # 	required = False)

    class Meta:
        model = Exhibitor
        # fields = ['catalogue_about', 'catalogue_purpose', 'catalogue_logo_squared', 'catalogue_logo_freesize', 'catalogue_contact_name', 'catalogue_contact_email_address', 'catalogue_contact_phone_number', 'catalogue_industries', 'catalogue_values', 'catalogue_employments', 'catalogue_locations', 'catalogue_benefits', 'catalogue_average_age', 'catalogue_founded']
        fields = [
            "catalogue_about",
            "catalogue_logo_squared",
            "catalogue_logo_freesize",
            "catalogue_contact_name",
            "catalogue_contact_email_address",
            "catalogue_contact_phone_number",
            "catalogue_industries",
            "catalogue_employments",
            "catalogue_locations",
            "catalogue_cities",
        ]

        help_texts = {
            "catalogue_logo_squared": "Allowed formats are JPEG and PNG.",
            "catalogue_logo_freesize": "Allowed formats are JPEG and PNG.",
            #'catalogue_average_age': 'Leave the field empty if you\'re unsure.',
            "catalogue_about": "Keep it concise – no more than 600 characters. Please write in english to reach both Swedish and international students.",
            #'catalogue_purpose': 'Keep it concise – no more than 600 characters.',
            "catalogue_contact_name": "This is the person that students will be referred to if they wish to get in touch with you outside of the career fair.",
            "catalogue_cities": "E.g: Stockholm, Gothenburg, London",
        }

        labels = {
            "catalogue_about": "Text about your organisation (required to sign contract)",
            #'catalogue_purpose': 'Your organisation\'s purpose',
            "catalogue_logo_squared": "Upload your company's squared logotype. (required to sign contract)",
            "catalogue_logo_freesize": "Upload your company's logotype in any dimensions, in addition to the squared logotype.",
            "catalogue_cities": "Please write the main cities where your company operates. Separate the cities with commas.",
            #'catalogue_founded': 'Which year was the company founded?'
        }

        widgets = {
            "catalogue_about": forms.Textarea(
                attrs={
                    "maxlength": 600,
                    "rows": 3,
                    "placeholder": "What does your organisation work with?",
                }
            ),
            "catalogue_cities": forms.Textarea(attrs={"maxlength": 400, "rows": 1}),
            #'catalogue_purpose': forms.Textarea(attrs = {'maxlength': 600, 'rows': 3, 'placeholder': 'What does your organisation believe in?'}),
        }

    def clean(self):
        super(CompleteCatalogueDetailsForm, self).clean()

        if (
            "catalogue_contact_email_address" in self.cleaned_data
            and self.cleaned_data["catalogue_contact_email_address"] is not None
        ):
            self.cleaned_data["catalogue_contact_email_address"] = self.cleaned_data[
                "catalogue_contact_email_address"
            ].lower()

        if "catalogue_contact_phone_number" in self.cleaned_data:
            self.cleaned_data["catalogue_contact_phone_number"] = fix_phone_number(
                self.cleaned_data["catalogue_contact_phone_number"]
            )

        return self.cleaned_data

    def is_valid(self):
        valid = super(CompleteCatalogueDetailsForm, self).is_valid()

        if not valid:
            return valid

        catalogue_contact_phone_number = self.cleaned_data.get(
            "catalogue_contact_phone_number"
        )
        catalogue_logo_squared = self.cleaned_data.get("catalogue_logo_squared")
        # catalogue_number_values = self.cleaned_data.get(
        #   'catalogue_values').count()
        # catalogue_founded = self.cleaned_data.get('catalogue_founded')

        if catalogue_contact_phone_number is not None and not re.match(
            r"\+[0-9]+$", catalogue_contact_phone_number
        ):
            self.add_error(
                "catalogue_contact_phone_number",
                "Must only contain numbers and a leading plus.",
            )
            valid = False

        # if catalogue_number_values > 3:
        #   self.add_error('catalogue_values',
        #                 'You can not select more than 3 values.')
        # valid = False

        # if catalogue_founded is not None and (catalogue_founded < 1600 or catalogue_founded > datetime.datetime.now().year):
        # 	self.add_error('catalogue_founded', 'The year is invalid.')
        # 	valid = False

        return valid


class CompleteProductQuantityForm(Form):
    quantity = ChoiceField(choices=[], label="", required=True)


class CompleteProductBooleanForm(Form):
    checkbox = BooleanField(label="", required=False)


class CompleteFinalSubmissionForm(Form):
    # contract = BooleanField(required=True)
    # contract.label = 'I have read the binding contract and agree to the terms. I am also authorized to register my organization for THS Armada 2023 and sign this contract.'

    gdpr = BooleanField(required=True)
    gdpr.label = "THS Armada would like to process personal data about you and your organization to be able to contact you in conjunction with complete registration and send you information regarding the fair of 2023. The data we intend to collect and the process is forename, surname, the title of your organization, phone number, and email address. You decide for yourself if you want to leave any additional information to us. The data will only be processed by the project group in THS Armada and by THS Management. The data will be saved in the Armada Internal Systems, AIS. You are, according to GDPR (General Data Protection Regulation), entitled to receive information regarding what personal data we process and how we process these. You also have the right to request a correction as to what personal data we are processing about you. \nI consent for THS Armada to process my personal data in accordance with the above."


# form is also used to edit company info during initial registration
class NewCompanyForm(ModelForm):
    def clean(self):
        super(NewCompanyForm, self).clean()
        # make sure http:// is included in the url, otherwise the url will not direct to correct website in CRM
        if "website" in self.cleaned_data:
            self.cleaned_data["website"] = fix_url(self.cleaned_data["website"])

        if (
            "general_email_address" in self.cleaned_data
            and self.cleaned_data["general_email_address"] is not None
        ):
            self.cleaned_data["general_email_address"] = self.cleaned_data[
                "general_email_address"
            ].lower()

        return self.cleaned_data

    class Meta:
        model = Company
        fields = ["name", "identity_number", "website", "type", "general_email_address"]

        labels = {
            "general_email_address": "If available, please provide a non-personal e-mail address for future contact between Armada and your organization",
        }

        help_texts = {
            "general_email_address": "This is to simplify the process of reaching out to your organization for the upcoming years' fairs.",
        }


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = ""
        self.fields["password"].label = ""
        self.fields["username"].widget = forms.TextInput(
            attrs={"class": "input", "placeholder": "Email"}
        )
        self.fields["password"].widget = forms.TextInput(
            attrs={"class": "input", "placeholder": "Password", "type": "password"}
        )

    def clean(self):
        self.cleaned_data["username"] = self.cleaned_data["username"].lower()
        super(LoginForm, self).clean()


class ResetPasswordForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.fields["email"].label = ""
        self.fields["email"].widget = forms.TextInput(
            attrs={"class": "input", "placeholder": "Email"}
        )


class SetNewPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(SetNewPasswordForm, self).__init__(*args, **kwargs)
        self.fields["new_password1"].label = ""
        self.fields["new_password2"].label = ""
        self.fields["new_password1"].widget = forms.TextInput(
            attrs={"class": "input", "placeholder": "New Password", "type": "password"}
        )
        self.fields["new_password2"].widget = forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": "New Password Confirmation",
                "type": "password",
            }
        )


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        self.fields["old_password"].label = ""
        self.fields["new_password1"].label = ""
        self.fields["new_password2"].label = ""
        self.fields["old_password"].widget = forms.TextInput(
            attrs={"class": "input", "placeholder": "Old Password", "type": "password"}
        )
        self.fields["new_password1"].widget = forms.TextInput(
            attrs={"class": "input", "placeholder": "New Password", "type": "password"}
        )
        self.fields["new_password2"].widget = forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": "New Password Confirmation",
                "type": "password",
            }
        )


# OLD form - not used in 2019-
class RegistrationForm(ModelForm):
    # TODO: this needs to be Fair-specific
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.filter(allow_registration=True),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label="",
    )

    class Meta:
        model = Company
        fields = ("groups",)

    agreement_accepted = BooleanField(required=True)
    agreement_accepted.label = "I have read the contract and agree to terms*"

    gdpr_accepted = BooleanField(required=True)
    gdpr_accepted.label = "THS Armada would like to process personal data about you and your organization to be able to contact you in conjunction with initial registration, complete registration and send you information regarding the fair of 2023. The data we intend to collect and the process is forename, surname, the title of your organization, phone number, and email address. You decide for yourself if you want to leave any additional information to us. The data will only be processed by the project group in Armada and will be saved in the Armada Internal Systems, AIS. You are, according to GDPR (General Data Protection Regulation), entitled to receive information regarding what personal data we process and how we process these. You also have the right to request a correction as to what personal data we are processing about you.\nI consent for THS Armada to process my personal data in accordance with the above.*"

    authorized_accepted = BooleanField(required=True)
    authorized_accepted.label = (
        "I am authorized to register my company for Armada 2023 and sign this contract*"
    )


class TransportForm(Form):
    contact_name = forms.CharField(
        max_length=100,
        label="Contact person's name",
        help_text="The person at your company who is responsible for the parcels to and from the fair.",
    )
    contact_email_address = forms.CharField(
        max_length=100,
        label="Contact person's e-mail address",
        help_text="This is the e-mail address to which Ryska posten will respond.",
    )
    contact_phone_number = forms.CharField(
        max_length=100, label="Contact person's phone number"
    )
    description_of_parcels = forms.CharField(
        widget=forms.Textarea,
        help_text="Describe your parcels as detailed as possible; how many, their sizes, their weights etc. The description can be either in English or in Swedish.",
    )
    address_details = forms.CharField(
        widget=forms.Textarea,
        help_text="Physical addresses that Ryska posten should collected from and deliver the parcels to.",
    )


class LunchTicketForm(ModelForm):
    day = forms.ModelChoiceField(
        queryset=FairDay.objects.filter(fair__current=True),
        widget=forms.RadioSelect,
        required=True,
    )

    class Meta:
        model = LunchTicket
        fields = [
            "email_address",
            "comment",
            "day",
            "dietary_restrictions",
            "other_dietary_restrictions",
        ]

        widgets = {
            "dietary_restrictions": forms.CheckboxSelectMultiple(),
            "other_dietary_restrictions": forms.TextInput(),
        }

        help_texts = {
            "dietary_restrictions": "Please note that the lunch is entirely vegetarian.",
            "other_dietary_restrictions": "Please leave empty if no other restrictions.",
            "email_address": "The lunch ticket will be sent to this e-mail address in advance of the career fair.",
            "comment": "The comment is for your use only. It could, for instance, contain the name of the person who is going to use the ticket.",
        }


class BanquetParticipantForm(ModelForm):
    def clean(self):
        super(BanquetParticipantForm, self).clean()

        if "phone_number" in self.cleaned_data:
            self.cleaned_data["phone_number"] = fix_phone_number(
                self.cleaned_data["phone_number"]
            )

        return self.cleaned_data

    def is_valid(self):
        valid = super(BanquetParticipantForm, self).is_valid()

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
        model = BanquetParticipant
        fields = [
            "banquet",
            "name",
            "email_address",
            "phone_number",
            "dietary_restrictions",
            "other_dietary_restrictions",
            "alcohol",
            "giveaway",
        ]

        labels = {
            "giveaway": "Giveaway ticket",
        }

        widgets = {
            "dietary_restrictions": forms.CheckboxSelectMultiple(),
            "other_dietary_restrictions": forms.TextInput(),
            "alcohol": forms.RadioSelect(),
            "giveaway": forms.RadioSelect(),
        }

        help_texts = {
            "other_dietary_restrictions": "Please leave empty if no other restrictions.",
            #'email_address': 'The banquet ticket will be sent to this e-mail address.',
            "giveaway": "We plan to use this ticket in a giveaway for students.",
        }
