from django import forms
from django.contrib.auth.models import User
import re

from .models import Participant, InvitationGroup, Invitation


def fix_phone_number(n):
	if n is None: return None
	
	n = n.replace(' ', '')
	n = n.replace('-', '')
	
	if n.startswith("00"): n = "+" + n[2:]
	if n.startswith("0"): n = "+46" + n[1:]
	
	return n


class ParticipantForm(forms.ModelForm):
	def clean(self):
		super(ParticipantForm, self).clean()
		
		if 'phone_number' in self.cleaned_data:
			self.cleaned_data['phone_number'] = fix_phone_number(self.cleaned_data['phone_number'])
		
		return self.cleaned_data
	
	def is_valid(self):
		valid = super(ParticipantForm, self).is_valid()
		
		if not valid: return valid
		
		phone_number = self.cleaned_data.get('phone_number')
		
		if phone_number is not None and not re.match(r'\+[0-9]+$', phone_number):
			self.add_error('phone_number', 'Must only contain numbers and a leading plus.')
			valid = False
			
		return valid
	
	class Meta:
		model = Participant
		fields = ['name', 'email_address', 'phone_number', 'dietary_restrictions', 'alcohol']
		
		widgets = {
			'name' : forms.TextInput(attrs={'readonly':'readonly'}),
			'email_address' : forms.TextInput(attrs={'readonly':'readonly'}),
			'dietary_restrictions' : forms.CheckboxSelectMultiple(),
			'alcohol': forms.RadioSelect()
		}


class InvitationForm(forms.ModelForm):
	def clean(self):
		super(InvitationForm, self).clean()
		
		if 'phone_number' in self.cleaned_data:
			self.cleaned_data['phone_number'] = fix_phone_number(self.cleaned_data['phone_number'])
		
		return self.cleaned_data
	
	def is_valid(self):
		valid = super(InvitationForm, self).is_valid()
		
		if not valid: return valid
		
		user = self.cleaned_data.get('user')
		name = self.cleaned_data.get('name')
		email_address = self.cleaned_data.get('email_address')
		
		if user is not None:
			if name is not None:
				self.add_error('name', 'Leave this empty if you select a user.')
				valid = False
			
			if email_address is not None:
				self.add_error('email_address', 'Leave this empty if you select a user.')
				valid = False
		
		else:
			if name is None or len(name) == 0:
				self.add_error('name', 'Either select a user or provide a name.')
				valid = False
			
			if email_address is None or len(email_address) == 0:
				self.add_error('email_address', 'Either select a user or provide an e-mail address.')
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
		fields = ['group', 'user', 'name', 'email_address', 'reason', 'deadline', 'price']
		
		help_texts = {
			'reason': 'Not shown to the invitee.',
			'deadline': 'Leave blank to get the group\'s default deadline.',
			'price': 'Enter an integer price in SEK.'
		}


class InvitationSearchForm(forms.Form):
	status_choices = [
		('GOING', 'Going'),
		('NOT_GOING', 'Not going'),
		('PENDING', 'Pending')
	]
	
	statuses = forms.MultipleChoiceField(choices = status_choices, widget = forms.CheckboxSelectMultiple(), required = False)
	groups = forms.ModelMultipleChoiceField(queryset = InvitationGroup.objects.none(), widget = forms.CheckboxSelectMultiple(), label = 'Show only invitation belonging to any of these', required = False)


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
        exclude = ['banquet', 'company', 'user', 'seat']
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
