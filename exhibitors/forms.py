from django import forms

import inspect

from companies.models import Company, CompanyCustomerComment
from .models import ExhibitorView, Exhibitor

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
exhibitor_fields = ['hosts']
stand_fields = ['location', 'booth_number']


class ExhibitorFormFull(forms.ModelForm):
    '''
    The full version of the exhibitor form.
    '''

    field_order = exhibitor_fields + stand_fields 

    class Meta:
        model = Exhibitor
        fields = '__all__'
        exclude = ('company', 'fair', 'pickup_order', 'delivery_order') 



class ExhibitorFormPartial(ExhibitorFormFull):
    '''
    A basic version of exhibitor form (shown to users with partial permissions)

    Is a child of ExhibitorFormFull
    '''

    class Meta(ExhibitorFormFull.Meta):
        exclude = ('company', 'fair', 'hosts', 'contact', 'pickup_order', 'delivery_order')

class ExhibitorCreateForm(forms.Form):
	companies = forms.ModelMultipleChoiceField(
		queryset = Company.objects.all(),
		widget = forms.SelectMultiple(attrs = {"size": 20}),
		required = True,
		label = "Companies from the initial registration"
	)


class TransportForm(forms.ModelForm):
	class Meta:
		model = Exhibitor
		fields = ['transport_to', 'transport_from', 'transport_comment']


class CommentForm(forms.ModelForm):
	class Meta:
		model = CompanyCustomerComment
		fields = ['comment']
