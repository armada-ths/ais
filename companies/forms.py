import re, datetime

from django.forms import ModelForm, HiddenInput, BaseModelFormSet
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from register.models import SignupContract
from accounting.models import Product, Order
from .models import (
    Company,
    CompanyAddress,
    CompanyCustomer,
    CompanyCustomerResponsible,
    CompanyContact,
    CompanyCustomerComment,
    Group,
)
from fair.models import Fair


def fix_url(url):
    if url is None:
        return None

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    return url


# this form is used internally to edit company details in the CRM app
class CompanyForm(ModelForm):
    def clean(self):
        super(CompanyForm, self).clean()
        # make sure http:// is included in the url, otherwise the url will not direct to correct website in CRM
        if "website" in self.cleaned_data:
            self.cleaned_data["website"] = fix_url(self.cleaned_data["website"])
        return self.cleaned_data

    class Meta:
        model = Company
        fields = [
            "show_externally",
            "name",
            "identity_number",
            "website",
            "general_email_address",
            "type",
            "ths_customer_id",
            "invoice_name",
            "invoice_address_line_1",
            "invoice_address_line_2",
            "invoice_address_line_3",
            "invoice_zip_code",
            "invoice_city",
            "invoice_country",
            "invoice_reference",
            "invoice_email_address",
            "e_invoice",
        ]


class CompanyAddressForm(ModelForm):
    class Meta:
        model = CompanyAddress
        fields = "__all__"


class GroupForm(ModelForm):
    parent = forms.ModelChoiceField(
        queryset=Group.objects.filter(fair__current=True), required=False
    )
    contract = forms.ModelChoiceField(
        queryset=SignupContract.objects.filter(fair__current=True), required=False
    )

    class Meta:
        model = Group
        fields = "__all__"

    def is_valid(self, group):
        valid = super(GroupForm, self).is_valid()

        if not valid:
            return valid

        parent = self.cleaned_data.get("parent")
        allow_companies = self.cleaned_data.get("allow_companies")
        allow_registration = self.cleaned_data.get("allow_registration")

        if parent is not None and parent == group:
            self.add_error("parent", "The group cannot be its own parent.")
            valid = False

        if not allow_companies and allow_registration:
            self.add_error(
                "allow_registration",
                "Companies must be allowed in order to allow registration.",
            )
            valid = False

        return valid

    def __init__(self, fair, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)

        self.initial["fair"] = fair.id
        self.fields["fair"].disabled = True
        self.fields["fair"].widget = HiddenInput()


class BaseCompanyAddressFormSet(BaseModelFormSet):
    def clean(self):
        if any(self.errors):
            return

        for form in self.forms:
            pass


class BaseCompanyContactFormSet(BaseModelFormSet):
    def clean(self):
        if any(self.errors):
            return

        for form in self.forms:
            pass


class CompanyCustomerResponsibleForm(ModelForm):
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(), widget=forms.RadioSelect(), required=True
    )
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=True,
    )

    def __init__(self, company, *args, **kwargs):
        super(CompanyCustomerResponsibleForm, self).__init__(*args, **kwargs)
        self.initial["company"] = company.id
        self.fields["company"].disabled = True
        self.fields["company"].widget = HiddenInput()

    class Meta:
        model = CompanyCustomerResponsible
        fields = "__all__"

    def is_valid(self):
        valid = super(CompanyCustomerResponsibleForm, self).is_valid()

        if not valid:
            return valid

        group = self.cleaned_data.get("group")

        if not group.allow_responsibilities:
            self.add_error("group", "This group cannot be used for responsibilities.")
            valid = False

        return valid


class CompanyCustomerCommentForm(ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.filter(allow_comments=True, fair__current=True),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        model = CompanyCustomerComment
        fields = ["groups", "comment", "show_in_exhibitors"]


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


# form to be used for intital registration, excludes user, company, active, confirmed as the contact person should not see this
class InitialCompanyContactForm(ModelForm):
    def clean(self):
        super(InitialCompanyContactForm, self).clean()

        if "mobile_phone_number" in self.cleaned_data:
            self.cleaned_data["mobile_phone_number"] = fix_phone_number(
                self.cleaned_data["mobile_phone_number"]
            )

        if "work_phone_number" in self.cleaned_data:
            self.cleaned_data["work_phone_number"] = fix_phone_number(
                self.cleaned_data["work_phone_number"]
            )

        if (
            "email_address" in self.cleaned_data
            and self.cleaned_data["email_address"] is not None
        ):
            self.cleaned_data["email_address"] = self.cleaned_data[
                "email_address"
            ].lower()

        return self.cleaned_data

    def is_valid(self):
        valid = super(InitialCompanyContactForm, self).is_valid()

        if not valid:
            return valid

        mobile_phone_number = self.cleaned_data.get("mobile_phone_number")
        work_phone_number = self.cleaned_data.get("work_phone_number")

        if mobile_phone_number is not None and not re.match(
            r"\+[0-9]+$", mobile_phone_number
        ):
            self.add_error(
                "mobile_phone_number", "Must only contain numbers and a leading plus."
            )
            valid = False

        if work_phone_number is not None and not re.match(
            r"\+[0-9]+$", work_phone_number
        ):
            self.add_error(
                "work_phone_number", "Must only contain numbers and a leading plus."
            )
            valid = False

        return valid

    class Meta:
        model = CompanyContact
        fields = "__all__"
        exclude = ["user", "company", "active", "confirmed"]


class CompanyContactForm(ModelForm):
    def clean(self):
        super(CompanyContactForm, self).clean()

        if "mobile_phone_number" in self.cleaned_data:
            self.cleaned_data["mobile_phone_number"] = fix_phone_number(
                self.cleaned_data["mobile_phone_number"]
            )

        if "work_phone_number" in self.cleaned_data:
            self.cleaned_data["work_phone_number"] = fix_phone_number(
                self.cleaned_data["work_phone_number"]
            )

        if (
            "email_address" in self.cleaned_data
            and self.cleaned_data["email_address"] is not None
        ):
            self.cleaned_data["email_address"] = self.cleaned_data[
                "email_address"
            ].lower()

        return self.cleaned_data

    def is_valid(self):
        valid = super(CompanyContactForm, self).is_valid()

        if not valid:
            return valid

        mobile_phone_number = self.cleaned_data.get("mobile_phone_number")
        work_phone_number = self.cleaned_data.get("work_phone_number")

        if mobile_phone_number is not None and not re.match(
            r"\+[0-9]+$", mobile_phone_number
        ):
            self.add_error(
                "mobile_phone_number", "Must only contain numbers and a leading plus."
            )
            valid = False

        if work_phone_number is not None and not re.match(
            r"\+[0-9]+$", work_phone_number
        ):
            self.add_error(
                "work_phone_number", "Must only contain numbers and a leading plus."
            )
            valid = False

        return valid

    class Meta:
        model = CompanyContact
        fields = "__all__"
        exclude = ["user", "company"]


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["password1", "password2"]


class CreateCompanyContactForm(ModelForm):
    def clean(self):
        super(CreateCompanyContactForm, self).clean()

        if "mobile_phone_number" in self.cleaned_data:
            self.cleaned_data["mobile_phone_number"] = fix_phone_number(
                self.cleaned_data["mobile_phone_number"]
            )

        if "work_phone_number" in self.cleaned_data:
            self.cleaned_data["work_phone_number"] = fix_phone_number(
                self.cleaned_data["work_phone_number"]
            )

        if (
            "email_address" in self.cleaned_data
            and self.cleaned_data["email_address"] is not None
        ):
            self.cleaned_data["email_address"] = self.cleaned_data[
                "email_address"
            ].lower()

        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(CreateCompanyContactForm, self).__init__(*args, **kwargs)
        self.fields["company"].queryset = Company.objects.filter(show_externally=True)
        self.fields["company"].label = "Find your company"
        self.fields["company"].widget = forms.TextInput(attrs={"id": "browser"})

    class Meta:
        model = CompanyContact
        fields = "__all__"
        exclude = ("user", "active", "confirmed")
        widgets = {"company": forms.TextInput}

    def is_valid(self):
        valid = super(CreateCompanyContactForm, self).is_valid()

        if not valid:
            return valid

        email_address = self.cleaned_data["email_address"]
        mobile_phone_number = self.cleaned_data.get("mobile_phone_number")
        work_phone_number = self.cleaned_data.get("work_phone_number")

        if User.objects.filter(username=email_address).first() != None:
            self.add_error("email_address", "Account already exists")
            return False

        if mobile_phone_number is not None and not re.match(
            r"\+[0-9]+$", mobile_phone_number
        ):
            self.add_error(
                "mobile_phone_number", "Must only contain numbers and a leading plus."
            )
            valid = False

        if work_phone_number is not None and not re.match(
            r"\+[0-9]+$", work_phone_number
        ):
            self.add_error(
                "work_phone_number", "Must only contain numbers and a leading plus."
            )
            valid = False

        return valid


class CreateCompanyContactNoCompanyForm(CreateCompanyContactForm):
    def __init__(self, *args, **kwargs):
        super(CreateCompanyContactForm, self).__init__(*args, **kwargs)

    class Meta:
        model = CompanyContact
        fields = "__all__"
        exclude = ("user", "active", "confirmed", "company")


class CompanyCustomerStatusForm(forms.Form):
    status = forms.ModelChoiceField(
        queryset=Group.objects.all(), required=False, label="Status"
    )


class DateInput(forms.DateInput):
    input_type = "date"


class StatisticsForm(forms.Form):
    date_from = forms.DateField(
        widget=DateInput(),
    )
    date_to = forms.DateField(initial=datetime.date.today, widget=DateInput())


class CompanyNewOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ["product", "quantity"]

    def is_valid(self):
        valid = super(CompanyNewOrderForm, self).is_valid()

        if not valid:
            return valid

        product = self.cleaned_data["product"]
        quantity = self.cleaned_data["quantity"]

        if quantity < 1:
            self.add_error("quantity", "Must be a positive integer.")
            return False

        if product.max_quantity is not None and quantity > product.max_quantity:
            self.add_error(
                "quantity", "Must not exceed " + str(product.max_quantity) + "."
            )
            return False

        return valid


class CompanyEditOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ["name", "quantity", "unit_price", "comment"]

    def is_valid(self):
        valid = super(CompanyEditOrderForm, self).is_valid()

        if not valid:
            return valid

        quantity = self.cleaned_data["quantity"]

        if quantity < 1:
            self.add_error("quantity", "Must be a positive integer.")
            return False

        if (
            self.instance.product.max_quantity is not None
            and quantity > self.instance.product.max_quantity
        ):
            self.add_error(
                "quantity", "Must not exceed " + str(product.max_quantity) + "."
            )
            return False

        return valid


class CompanySearchForm(forms.Form):
    exhibitors_choices = [
        ("BOTH", "Show both exhibitors and non-exhibitors"),
        ("NO", "Show only non-exhibitors"),
        ("YES", "Show only exhibitors"),
    ]

    exhibitors_year = forms.ChoiceField(
        widget=forms.Select(), label="For the year: ", required=True
    )
    exhibitors = forms.ChoiceField(
        choices=exhibitors_choices,
        widget=forms.RadioSelect(),
        initial="BOTH",
        required=True,
    )
    contracts_positive = forms.ModelMultipleChoiceField(
        queryset=SignupContract.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
        label="Show only companies who have signed any of these",
        required=False,
    )
    contracts_negative = forms.ModelMultipleChoiceField(
        queryset=SignupContract.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
        # Note: Sales required that "NOT" is to be underlined, this is now done in
        # the HTML file "companies/companies_list.html"
        # label="Show only companies who have NOT signed any of these",
        required=False,
    )
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        label="Show only companies for which any of the following people are responsible",
        required=False,
    )
    q = forms.CharField(
        label="Search:",
        required=False,
    )


class ContractExportForm(forms.Form):
    contract = forms.ModelChoiceField(
        queryset=SignupContract.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        label="Contract to export signatures for",
    )

    exhibitors_choices = [
        ("BOTH", "Show both exhibitors and non-exhibitors"),
        ("NO", "Show only non-exhibitors"),
        ("YES", "Show only exhibitors"),
    ]

    exhibitors = forms.ChoiceField(
        choices=exhibitors_choices,
        widget=forms.RadioSelect(),
        initial="BOTH",
        required=True,
    )

    companies_choices = [
        ("BOTH", "Show both companies with signatures and those without"),
        ("YES", "Show only companies with signatures"),
    ]

    companies = forms.ChoiceField(
        choices=companies_choices,
        widget=forms.RadioSelect(),
        initial="BOTH",
        required=True,
    )
