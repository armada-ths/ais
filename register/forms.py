from django.forms import TextInput, Select, RadioSelect, ModelForm, Form, BooleanField, ModelMultipleChoiceField, CheckboxSelectMultiple, ValidationError, IntegerField, CharField, ChoiceField
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe, format_html
from django import forms

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User

from fair.models import Fair
from orders.models import Product, Order, ProductType
from sales.models import Sale
from exhibitors.models import Exhibitor, CatalogInfo
from companies.models import Company, Contact

from enum import Enum

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = ""
        self.fields['password'].label = ""
        self.fields['username'].widget = forms.TextInput(attrs={'class' : 'input', 'placeholder' : 'Email'})
        self.fields['password'].widget = forms.TextInput(attrs={'class' : 'input', 'placeholder' : 'Password', 'type' : 'password'})

    def clean(self):
        self.cleaned_data['username'] = self.cleaned_data['username'].lower()
        super(LoginForm, self).clean()


class ResetPasswordForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = ""
        self.fields['email'].widget = forms.TextInput(attrs={'class' : 'input', 'placeholder' : 'Email'})

class SetNewPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(SetNewPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].label = ""
        self.fields['new_password2'].label = ""
        self.fields['new_password1'].widget = forms.TextInput(attrs={'class' : 'input', 'placeholder' : 'New Password', 'type' : 'password'})
        self.fields['new_password2'].widget = forms.TextInput(attrs={'class' : 'input', 'placeholder' : 'New Password Confirmation', 'type' : 'password'})

class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = ""
        self.fields['new_password1'].label = ""
        self.fields['new_password2'].label = ""
        self.fields['old_password'].widget = forms.TextInput(attrs={'class' : 'input', 'placeholder' : 'Old Password', 'type' : 'password'})
        self.fields['new_password1'].widget = forms.TextInput(attrs={'class' : 'input', 'placeholder' : 'New Password', 'type' : 'password'})
        self.fields['new_password2'].widget = forms.TextInput(attrs={'class' : 'input', 'placeholder' : 'New Password Confirmation', 'type' : 'password'})


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

class ExhibitorCatalogInfoForm(ModelForm):
    class Meta:
        model = CatalogInfo 
        fields = '__all__'
        exclude = ('exhibitor', 'programs', 'main_work_field', 'work_fields', 'continents', 'tags')
        widgets = {}   

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
        self.products_as_multi_field(rooms, 'product_selection_rooms', room_orders)
        self.products_as_multi_field(nova, 'product_selection_nova', nova_orders)
        self.products_as_select_field(stand_area, 'product_selection_additional_stand_area', stand_area_orders, "Select")
        self.products_as_select_field(stand_height, 'product_selection_additional_stand_height', stand_height_orders, "Select")

        # create form fields for the banquet, lunch and event products
        self.products_as_int_field(banquet, "banquet_", banquet_orders)
        self.products_as_int_field(lunch, "lunch_", lunch_orders)
        self.products_as_int_field(events, "event_", event_orders)

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
        self.fields['additional_address_information'] = CharField(initial=company.additional_address_information, required=False)
        self.fields['website'] = CharField(initial=company.website, required=False)


    class Meta:
        model = Exhibitor
        fields = '__all__'
        exclude = ('fair','contact','company', 'status', 'hosts', 'location', 'fair_location', 'wants_information_about_osqledaren')
        widgets = {
            'invoice_address': TextInput(attrs={'placeholder': 'Address'}),
            'invoice_address_po_box': TextInput(attrs={'placeholder': 'Address/PO-box'}),
            'invoice_address_zip_code': TextInput(attrs={'placeholder': 'Zip code'}),
            'transport_from_fair_address': TextInput(attrs={'placeholder': 'Address'}),
            'allergies': TextInput(),
        }

    # Fields for contact in save and confirm tab
    def init_contact_fields(self, contact):
        self.fields['contact_name'] = CharField(initial=contact.name)
        self.fields['work_phone'] = CharField(initial=contact.work_phone)
        self.fields['cell_phone'] = CharField(initial=contact.cell_phone, required=False)
        self.fields['phone_switchboard'] = CharField(initial=contact.phone_switchboard, required=False)
        self.fields['contact_email'] = CharField(initial=contact.email)
        self.fields['alternative_email'] = CharField(initial=contact.alternative_email, required=False)

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
    def products_as_int_field(self, products, prefix, orders):
        # Map the ordered products to its ordered amount.
        # Will be O(1) when looking if a product is ordered and getting its amount
        # instead of looping through all orders again with O(n), n = number of orders.
        orderedProductsAmountDict = dict()
        for order in orders:
            orderedProductsAmountDict[order.product.__hash__] = order.amount

        for i, product in enumerate(products):
            amount = 0
            try:
                amount = orderedProductsAmountDict[product.__hash__]
            except KeyError:
                pass
            product_name_underscores = product.name.replace(" ", "_")
            product_name_underscores = product_name_underscores.replace("/", "")
            product_name_underscores = product_name_underscores.replace("-", "")
            product_name_underscores = product_name_underscores.replace(",", "")
            product_name_underscores = product_name_underscores.lower()
            self.fields['%s%s' % (prefix, product_name_underscores)] = self.ProductIntegerField(product, prefix, initial=amount, min_value=0)

    # A modelmultiplechoicefield with a customized label for each instance
    class RoomMultiChoiceField(ModelMultipleChoiceField):
        def label_from_instance(self, product):
            return format_html("<h3 class='product-label'>{}</h3> <p class='product-description'>{}</p> <p class='confirm-title'>{}</p> <h4 class='room-price'>10 000 SEK</h4>",
                        mark_safe(product.name),
                        mark_safe(product.description),
                        mark_safe("We want to apply for this area"),
                    )

    # A modelmultiplechoicefield with a customized label for each instance
    class NovaMultiChoiceField(ModelMultipleChoiceField):
        def label_from_instance(self, product):
            return format_html("<h3 class='product-label'>{}</h3> <h4 class='product-description'><span class='h-white'>{}</span></h4> <h4 class='confirm-title'>{}</h4>",
                        mark_safe(product.name),
                        mark_safe(product.description),
                        mark_safe("We want this"),
                    )

    # Takes some objects and makes a choicefield for each one.
    # The field name will be the object's name with the 'prefix_' as a prefix
    # The field label will the object's name and the help_text its prefix
    # to help you find it in the template
    def products_as_number_choice_field(self, objects, prefix, num):
        for i, object in enumerate(objects):
            self.fields['%s%s' % (prefix, object.name)] = ChoiceField(choices=[(x, x) for x in range(0, 11)])
            self.fields['%s%s' % (prefix, object.name)].label = object.name
            self.fields['%s%s' % (prefix, object.name)].help_text = prefix


    # Takes some objects and puts them in a ProductMultiChoiceField.
    # The field name will be named by the fieldname argument.
    # A products will be checked if they exist in an order for the current exhibitor
    def products_as_multi_field(self, products, fieldname, orders):
        # An order will have the amount 1 if checked, otherwise 0. Only for readability purposes!
        class Status(Enum):
            CHECKED = 1
            UNCHECKED = 0
        # List of all checked products
        checkedProductsList = [None]
        for order in orders:
            checkedProductsList.append(order.product)
        # create field and make sure all products that is inside the dictionary is initially checked
        if fieldname == 'product_selection_rooms':
            self.fields[fieldname] = self.RoomMultiChoiceField(queryset=products, required=False, widget=CheckboxSelectMultiple())
        elif fieldname == 'product_selection_nova':
            self.fields[fieldname] = self.NovaMultiChoiceField(queryset=products, required=False, widget=CheckboxSelectMultiple())
        else:
            self.fields[fieldname] = self.ProductMultiChoiceField(queryset=products, required=False, widget=CheckboxSelectMultiple())
        self.fields[fieldname].initial = [p for p in checkedProductsList]


    # Takes some objects and puts them in a ProductMultiChoiceField.
    # The field name will be named by the fieldname argument.
    # A products will be checked if they exist in an order for the current exhibitor
    def products_as_select_field(self, products, fieldname, orders, widget):
        # An order will have the amount 1 if checked, otherwise 0. Only for readability purposes!
        class Status(Enum):
            CHECKED = 1
            UNCHECKED = 0
        # List of all checked products
        checkedProductsList = [None]
        for order in orders:
            checkedProductsList.append(order.product)
        # create field and make sure all products that is inside the dictionary is initially checked
        listProducts = []
        for product in products:
            option = str(product.name)
            option = option.replace(" ", "")
            option = option.replace(",", "_")
            label = product.name
            tup = (option, label)
            listProducts.append(tup)
            #listProducts.append(product.name)
        if widget == "RadioSelect":
            self.fields[fieldname] = self.ProductSelectChoiceField(choices=listProducts, required=False, widget=RadioSelect())
        elif widget == "Select":
            self.fields[fieldname] = self.ProductSelectChoiceField(choices=listProducts, required=False, widget=Select())
        try:
            # Fix for radio buttons and select to show ordered product
            # Try/except because if there is no order, there will be indexError
            self.initial[fieldname] = orders[0].product.name
        except IndexError:
            pass
        #self.fields[fieldname].initial = [p for p in checkedProductsList]


    # A modelmultiplechoicefield with a customized label for each instance
    class ProductSelectChoiceField(ChoiceField):
        def label_from_instance(self, product):
            return format_html("<span class='btn btn-armada-checkbox product-label'>{}</span> <span class='product-description'>{}</span>",
                        mark_safe(product.name),
                        mark_safe(product.description),
                    )


    # Returns a generator/iterator with all product fields where you choose an amount.
    # Choose a prefix to get which the correct type, e.g 'banquet_', or 'event_'.
    # Make sure they are the same as the ones in the form's constructor!
    def amount_products(self, prefix):
        for name, amount in self.cleaned_data.items():
            if name.startswith(prefix):
                yield(self.fields[name].object, amount)

    def accepting_terms(self):
        return self.fields['accept_terms']

    def save_or_submit(self):
        if 'submit' in self.data:
            return 'submit'
        elif 'save' in self.data:
            return 'save'

    def clean(self):
        super(ExhibitorForm, self).clean()