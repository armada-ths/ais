import re

from django import forms
from django.forms import ModelForm
from django.utils import timezone

from .models import Profile


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


class ProfileForm(ModelForm):
    def clean(self):
        super(ProfileForm, self).clean()

        if "phone_number" in self.cleaned_data:
            self.cleaned_data["phone_number"] = fix_phone_number(
                self.cleaned_data["phone_number"]
            )

        return self.cleaned_data

    def is_valid(self):
        valid = super(ProfileForm, self).is_valid()

        if not valid:
            return valid

        dietary_restrictions = self.cleaned_data.get("dietary_restrictions")
        other_dietary_restrictions = self.cleaned_data.get("other_dietary_restrictions")
        no_dietary_restrictions = self.cleaned_data.get("no_dietary_restrictions")

        phone_number = self.cleaned_data.get("phone_number")

        if (
            len(dietary_restrictions) == 0
            and not other_dietary_restrictions
            and not no_dietary_restrictions
        ):
            self.add_error(
                "no_dietary_restrictions",
                "If you have no dietary restrictions, tick this box to confirm.",
            )
            valid = False

        elif (
            len(dietary_restrictions) != 0 or other_dietary_restrictions
        ) and no_dietary_restrictions:
            self.add_error(
                "no_dietary_restrictions",
                "If you have dietary restrictions, you cannot tick this box. Leave the other dietary restrictions text field empty if not needed.",
            )
            valid = False

        if phone_number is not None and not re.match(r"\+[0-9]+$", phone_number):
            self.add_error(
                "phone_number", "Must only contain numbers and a leading plus."
            )
            valid = False

        return valid

    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ["user", "picture", "token", "kth_synchronize"]

        widgets = {
            "registration_year": forms.Select(
                choices=[("", "--------")]
                + [(year, year) for year in range(2000, timezone.now().year + 1)]
            ),
            "birth_date": forms.DateInput(),
            "planned_graduation": forms.Select(
                choices=[("", "--------")]
                + [(year, year) for year in range(2000, timezone.now().year + 10)]
            ),
            "dietary_restrictions": forms.CheckboxSelectMultiple(),
            "birth_date": forms.DateInput(
                attrs={"type": "date", "placeholder": "YYYY-MM-DD"}
            ),
        }

        labels = {
            "picture_original": "Picture of you",
        }

        help_texts = {
            "other_dietary_restrictions": "Please leave empty if no other restrictions.",
        }
