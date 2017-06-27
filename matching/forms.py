from django.forms import ModelForm
from .models import ChoiceAns, TextAns, BooleanAns

class ChoiceAnsForm(ModelForm):
    class Meta:
        model = ChoiceAns
        exclude=('question',)
ChoiceAns.form = ChoiceAnsForm

class TextAnsForm(ModelForm):
    class Meta:
        model = TextAns
        exclude=('question',)
TextAns.form = TextAnsForm

class BooleanAnsForm(ModelForm):
    class Meta:
        model = BooleanAns
        exclude=('question',)
BooleanAns.form = BooleanAnsForm
