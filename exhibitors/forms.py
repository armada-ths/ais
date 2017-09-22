from django import forms

import inspect

from .models import ExhibitorView, Exhibitor

class ExhibitorViewForm(forms.Form):
    instance = None

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance')
        super(ExhibitorViewForm, self).__init__(*args, **kwargs)
        if not instance:
            instance = ExhibitorView()
            for item in ExhibitorView.default:
                instance.choices = instance.choices + ' ' + item

        for field in Exhibitor._meta.get_fields():
            print(field.name)
            if field.name not in ExhibitorView.ignore:
                self.fields[field.name] = forms.BooleanField(initial=(field.name in instance.choices), required=False)
