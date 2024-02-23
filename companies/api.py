from itertools import groupby

from django.http import HttpResponseBadRequest, JsonResponse

from companies.models import Company, Group

import api.serializers as serializers
from util import get_fair


def get_registration_groups(request):
    fair = get_fair()
    groups = Group.objects.filter(
        fair=fair, allow_registration=True, parent__allow_registration=True
    )

    groups = groupby(groups, lambda group: group.parent)

    groups = [
        {
            "id": parent.id,
            "name": parent.name,
            "children": [{"id": child.id, "name": child.name} for child in children],
        }
        for parent, children in groups
    ]

    return JsonResponse(groups, safe=False)


def companies(request):
    """
    Returns a query of customizable amount of companies (default= 10) based on user input
    """
    if request.method == "GET":
        limit = request.GET.get("limit", 0)
        input = request.GET.get("input", "")

        limit = int(limit)

        if limit == 0:
            companies = Company.objects.filter(name__icontains=input)
        else:
            companies = Company.objects.filter(name__icontains=input)[:limit]

        data = [serializers.companies(request, company) for company in companies]
        return JsonResponse(data, safe=False)

    else:
        return HttpResponseBadRequest("Unsupported method!", content_type="text/plain")
