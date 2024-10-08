import json
from collections import OrderedDict

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from exhibitors import serializers
from exhibitors.models import Exhibitor, Location, LocationTick
from fair.models import Fair, FairDay

MISSING_IMAGE = "/static/missing.png"


def serialize_exhibitor(exhibitor, request):
    img_placeholder = request.GET.get("img_placeholder") == "true"

    return OrderedDict(
        [
            ("id", exhibitor.pk),
            ("name", exhibitor.company.name),
            ("type", exhibitor.company.type.type),
            ("tier", exhibitor.tier),
            ("company_website", exhibitor.company.website),
            ("about", exhibitor.catalogue_about),
            ("purpose", exhibitor.catalogue_purpose),
            (
                "logo_squared",
                (
                    (exhibitor.catalogue_logo_squared.url)
                    if exhibitor.catalogue_logo_squared
                    else (MISSING_IMAGE if img_placeholder else None)
                ),
            ),
            (
                "logo_freesize",
                (
                    (exhibitor.catalogue_logo_freesize.url)
                    if exhibitor.catalogue_logo_freesize
                    else (MISSING_IMAGE if img_placeholder else None)
                ),
            ),
            (
                "industries",
                [
                    {"id": industry.pk, "name": industry.industry}
                    for industry in exhibitor.catalogue_industries.all()
                ],
            ),
            (
                "values",
                [
                    {"id": value.pk, "name": value.value}
                    for value in exhibitor.catalogue_values.all()
                ],
            ),
            (
                "employments",
                [
                    {"id": employment.pk, "name": employment.employment}
                    for employment in exhibitor.catalogue_employments.all()
                ],
            ),
            (
                "locations",
                [
                    {"id": location.pk, "name": location.location}
                    for location in exhibitor.catalogue_locations.all()
                ],
            ),
            (
                "competences",
                [
                    {"id": competence.pk, "name": competence.competence}
                    for competence in exhibitor.catalogue_competences.all()
                ],
            ),
            (
                "cities",
                (
                    exhibitor.catalogue_cities
                    if exhibitor.catalogue_cities is not None
                    else ""
                ),
            ),
            (
                "benefits",
                [
                    {"id": benefit.pk, "name": benefit.benefit}
                    for benefit in exhibitor.catalogue_benefits.all()
                ],
            ),
            ("average_age", exhibitor.catalogue_average_age),
            ("founded", exhibitor.catalogue_founded),
            (
                "groups",
                [
                    {"id": group.pk, "name": group.name}
                    for group in exhibitor.company.groups.filter(
                        fair=exhibitor.fair, allow_exhibitors=True
                    )
                ],
            ),
            (
                "fair_location",
                str(exhibitor.fair_location) if exhibitor.fair_location else "",
            ),
            (
                "vyer_position",
                exhibitor.vyer_position if exhibitor.vyer_position else "",
            ),
            (
                "location_special",
                (
                    str(exhibitor.fair_location_special)
                    if exhibitor.fair_location_special
                    else ""
                ),
            ),
            ("climate_compensation", exhibitor.climate_compensation),
            ("flyer", (exhibitor.flyer.url) if exhibitor.flyer else ""),
            ("map_coordinates", exhibitor.map_coordinates),
        ]
    )


@cache_page(60)
def exhibitors(request):
    fair = (
        Fair.objects.get(current=True)
        if "year" not in request.GET
        else Fair.objects.get(year=request.GET["year"])
    )

    # Will get the string key for the accepted status.
    # MUST exist, otherwise the server is in an invalid state.
    ACCEPTED_STATUS_KEY = next(
        status[0]
        for status in Exhibitor.application_statuses
        if status[1] == "accepted"
    )

    if ACCEPTED_STATUS_KEY is None:
        return JsonResponse({"message": "No accepted status found"}, status=500)

    # For the fair 2024 we introduced the exhibitor status system.
    # During an IR signing, an exhibitor is created with the status "pending".
    # Only "accepted" exhibitors are returned in this exhibitors endpoint.
    # However, for all fairs before 2024, we haven't set the status to "accepted" for the exhibitors.
    # This is an ugly hack to make sure that all exhibitors before 2024 are returned even though they are not "accepted".
    # TODO: Remove this when we go into the production database and set all exhibitors prior to 2024 to accepted.

    if fair.year >= 2024:
        exhibitors = Exhibitor.objects.filter(
            fair=fair,
            application_status=ACCEPTED_STATUS_KEY,
        )
    else:
        exhibitors = Exhibitor.objects.filter(fair=fair)

    exhibitors = exhibitors.select_related(
        "company",
        "fair",
        "check_in_user",
        "fair_location",
    ).prefetch_related(
        "catalogue_industries",
        "catalogue_values",
        "catalogue_employments",
        "catalogue_locations",
        "catalogue_competences",
        "catalogue_benefits",
        "company__groups",
    )

    data = [serialize_exhibitor(exhibitor, request) for exhibitor in exhibitors]
    return JsonResponse(data, safe=False)


def locations(request):
    data = []

    for location in Location.objects.filter(fair__current=True):
        data.append(
            {
                "id": location.pk,
                "parent": (
                    {"id": location.parent.pk, "name": location.parent.name}
                    if location.parent
                    else None
                ),
                "name": location.name,
                "has_map": bool(location.background),
            }
        )

    return JsonResponse(data, safe=False)


def days(request):
    data = []

    for day in FairDay.objects.filter(fair__current=True):
        data.append({"id": day.pk, "date": day.date})

    return JsonResponse(data, safe=False)


@require_POST
@csrf_exempt
def people_count(request, location_pk):
    location = get_object_or_404(Location, pk=location_pk)

    if not request.user:
        return JsonResponse({"message": "Authentication required."}, status=403)

    data = json.loads(request.body)

    if location.people_count is None:
        location.people_count = 0

    location.people_count += data["change"]
    location.save()

    LocationTick(
        location=location,
        user=request.user,
        change=data["change"],
        new_people_count=location.people_count,
    ).save()

    return JsonResponse({"people_count": location.people_count}, status=200)
