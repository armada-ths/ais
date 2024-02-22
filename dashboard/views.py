from datetime import timezone

from django.shortcuts import redirect, render
from companies.models import CompanyContact
from fair.models import Fair


def dashboard_index(request):
    if not request.user.is_authenticated:
        return redirect("anmalan:choose_company")

    # find all connections between this user and companies
    company_contacts = CompanyContact.objects.filter(user=request.user).exclude(
        company=None
    )

    if len(company_contacts) == 1:
        return render(request, "dashboard/index.html")

    return redirect("anmalan:choose_company")
