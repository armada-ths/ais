from django.forms import Select, ModelForm, Form, BooleanField, ModelMultipleChoiceField, CheckboxSelectMultiple, RadioSelect, ValidationError, IntegerField, CharField, ChoiceField
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe, format_html

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
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
        events = kwargs.pop('events')
        rooms = kwargs.pop('rooms')
        nova = kwargs.pop('nova')
        stand_area = kwargs.pop('stand_area')
        stand_height = kwargs.pop('stand_height')

        # current exhibitor's orders
        banquet_orders = kwargs.pop('banquet_orders')
        lunch_orders = kwargs.pop('lunch_orders')
        event_orders = kwargs.pop('event_orders')
        room_orders = kwargs.pop('room_orders')
        nova_orders = kwargs.pop('nova_orders')
        stand_area_orders = kwargs.pop('stand_area_orders')
        stand_height_orders = kwargs.pop('stand_height_orders')

        # company and contact for last tab
        company = kwargs.pop('company')
        contact = kwargs.pop('contact')

        super(ExhibitorForm, self).__init__(*args, **kwargs)

        # create multiselect fields for rooms, nova and additional stand and height area.
        self.products_as_multi_field(rooms, 'product_selection_rooms', CheckboxSelectMultiple())
        self.products_as_multi_field(nova, 'product_selection_nova', CheckboxSelectMultiple())
        self.products_as_multi_field(stand_height, 'product_selection_additional_stand_height', RadioSelect())
        self.products_as_multi_field(stand_area, 'product_selection_additional_stand_area', Select())

        # create form fields for the banquet, lunch and event products
        self.products_as_int_field(banquet, "banquet_")
        self.products_as_int_field(events, "event_")
        self.products_as_number_choice_field(lunch, "lunch_", 11)

        # Create fields for save and confirm tab
        self.init_company_fields(company)
        self.init_contact_fields(contact)

    # Fields for company in save and confirm tab
    def init_company_fields(self, company):
        self.fields['name_of_organisation'] = CharField(initial=company.name)
        self.fields['organisation_identification_number'] = CharField(initial=company.organisation_number)
        organisation_types = [
            ('company', 'Company'),
            ('county_council', 'County/County council'),
            ('government_agency', 'Government agency'),
            ('non_profit_organisation', 'Non-profit organisation'),
            ('union', 'Union'),
        ]
        self.fields['type_of_organisation'] = ChoiceField(choices=organisation_types,initial=company.organisation_type)
        self.fields['address_street'] = CharField(initial=company.address_street)
        self.fields['address_zip_code'] = CharField(initial=company.address_zip_code)
        self.fields['address_city'] = CharField(initial=company.address_city)
        self.fields['address_country'] = CharField(initial=company.address_country)
        self.fields['additional_address_information'] = CharField(initial=company.additional_address_information)
        self.fields['website'] = CharField(initial=company.website)

    class Meta:
        model = Exhibitor
        fields = '__all__'
        exclude = ('fair','contact','company', 'status', 'hosts', 'location', 'fair_location', 'wants_information_about_osqledaren')

    # Fields for contact in save and confirm tab
    def init_contact_fields(self, contact):
        self.fields['contact_name'] = CharField(initial=contact.name)
        self.fields['work_phone'] = CharField(initial=contact.work_phone)
        self.fields['cell_phone'] = CharField(initial=contact.cell_phone)
        self.fields['phone_switchboard'] = CharField(initial=contact.phone_switchboard)
        self.fields['contact_email'] = CharField(initial=contact.email)
        self.fields['alternative_email'] = CharField(initial=contact.alternative_email)

    # An IntegerField with a relation to a product object
    class ProductIntegerField(IntegerField):
        def __init__(self, object, prefix, *args, **kwargs):
            IntegerField.__init__(self, *args, **kwargs)
            self.label = object.name
            self.help_text = prefix
            self.description = object.description
            self.object = object

    # A modelmultiplechoicefield with a customized label for each instance
    class ProductMultiChoiceField(ModelMultipleChoiceField):
        def label_from_instance(self, product):
            #return mark_safe('%s<br/>%s' % (product.name, product.description))
            return format_html("<span class='btn btn-armada-checkbox product-label'>{}</span> <span class='product-description'>{}</span>",
                        mark_safe(product.name),
                        mark_safe(product.description),
                    )

    # Takes some objects and makes a productintegerfield for each one.
    # The field name will be the object's name with the 'prefix_' as a prefix
    # The field label will the object's name and the help_text its prefix
    # to help you find it in the template.
    # The initial amount will be set if an order related to the product exists.
    # Otherwise it will be 0.
    def products_as_int_field(self, objects, prefix):
        for i, object in enumerate(objects):
            self.fields['%s%s' % (prefix, object.name)] = self.ProductIntegerField(object, prefix, initial=0, min_value=0)

    # Takes some objects and makes a choicefield for each one.
    # The field name will be the object's name with the 'prefix_' as a prefix
    # The field label will the object's name and the help_text its prefix
    # to help you find it in the template
    def products_as_number_choice_field(self, objects, prefix, num):
        for i, object in enumerate(objects):
            self.fields['%s%s' % (prefix, object.name)] = ChoiceField(choices=[(x, x) for x in range(0, 11)])
            self.fields['%s%s' % (prefix, object.name)].label = object.name
            self.fields['%s%s' % (prefix, object.name)].help_text = prefix

    # Takes some objects and makes a choicefield for each one.
    # The field name will be the object's name with the 'prefix_' as a prefix
    # The field label will the object's name and the help_text its prefix
    # to help you find it in the template



    # Takes some objects and puts them in a ProductMultiChoiceField.
    # The field name will be named by the fieldname argument.
    # A products will be checked if they exist in an order for the current exhibitor
    def products_as_multi_field(self, objects, fieldname, widget):
        self.fields[fieldname] = self.ProductMultiChoiceField(queryset=objects, required=False, widget=widget)

    # Returns a generator/iterator with all product fields where you choose an amount.
    # Choose a prefix to get which the correct type, e.g 'banquet_', or 'event_'.
    # Make sure they are the same as the ones in the form's constructor!
    def amount_products(self, prefix):
        for name, amount in self.cleaned_data.items():
            if name.startswith(prefix):
                yield(self.fields[name].object, amount)

    def save_or_submit(self):
        if 'submit' in self.data:
            return 'submit'
        elif 'save' in self.data:
            return 'save'

    def clean(self):
        super(ExhibitorForm, self).clean()