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
    'hosts', 'contact', 'fair_location',  'about_text', 'facts_text',
    'comment', 'status', 'logo', 'location_at_fair',
    'tags', 'job_types'
]

stand_fields = [
    'location', 'booth_number'
]


class ExhibitorFormFull(forms.ModelForm):
    '''
    The full version of the exhibitor form.
    '''

    field_order = exhibitor_fields + stand_fields 

    class Meta:
        model = Exhibitor
        fields = '__all__'
        exclude = ('company', 'fair', 'invoice_details', 'pickup_order', 'delivery_order') 



class ExhibitorFormPartial(ExhibitorFormFull):
    '''
    A basic version of exhibitor form (shown to users with partial permissions)

    Is a child of ExhibitorFormFull
    '''

    class Meta(ExhibitorFormFull.Meta):
        exclude = ('company', 'fair', 'hosts', 'contact', 'invoice_details','pickup_order', 'delivery_order')


