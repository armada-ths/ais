from django import forms
from django.forms import ModelForm, Form, ModelMultipleChoiceField, ModelChoiceField, ChoiceField
from django.contrib.auth.models import User
import re

from .models import Participant, InvitationGroup, Invitation, AfterPartyInvitation, AfterPartyTicket, TableMatching, MatchingProgram, MatchingInterest, MatchingYear
from exhibitors.models import CatalogueIndustry, CatalogueCompetence, CatalogueValue, CatalogueLocation, CatalogueEmployment, CatalogueCategory


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
			self.cleaned_data['phone_number'] = fix_phone_number(
			    self.cleaned_data['phone_number'])

		return self.cleaned_data

	def is_valid(self):
		valid = super(ParticipantForm, self).is_valid()

		if not valid: return valid

		phone_number = self.cleaned_data.get('phone_number')

		if phone_number is not None and not re.match(r'\+[0-9]+$', phone_number):
			self.add_error(
			    'phone_number', 'Must only contain numbers and a leading plus.')
			valid = False

		return valid

	class Meta:
		model = Participant
		fields = ['name', 'email_address', 'phone_number',
		    'dietary_restrictions', 'other_dietary_restrictions', 'alcohol']

		widgets = {
			'name': forms.TextInput(attrs={'readonly': 'readonly'}),
			'email_address': forms.TextInput(attrs={'readonly': 'readonly'}),
			'dietary_restrictions': forms.CheckboxSelectMultiple(),
			'other_dietary_restrictions': forms.TextInput(),
			'alcohol': forms.RadioSelect()
		}

		help_texts = {
			'other_dietary_restrictions': 'Please leave empty if no other restrictions.',
		}


class ParticipantAdminForm(forms.ModelForm):
	def clean(self):
		super(ParticipantAdminForm, self).clean()

		if 'phone_number' in self.cleaned_data:
			self.cleaned_data['phone_number'] = fix_phone_number(
			    self.cleaned_data['phone_number'])

		return self.cleaned_data

	def is_valid(self):
		valid = super(ParticipantAdminForm, self).is_valid()

		if not valid: return valid

		company = self.cleaned_data.get('company')
		user = self.cleaned_data.get('user')
		name = self.cleaned_data.get('name')
		email_address = self.cleaned_data.get('email_address')
		phone_number = self.cleaned_data.get('phone_number')

		if company is not None and user is not None:
			self.add_error('company', 'Cannot have both a company and a user.')
			self.add_error('user', 'Cannot have both a company and a user.')
			valid = False

		if phone_number is not None and not re.match(r'\+[0-9]+$', phone_number):
			self.add_error(
			    'phone_number', 'Must only contain numbers and a leading plus.')
			valid = False

		if user is not None and name is not None:
			self.add_error('name', 'Must be empty if a user is selected.')
			valid = False

		if user is not None and email_address is not None:
			self.add_error('email_address', 'Must be empty if a user is selected.')
			valid = False

		if user is None and name is None:
			self.add_error('name', 'Must be given if no user is selected.')
			valid = False

		if user is None and email_address is None:
			self.add_error('email_address', 'Must be given if no user is selected.')
			valid = False

		return valid

	class Meta:
		model = Participant
		fields = ['seat', 'company', 'user', 'name', 'email_address', 'phone_number',
		    'dietary_restrictions', 'other_dietary_restrictions', 'alcohol', 'giveaway']

		help_texts = {
			'name': 'Only enter a name if you do not select a user.',
			'email_address': 'Only enter an e-mail address if you do not select a user.',
			'giveaway': 'Only applies to company tickets, default should be No for all other tickets.',
		}

		labels = {
			'giveaway': 'The company plan to give this ticket to a student',
		}

		widgets = {
			'dietary_restrictions': forms.CheckboxSelectMultiple(),
			'other_dietary_restrictions': forms.TextInput(),
			'alcohol': forms.RadioSelect(),
			'giveaway': forms.RadioSelect(),
		}


class InvitationForm(forms.ModelForm):
	def clean(self):
		super(InvitationForm, self).clean()

		if 'phone_number' in self.cleaned_data:
			self.cleaned_data['phone_number'] = fix_phone_number(
			    self.cleaned_data['phone_number'])

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
				self.add_error('email_address',
				               'Either select a user or provide an e-mail address.')
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
		fields = ['group', 'user', 'name', 'email_address',
		    'reason', 'deadline', 'price', 'part_of_matching']

		help_texts = {
			'reason': 'Not shown to the invitee.',
			'deadline': 'Leave blank to get the group\'s default deadline.',
			'price': 'Enter an integer price in SEK.',
			'part_of_matching': "This person is subject to the banquet placement matching functionality."
		}

		widgets = {
			'deadline': forms.DateInput(attrs={'type': 'date'})
		}


class InvitationSearchForm(forms.Form):
	status_choices = [
		('GOING', 'Going'),
		('HAS_NOT_PAID', 'Has not paid'),
		('NOT_GOING', 'Not going'),
		('PENDING', 'Pending')
	]

	matching_status_choices = [
		(None, 'Any'),
		(True, 'Part of matching'),
		(False, 'Not part of matching')
	]

	statuses = forms.MultipleChoiceField(
	    choices=status_choices, widget=forms.CheckboxSelectMultiple(), required=False)
	groups = forms.ModelMultipleChoiceField(queryset=InvitationGroup.objects.none(), widget=forms.CheckboxSelectMultiple(
	), label='Show only invitations belonging to any of these groups', required=False)
	matching_statuses = forms.ChoiceField(choices=matching_status_choices, widget=forms.RadioSelect(
	), label='Show only invitations that are / are not subject to the matching functionality', required=False)


class AfterPartyInvitationForm(forms.ModelForm):
	class Meta:
		model = AfterPartyInvitation
		fields = ['name', 'email_address']

		labels = {
			'name': "Friend's full name",
			'email_address': "Friend's email address"
		}


class AfterPartyTicketForm(forms.ModelForm):
	class Meta:
		model = AfterPartyTicket
		fields = ['name', 'email_address', 'inviter']

		labels = {
			'name': 'Your full name',
			'inviter': 'Did someone in Armada recommend you about this after party? Write first name and last name.'
		}


class InternalParticipantForm(forms.ModelForm):
    """
    Form for internal users to register for the banquet
    certain fields are disabled as they are prefilled in view
    """
    class Meta:
        model = Participant
        # Is still something we send back in view but handled without user input
        exclude = ['banquet', 'company', 'user']

        widgets = {
            'name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'email_address': forms.TextInput(attrs={'readonly': 'readonly'}),
            'phone_number': forms.TextInput(attrs={'readonly': 'readonly'}),
            'dietary_restrictions': forms.CheckboxSelectMultiple(),
            'other_dietary_restrictions': forms.TextInput(),
            'alcohol': forms.RadioSelect()
        }

        help_texts = {
            'other_dietary_restrictions': 'Please leave empty if no other restrictions.',
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
        queryset = MatchingProgram.objects.filter(include_in_form = True),
        widget = forms.RadioSelect, 
        label = 'What are you studying?',
        required = False)

    matching_interests = IncludeCategoryChoiceFieldMultiple(
        queryset = MatchingInterest.objects.filter(include_in_form = True),
        widget = forms.CheckboxSelectMultiple,
        label = 'What are your interests?',
        required = False)

    matching_year = IncludeCategoryChoiceFieldSingle(
        queryset = MatchingYear.objects.filter(include_in_form = True),
        widget = forms.RadioSelect,
        label = 'What year will you graduate?',
        required = False)

    class Meta:
        model = TableMatching
        fields = ['matching_program', 'matching_interests', 'matching_year']


#Previous implementation of the MatchingForm
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
        exclude = ['banquet', 'company', 'user', 'seat']
        widgets = {
            'name' : forms.TextInput(attrs={'readonly':'readonly'}),
            'email_address' : forms.TextInput(attrs={'readonly':'readonly'}),
            'dietary_restrictions' : forms.CheckboxSelectMultiple(),
            'dietary_restictions_other' : forms.TextInput(),
            'alcohol' : forms.RadioSelect()
        }

class SendInvitationForm(forms.ModelForm):
	"""
	Banquet administrator sends out invite
	"""
	def __init__(self, *args, **kwargs):
		# would like to do as in conact list however I can't get user object in that case
		# but this works also although not pretty
		super(SendInvitationForm, self).__init__(*args, **kwargs)
		self.fields['user'].queryset = User.objects.exclude(groups__isnull=True).order_by('last_name')

	class Meta:
		model = Invitation
		exclude = ['banquet', 'participant', 'denied','token']
