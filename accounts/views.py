from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .forms import ExternalUserLoginForm

# Create your views here.
def login(request):
    return render(request, "accounts/login.html")


# TODO: make these external signup and login general. With possibility to
# provide a next link that it should redirect to. That way they can be used
# from any application.
def external_create_account(
    request, template_name="accounts/create_external_user.html"
):
    """
    Sign up for external people meaning those who are not in Armada and not from KTH.
    """
    if request.user.is_authenticated:
        # TODO: this line needs to be changed for next years banquet signup.
        # Now it redirects to placement
        return HttpResponseRedirect(reverse("banquet/placement", kwargs={"year": 2019}))
    else:
        form = ExternalUserForm(request.POST or None, prefix="user")
        if form.is_valid():
            user = form.save(commit=False)
            mail = form.cleaned_data["email"].lower()
            user.username = mail
            user.email = mail
            # the form's cleaning checks if the user email already exists
            user.save()
            user = authenticate(
                username=mail,
                password=form.cleaned_data["password1"],
            )
            login(request, user)

            return HttpResponseRedirect(
                reverse("banquet/signup", kwargs={"year": 2019})
            )
    return render(request, template_name, dict(form=form, year=2019))


def external_login(request, template_name="accounts/external_login.html"):
    """
    Login in for external people meaning those who are not in Armada and not from KTH.
    Will redirect to external banquet signup
    """
    form = ExternalUserLoginForm(request.POST or None)
    if form.is_valid():
        user = authenticate(
            username=form.cleaned_data["email"].lower(),
            password=form.cleaned_data["password"],
        )
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(
                reverse("banquet/placement", kwargs={"year": 2019})
            )

    return render(request, template_name, dict(form=form, year=2019))
