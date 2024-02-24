from django.shortcuts import redirect, render
from companies.models import CompanyContact


def dashboard_company(request, company_id):
    if not request.user.is_authenticated:
        return redirect("anmalan:choose_company")

    return render(request, "dashboard/index.html")


def dashboard_index(request):
    if not request.user.is_authenticated:
        return redirect("anmalan:choose_company")

    # Find all connections between this user and companies
    company_contacts = CompanyContact.objects.filter(user=request.user).exclude(
        company=None
    )

    if len(company_contacts) == 1:
        return redirect(
            "dashboard:company_dashboard", company_id=company_contacts[0].company.id
        )

    return redirect("anmalan:choose_company")
