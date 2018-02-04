from django import forms
from .models import TransportationOrder

class PickupForm(forms.ModelForm):
    class Meta:
        model = TransportationOrder
        fields = '__all__'
        exclude = ('delivery_street_address', 'delivery_zip_code', 'delivery_city')

    def is_valid(self):
        valid = super(PickupForm, self).is_valid()
        if not valid:
            return valid

        error_message = 'If you use our transport services you need to fill out all transportation information'

        if len(self.cleaned_data['pickup_street_address']) == 0:
            self.add_error(None, error_message)
            return False

        if len(self.cleaned_data['pickup_zip_code']) == 0:
            self.add_error(None, error_message)
            return False

        if len(self.cleaned_data['contact_name']) == 0:
            self.add_error(None, error_message)
            return False

        if len(self.cleaned_data['contact_phone_number']) == 0:
            self.add_error(None, error_message)
            return False


        return valid

class DeliveryForm(forms.ModelForm):
    class Meta:
        model = TransportationOrder
        fields = '__all__'
        exclude = ('pickup_street_address', 'pickup_zip_code', 'pickup_city')


    def is_valid(self):
        valid = super(DeliveryForm, self).is_valid()
        if not valid:
            return valid

        error_message = 'If you use our transport services you need to fill out all transportation information'

        if len(self.cleaned_data['delivery_street_address']) == 0:
            self.add_error(None, error_message)
            return False

        if len(self.cleaned_data['delivery_zip_code']) == 0:
            self.add_error(None, error_message)
            return False

        if len(self.cleaned_data['contact_name']) == 0:
            self.add_error(None, error_message)
            return False

        if len(self.cleaned_data['contact_phone_number']) == 0:
            self.add_error(None, error_message)
            return False

        return valid

