from django.forms import ModelForm, Form, BooleanField, ModelMultipleChoiceField, CheckboxSelectMultiple, ValidationError, IntegerField
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from fair.models import Fair
from orders.models import Product, Order, ProductType
from sales.models import Sale
from exhibitors.models import Exhibitor
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
        exclude = ('user','belongs_to','active','confirmed' )

class RegistrationForm(Form):
    agreement_accepted = BooleanField(required=True)
    agreement_accepted.label = "I have read the contract and agree to terms"

class InterestForm(ModelForm):
    class Meta:
        model = Sale
        fields = ('diversity_room','green_room', 'events', 'nova')
        labels = {
            "diversity_room": _("Interested in diversity room"),
            "green_room": _("Interested in green room"),
            "events": _("Interested in having events"),
            "nova": ("Interested in Nova")
        }
        #help_texts = {
        #    "diversity_room": _("Tick this if you are interested in our diversity room concept"),
        #}


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

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('password1','password2',)


class ExhibitorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # products that can be chosen with an amount
        banquet = kwargs.pop('banquet')
        lunch = kwargs.pop('lunch')

        super(ExhibitorForm, self).__init__(*args, **kwargs)

        # create form fields for the banquet and lunch products
        for i, banq in enumerate(banquet):
            self.fields['banquet_%s' % banq.name] = IntegerField()
        for i, lun in enumerate(lunch):
            self.fields['lunch_%s' % lun.name] = IntegerField()

    class ProductMultiChoiceField(ModelMultipleChoiceField):
        def label_from_instance(self, product):
            return mark_safe('%s<br/>%s' % (product.name, product.description))

    # Products in the forms different tabs
    product_selection_rooms = ProductMultiChoiceField(queryset=Product.objects.filter(fair=Fair.objects.get(current = True), product_type=ProductType.objects.filter(name="Rooms")), required=False,widget=CheckboxSelectMultiple())
    product_selection_events = ProductMultiChoiceField(queryset=Product.objects.filter(fair=Fair.objects.get(current = True), product_type=ProductType.objects.filter(name="Events")), required=False,widget=CheckboxSelectMultiple())
    product_selection_nova = ProductMultiChoiceField(queryset=Product.objects.filter(fair=Fair.objects.get(current = True), product_type=ProductType.objects.filter(name="Nova")), required=False,widget=CheckboxSelectMultiple())
    product_selection_additional_stand_area = ProductMultiChoiceField(queryset=Product.objects.filter(fair=Fair.objects.get(current = True), product_type=ProductType.objects.filter(name="Additional Stand Area")), required=False,widget=CheckboxSelectMultiple())
    product_selection_additional_stand_height = ProductMultiChoiceField(queryset=Product.objects.filter(fair=Fair.objects.get(current = True), product_type=ProductType.objects.filter(name="Additional Stand Height")), required=False,widget=CheckboxSelectMultiple())
    product_selection_additional_lunch_tickets = ProductMultiChoiceField(queryset=Product.objects.filter(fair=Fair.objects.get(current = True), product_type=ProductType.objects.filter(name="Additional Lunch Tickets")), required=False,widget=CheckboxSelectMultiple())

    class Meta:
        model = Exhibitor
        fields = '__all__'
        exclude = ('fair','contact','company', 'status', 'hosts', 'location', 'fair_location', 'wants_information_about_osqledaren')

    def clean(self):
        super(ExhibitorForm, self).clean()

    # Returns a generator/iterator with all banquet product field names and the chosen amount
    def banquet_products(self):
        for name, amount in self.cleaned_data.items():
            if name.startswith('banquet_'):
                yield (self.fields[name].label[index("_")+1:], amount)
    # Returns a generator/iterator with all lunch product field names and the chosen amount
    def lunch_products(self):
        for name, amount in self.cleaned_data.items():
            if name.startswith('lunch_'):
                yield (self.fields[name].label[index("_")+1:], amount)
