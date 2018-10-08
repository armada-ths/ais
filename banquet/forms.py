from django import forms
from .models import Participant, Invitation

from django.contrib.auth.models import User

from recruitment.models import RecruitmentApplication
from django.forms import modelformset_factory

class InternalParticipantForm(forms.ModelForm):
    """
    Form for internal users to register for the banquet
    certain fields are disabled as they are prefilled in view
    """
    class Meta:
        model = Participant
        # Is still something we send back in view but handled without user input
        exclude = ['banquet','company','user']

        widgets = {
            'name' : forms.TextInput(attrs={'readonly':'readonly'}),
            'email_address' : forms.TextInput(attrs={'readonly':'readonly'}),
            'phone_number' : forms.TextInput(attrs={'readonly':'readonly'}),
            'dietary_restrictions' : forms.CheckboxSelectMultiple(),
            'alcohol' : forms.RadioSelect()
        }


class ExternalParticipantForm(forms.ModelForm):
    """
    External participant fills in personal info (invitation page)
    """
    class Meta:
        model = Participant
        exclude = ['banquet','company','user']
        widgets = {
            'name' : forms.TextInput(attrs={'readonly':'readonly'}),
            'email_address' : forms.TextInput(attrs={'readonly':'readonly'}),
            'dietary_restrictions' : forms.CheckboxSelectMultiple(),
            'alcohol' : forms.RadioSelect()
        }

class SendInvitationForm(forms.ModelForm):
    """
    Banquet administrator sends out invite
    """
    def __init__(self, *args, **kwargs):
        ## would like to do as in conact list however I can't get user object in that case
        ## but this works also although not pretty
        super(SendInvitationForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.exclude(groups__isnull=True).order_by('last_name')

    class Meta:
        model = Invitation
        exclude = ['banquet', 'participant', 'denied','token']
