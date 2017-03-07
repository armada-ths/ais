from django.forms import ModelForm, Form, BooleanField

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ValidationError

from companies.models import Company, Contact

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Email"

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
        super(CreateContactForm, self).clean()
        email = self.cleaned_data.get("email")
        if User.objects.filter(username=email).first() != None:
            msg = "Already existing account"
            self.add_error('email', msg)
            raise ValidationError("Account already exists")

    def save(self, commit=True):
        ## Check if contact already exists without login
        ## and in that case only create a login for that contact 
        ## and edit info
        instance = super(CreateContactForm, self).save(commit=False)
        contact = Contact.objects.filter(email=self.cleaned_data['email']).first() # only one will exist
        print("form saving")
        if contact != None:
            #edit the contact
            print("updating contact", contact, self.cleaned_data)
            Contact.objects.filter(email=self.cleaned_data['email']).update(**self.cleaned_data)
            return Contact.objects.get(email=self.cleaned_data['email'])
        else:
            if commit:
                instance.save()
            return instance
        

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('password1','password2',)


