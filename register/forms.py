from django.forms import ModelForm, Form, BooleanField

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ValidationError

from sales.models import Sale
from companies.models import Company, Contact

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Email"

    def clean(self):
        self.cleaned_data['username'] = self.cleaned_data['username'].lower()
        super(LoginForm, self).clean()

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
    
    def clean(self):
        super(CompanyForm, self).clean()
        name = self.cleaned_data.get("name")
        if Company.objects.filter(name=name).first() != None:
            msg = "Company name already exists"
            self.add_error('name', msg)
            raise ValidationError(msg)


class ContactForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Full name"

    class Meta:
        model = Contact
        fields = '__all__'
        exclude = ('user','belongs_to','active', )

class RegistrationForm(Form):
    agreement_accepted = BooleanField(required=True)
    agreement_accepted.label = "I have read the contract and agree to terms"

class InterestForm(ModelForm):
    class Meta:
        model = Sale
        fields = ('diversity_room','green_room', 'events')
    

class CreateContactForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreateContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Full name"
        self.fields['belongs_to'].label = "Company"

    class Meta:
        model = Contact
        fields = '__all__'
        exclude = ('user', 'active',)

    def clean(self):
        self.cleaned_data['email'] = self.cleaned_data['email'].lower()
        super(CreateContactForm, self).clean()
        email = self.cleaned_data.get("email")
        if User.objects.filter(username=email).first() != None:
            msg = "Already existing account"
            self.add_error('email', msg)
            raise ValidationError("Account already exists")

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('password1','password2',)


