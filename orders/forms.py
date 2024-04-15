from django.forms import Select, Form, ModelChoiceField, HiddenInput
from django import forms

from orders.models import Product, Order, ElectricityOrder


class ElectricityOrderForm(forms.ModelForm):
    class Meta:
        model = ElectricityOrder
        fields = "__all__"

    def __init__(self, exhibitor, *args, **kwargs):
        instance = kwargs.get("instance")
        super(ElectricityOrderForm, self).__init__(*args, **kwargs)
        if instance == None:
            self.fields["exhibitor"].initial = exhibitor.pk
        self.fields["exhibitor"].disabled = (
            True  # make sure exhibitor field is not editable
        )
        self.fields["exhibitor"].widget = HiddenInput()


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"

    def __init__(self, exhibitor, *args, **kwargs):
        instance = kwargs.get("instance")
        super(OrderForm, self).__init__(*args, **kwargs)
        if instance == None:
            self.fields["exhibitor"].initial = exhibitor.pk
            self.fields["amount"].initial = 1
        self.fields["exhibitor"].disabled = (
            True  # make sure exhibitor field is not editable
        )
        self.fields["amount"].disabled = (
            True  # make sure exhibitor field is not editable
        )
        self.fields["exhibitor"].widget = HiddenInput()
        self.fields["amount"].widget = HiddenInput()

    def save(self, **kwargs):
        order_form = super(OrderForm, self).save(commit=False)
        try:
            # Check if it is an update or just a new one
            order = Order.objects.get(pk=order_form.pk)
            # if previous line does not fail, it is an update that is being made
            # if the amount is 0, we should rather delete the order than setting it to 0
            if order_form.amount == 0:
                order.delete()
            else:
                order_form.save()
        except:
            # Previous order did not exist so just save it if it is not 0 amonut
            if not order_form.amount == 0:
                order_form.save()


class OrderSelectionForm(OrderForm):
    class Meta:
        model = Order
        fields = "__all__"

    def __init__(self, exhibitor, product_type, query_set, *args, **kwargs):
        super(OrderSelectionForm, self).__init__(exhibitor, *args, **kwargs)
        self.fields["product"].queryset = query_set
        self.fields["product"].label = "Select product"


class OrderCheckboxForm(OrderForm):
    class Meta:
        model = Order
        fields = "__all__"

    def __init__(self, exhibitor, product, *args, **kwargs):
        instance = kwargs.get("instance")
        super(OrderCheckboxForm, self).__init__(exhibitor, *args, **kwargs)
        self.fields["add"] = forms.BooleanField(initial=False, required=False)
        self.fields["add"].label = "Add product " + product.name
        self.fields["add"].help_text = product.description
        self.fields["add"].widget = forms.CheckboxInput()

        if instance == None:
            self.fields["product"].initial = product.pk
        else:
            self.fields["add"].initial = True

        self.fields["product"].label = product.name + ", +" + str(product.price) + ":-"
        self.fields["product"].disabled = True
        self.fields["product"].widget = HiddenInput()

    def save(self, commit=False):
        if self.cleaned_data["add"] == True:
            super(OrderCheckboxForm, self).save(commit=True)
        else:
            # Try to delete previous order if existing
            try:
                prev_order = Order.objects.filter(
                    exhibitor=self.cleaned_data["exhibitor"],
                    product=self.cleaned_data["product"],
                ).first()
                prev_order.delete()
            except:
                pass


class OrderAmountForm(OrderForm):
    def __init__(self, exhibitor, product, *args, **kwargs):
        instance = kwargs.get("instance")
        super(OrderAmountForm, self).__init__(exhibitor, *args, **kwargs)
        self.fields["amount"].disabled = False
        self.fields["amount"].widget = forms.NumberInput()
        self.fields["amount"].help_text = product.description
        self.fields["amount"].label = "Amount"
        self.fields["product"].label = product.name + ", +" + str(product.price) + ":-"
        if instance == None:
            self.fields["product"].initial = product.pk
            self.fields["amount"].initial = 0
        self.fields["product"].disabled = True
        self.fields["product"].widget = HiddenInput()


def get_order_forms(exhibitor, product_type, *args, **kwargs):
    """
    Returns a list of order forms. Given the product type, the orderforms could be
    a select one field or select multiple field, together with an amount field or not.
    A product type with selection_policy == 'SELECT' will return a form with one ChoiceField
    where the choices are the products that has that product type.
    """
    if product_type.selection_policy == "SELECT":
        query_set = Product.objects.filter(
            fair=exhibitor.fair, product_type=product_type, display_in_product_list=True
        )
        kwargs["instance"] = Order.objects.filter(
            exhibitor=exhibitor, product__in=query_set
        ).first()
        if len(query_set) == 0:
            return []
        else:
            return [
                OrderSelectionForm(exhibitor, product_type, query_set, *args, **kwargs)
            ]
    else:
        order_forms = []
        products = Product.objects.filter(
            product_type=product_type, fair=exhibitor.fair, display_in_product_list=True
        )
        for i, product in enumerate(products):
            kwargs["instance"] = Order.objects.filter(
                exhibitor=exhibitor, product=product
            ).first()
            kwargs["prefix"] = kwargs["prefix"] + str(i)
            if product_type.selection_policy == "SELECT_MULTIPLE":
                order_forms.append(
                    OrderCheckboxForm(exhibitor, product, *args, **kwargs)
                )
            else:
                order_forms.append(OrderAmountForm(exhibitor, product, *args, **kwargs))
        return order_forms
