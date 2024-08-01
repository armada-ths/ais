from django import forms
from django.contrib.auth.models import User
import inspect

from companies.models import Company, CompanyCustomerComment
from .models import ExhibitorChat, ExhibitorView, Exhibitor, Booth, ExhibitorInBooth

from dal import autocomplete


class ExhibitorViewForm(forms.Form):
    instance = None

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.setdefault("instance", None)
        user = kwargs.setdefault("user", None)

        kwargs.pop("instance")
        kwargs.pop("user")

        super(ExhibitorViewForm, self).__init__(*args, **kwargs)

        if not self.instance:
            if not user:
                raise Exception("No user or instance supplied to ExhibitorViewForm")

            self.instance = ExhibitorView(user=user)

        for name_system in ExhibitorView.selectable_fields:
            name_friendly = ExhibitorView.selectable_fields[name_system]
            self.fields[name_system] = forms.BooleanField(
                label=name_friendly,
                initial=(name_system in self.instance.choices),
                required=False,
            )

    def save(self, commit=True):
        saved_fields = ""

        for name_system, name_friendly in self.cleaned_data.items():
            if name_friendly:
                saved_fields += " " + name_system

        self.instance.choices = saved_fields.strip()

        if commit:
            self.instance.save()

        return self.instance


class ExhibitorCreateForm(forms.Form):
    companies = forms.ModelMultipleChoiceField(
        queryset=Company.objects.all(),
        widget=forms.SelectMultiple(attrs={"size": 20}),
        required=True,
        label="Companies from the initial registration",
    )


class ExhibitorCreateBypassedForm(forms.Form):
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        widget=forms.Select(),
        required=True,
        label="Select a company that you want to add as an exhibitor.",
    )
    company.help_text = "Only companies that have not signed the initial contract or been added as exhibitors are shown in the list."


class TransportForm(forms.ModelForm):
    class Meta:
        model = Exhibitor
        fields = ["transport_to", "transport_from", "transport_comment"]


class ContactPersonForm(forms.ModelForm):
    class Meta:
        model = Exhibitor
        fields = ["contact_persons"]

        widgets = {"contact_persons": forms.SelectMultiple(attrs={"size": 30})}


class CheckInForm(forms.Form):
    comment = forms.CharField(
        required=False,
        label="Optional comment",
        widget=forms.Textarea(attrs={"rows": 5}),
    )


class DetailsForm(forms.ModelForm):
    class Meta:
        model = Exhibitor
        fields = ["deadline_complete_registration"]

        widgets = {
            "deadline_complete_registration": forms.TextInput(
                attrs={"placeholder": "Y-m-d H:i:s, e.g. 1995-10-10 13:37:00"}
            ),
        }


class CoordinatesForm(forms.ModelForm):
    class Meta:
        model = Exhibitor
        fields = ["map_coordinates"]


class FairLocationForm(forms.ModelForm):
    class Meta:
        model = Exhibitor
        fields = ["fair_location"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = CompanyCustomerComment
        fields = ["comment"]


class ChatForm(forms.ModelForm):
    class Meta:
        model = ExhibitorChat
        fields = ["chat"]
        widgets = {
            "chat": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class BoothForm(forms.ModelForm):
    class Meta:
        model = Booth
        fields = ["location", "name"]


class ExhibitorForm(forms.ModelForm):
    class Meta:
        model = Exhibitor
        fields = "__all__"
        widgets = {
            "contact_persons": autocomplete.ModelSelect2Multiple(
                url="user-autocomplete", attrs={"data-html": True}
            )
        }


class ExhibitorInBoothForm(forms.ModelForm):
    class Meta:
        model = ExhibitorInBooth
        fields = ["exhibitor", "days", "comment"]

        widgets = {"days": forms.CheckboxSelectMultiple()}


class ExhibitorSearchForm(forms.Form):
    contact_persons = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        label="Show only exhibitors for which any of the following people are contact persons",
        required=False,
        widget=forms.SelectMultiple(attrs={"size": 10}),
    )
