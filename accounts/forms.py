from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class ExternalUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "email",
            "password1",
            "password2",
        )

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            user = User.objects.get(email=email.lower())
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % email)


class ExternalUserLoginForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExternalUserLoginForm, self).__init__(*args, **kwargs)
        self.fields["password"] = forms.CharField(
            widget=forms.PasswordInput(attrs={"placeholder": "Password"})
        )
        self.fields["email"].label = ""
        self.fields["password"].label = ""
        self.fields["email"].widget = forms.TextInput(attrs={"placeholder": "Email"})

    class Meta:
        model = User
        fields = (
            "email",
            "password",
        )

    def clean(self):
        email = self.data["email"]
        password = self.data["password"]
        try:
            # check if a user exists with the inputed credentials.
            # set_passwords hashes the password since its hash string is in the db
            # and not the real password itsef
            user = User.objects.get(email=email.lower())
        except User.DoesNotExist:
            # according to standardized recommendations you should not reveil what field is wrong
            raise forms.ValidationError(_("Invalid Email or Password!"))

        # hash the password variable and see if it matches the users stored hashed password in db
        if user.check_password(password):
            return self.cleaned_data
        else:
            # according to standardized recommendations you should not reveil what field is wrong
            raise forms.ValidationError(_("Invalid Email or Password!"))
