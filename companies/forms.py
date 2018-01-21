from django.forms import ModelForm, HiddenInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Company, Contact, InvoiceDetails


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

class EditCompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = '__all__'



class ContactForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Full name"

    class Meta:
        model = Contact
        fields = '__all__'
        exclude = ('user','belongs_to','active','confirmed' )

class InvoiceDetailsForm(ModelForm):

    class Meta:
        model = InvoiceDetails
        fields = '__all__'

    def __init__(self, company, *args, **kwargs):
        instance = kwargs.get('instance')
        super(InvoiceDetailsForm, self).__init__(*args, **kwargs)
        if instance == None:
            self.initial['company'] =  Company.objects.filter(id=company.pk).first().id
        self.fields['company'].disabled = True #make sure company field is not editable
        self.fields['company'].widget= HiddenInput()



class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['password1', 'password2']


class CreateContactForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreateContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Full name"
        self.fields['belongs_to'].label = "Company"

    class Meta:
        model = Contact
        fields = '__all__'
        exclude = ('user', 'active','confirmed')

    def clean(self):
        self.cleaned_data['email'] = self.cleaned_data['email'].lower()
        super(CreateContactForm, self).clean()
        email = self.cleaned_data.get("email")
        if User.objects.filter(username=email).first() != None:
            msg = "Already existing account"
            self.add_error('email', msg)
            raise ValidationError("Account already exists")

class CreateContactNoCompanyForm(CreateContactForm):

    def __init__(self, *args, **kwargs):
        super(CreateContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Full name"

    class Meta:
        model = Contact
        fields = '__all__'
        exclude = ('user', 'active', 'confirmed', 'belongs_to')
