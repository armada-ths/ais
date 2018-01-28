from django import forms

import inspect

from .models import ExhibitorView, Exhibitor, TransportationAlternative
from companies.models import InvoiceDetails

class TransportationForm(forms.ModelForm):
    class Meta:
        model = Exhibitor
        fields = ('inbound_transportation', 'outbound_transportation')

    def __init__(self, *args, **kwargs):
        super(TransportationForm, self).__init__(*args, **kwargs)
        self.fields['inbound_transportation'].queryset = TransportationAlternative.objects.filter(inbound=True)
        self.fields['outbound_transportation'].queryset = TransportationAlternative.objects.filter(inbound=False)


class SelectInvoiceDetailsForm(forms.ModelForm):
    class Meta:
        model = Exhibitor
        fields = ('invoice_details',)

    def __init__(self, exhibitor, *args, **kwargs):
        super(SelectInvoiceDetailsForm, self).__init__(*args, **kwargs)
        self.fields['invoice_details'].queryset = InvoiceDetails.objects.filter(company=exhibitor.company)

class ExhibitorProfileForm(forms.ModelForm):
    class Meta:
        model = Exhibitor
        fields = ('logo', 'about_text','job_types')

class ExhibitorViewForm(forms.Form):
    instance = None


    def __init__(self, *args, **kwargs):
        self.instance = kwargs.setdefault('instance', None)
        user = kwargs.setdefault('user', None)
        kwargs.pop('instance')
        kwargs.pop('user')
        super(ExhibitorViewForm, self).__init__(*args, **kwargs)
        if not self.instance:
            if not user:
                raise Exception('No user or instance supplied to ExhibitorViewForm')
            self.instance = ExhibitorView(user=user)

        for field in Exhibitor._meta.get_fields():
            if field.name not in ExhibitorView.ignore:
                self.fields[field.name] = forms.BooleanField(initial=(field.name in self.instance.choices), required=False)


    def save(self, commit=True):
        #instance = super(ExhibitorViewForm, self).save(commit=False)   # it might be important to call a super.save(), but it seems to work just fine anyway
        saved_fields = ''

        for name, field in self.cleaned_data.items():
            if field:
                saved_fields += ' ' + name

        self.instance.choices = saved_fields
        if commit:
            self.instance.save()
        return self.instance


# Fields for ordering
exhibitor_fields = [
    'hosts', 'contact', 'fair_location', 'estimated_arrival_of_representatives', 'about_text', 'facts_text',
    'accept_terms', 'comment', 'status', 'allergies', 'logo', 'location_at_fair', 'requests_for_exhibition_area',
    'number_of_outlets_needed', 'total_power', 
    'wants_information_about_events', 'wants_information_about_targeted_marketing', 'wants_information_about_osqledaren',
    'manual_invoice', 'interested_in_armada_transport', 'tags', 'goals_of_participation', 'job_types'
]
transport_to_fair_fields = [
    'transport_to_fair_type', 'number_of_packages_to_fair', 'number_of_pallets_to_fair', 'estimated_arrival'
]
transport_from_fair_fields = [
    'transport_from_fair_type', 'number_of_packages_from_fair', 'number_of_pallets_from_fair'
]
armada_transport_from_fair_fields = [
    'transport_from_fair_address', 'transport_from_fair_zip_code', 'transport_from_fair_recipient_name',
    'transport_from_fair_recipient_phone_number'
]
stand_fields = [
    'location', 'booth_number', 'requests_for_stand_placement', 'heavy_duty_electric_equipment', 'other_information_about_the_stand'
]


class ExhibitorFormFull(forms.ModelForm):
    '''
    The full version of the exhibitor form.
    '''

    field_order = exhibitor_fields + stand_fields + transport_to_fair_fields + transport_from_fair_fields + armada_transport_from_fair_fields

    class Meta:
        model = Exhibitor
        fields = '__all__'
        exclude = ('company', 'fair') 
        widgets = {
            'allergies' : forms.TextInput()
        }
        labels = {
            'estimated_arrival_of_representatives' : 'Estimated arrival of representatives (format: 2016-12-24 13:37)',
            'estimated_arrival' : 'Estimaded arrival (format: 2016-12-24 13:37)'
        }


    def clean(self):
        data = super(ExhibitorFormFull, self).clean()
        if data['status'] == 'checked_out':
            errors = []
            for field in transport_from_fair_fields:
                if data[field] is None:
                    error_text = '\"' + Exhibitor._meta.get_field(field).verbose_name.capitalize() + '\" field is required before checkout!'
                    errors.append(forms.ValidationError(error_text, code='invalid'))
            if data['transport_from_fair_type'] == 'armada_transport':
                for field in armada_transport_from_fair_fields:
                    if data[field] == '':
                        error_text = '\"' + Exhibitor._meta.get_field(field).verbose_name.capitalize() + '\" field is required before checkout!'
                        errors.append(forms.ValidationError(error_text, code='invalid'))
            if len(errors) != 0:
                raise forms.ValidationError(errors)
        return data


class ExhibitorFormPartial(ExhibitorFormFull):
    '''
    A basic version of exhibitor form (shown to users with partial permissions)

    Is a child of ExhibitorFormFull
    '''

    class Meta(ExhibitorFormFull.Meta):
        exclude = ('company', 'fair', 'hosts', 'contact')


