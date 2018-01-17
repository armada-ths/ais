from django.forms import Select,  Form, ModelChoiceField
from django import forms

from fair.models import Fair
from orders.models import Product, Order, ProductType, StandArea


class SelectStandAreaForm(Form):
    stand_area = forms.ModelChoiceField(queryset=StandArea.objects.filter(fair=Fair.objects.filter(current=True).first()))
    #def __init__(self, *args, **kwargs):
        #super(SelectStandArea, self).__init__(*args, **kwargs)
