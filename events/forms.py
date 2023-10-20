from django import forms
from django.forms import ModelForm, TextInput
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

from events.models import Event, SignupQuestionAnswerFile, Team


# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_UPLOAD_SIZE = 10485760  # 10MB
CONTENT_TYPES = ["png", "pdf"]


class SignupQuestionAnswerFileForm(ModelForm):
    def clean_file(self):
        content = self.cleaned_data["file"]
        content_type = content.content_type.split("/")[1]

        if content_type in CONTENT_TYPES:
            if content.size > MAX_UPLOAD_SIZE:
                raise forms.ValidationError(
                    _("Please keep filesize under %s. Current filesize %s")
                    % (filesizeformat(MAX_UPLOAD_SIZE), filesizeformat(content.size))
                )
        else:
            raise forms.ValidationError(
                _(
                    "File type is not supported, supported types: %s"
                    % ", ".join(CONTENT_TYPES)
                )
            )
        return content

    class Meta:
        model = SignupQuestionAnswerFile
        fields = ["file"]


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = "__all__"

        widgets = {
            "date_start": TextInput(attrs={"placeholder": "1994-07-12 13:37:00"}),
            "date_end": TextInput(attrs={"placeholder": "1995-10-10 13:37:00"}),
        }


class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ["name", "max_capacity", "allow_join_cr", "allow_join_s"]
