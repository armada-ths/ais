from django.shortcuts import redirect, render
from companies.models import CompanyContact


def register_company_contact(request):
    if request.user.is_authenticated:
        return redirect("dashboard:index")

    return render(request, "dashboard/index.html")


def dashboard_index(request):
    if not request.user.is_authenticated:
        return redirect("anmalan:choose_company")

    company_contact = (
        CompanyContact.objects.filter(user=request.user).exclude(company=None).first()
    )

    if company_contact is not None:
        return redirect(
            "dashboard:company_dashboard", company_id=company_contact.company.id
        )

    return redirect("anmalan:choose_company")


def company_dashboard(request, company_id):
    if not request.user.is_authenticated:
        return redirect("anmalan:choose_company")

    return render(request, "dashboard/index.html")
