import json
from collections import OrderedDict

from django.contrib.gis.geos import Polygon
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from exhibitors import serializers
from exhibitors.models import Exhibitor, Location, Booth, ExhibitorInBooth, LocationTick
from fair.models import Fair, FairDay

MISSING_IMAGE = "/static/missing.png"


def serialize_booths(exhibitor):
    return [
        {
            "id": eib.booth.pk,
            "location": {
                "parent": (
                    {
                        "id": eib.booth.location.parent.pk,
                        "name": eib.booth.location.parent.name,
                    }
                    if eib.booth.location.parent
                    else None
                ),
                "id": eib.booth.location.pk,
                "name": eib.booth.location.name,
            },
            "name": eib.booth.name,
            "comment": eib.comment,
            "days": [day.date for day in eib.days.all()],
        }
        for eib in exhibitor.exhibitorinbooth_set.all()
    ]


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
            ("booths", serialize_booths(exhibitor)),
            ("map_coordinates", exhibitor.map_coordinates),
        ]
    )


@cache_page(60)
def exhibitors(request):
    fair_criteria = (
        {"year": request.GET["year"]} if "year" in request.GET else {"current": True}
    )

    exhibitors = (
        Exhibitor.objects.filter(
            fair__in=Fair.objects.filter(**fair_criteria),
            application_status="1",  # Accepted
        )
        .select_related(
            "company",
            "fair",
            "check_in_user",
            "fair_location",
        )
        .prefetch_related(
            "catalogue_industries",
            "catalogue_values",
            "catalogue_employments",
            "catalogue_locations",
            "catalogue_competences",
            "catalogue_benefits",
            "company__groups",
            "exhibitorinbooth_set__booth__location__parent",
            "exhibitorinbooth_set__booth__location",
            "exhibitorinbooth_set__days",
        )
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


def location(request, location_pk):
    location = get_object_or_404(Location, fair__current=True, pk=location_pk)

    booths = []

    for booth in Booth.objects.filter(location=location):
        booths.append(
            {
                "id": booth.pk,
                "name": booth.name,
                "boundaries": booth.boundaries.coords[0],
                "centroid": booth.boundaries.centroid.coords,
                "exhibitors": [
                    {
                        "id": exhibitor_in_booth.exhibitor.pk,
                        "name": exhibitor_in_booth.exhibitor.company.name,
                        "comment": exhibitor_in_booth.comment,
                        "days": [
                            {"id": day.pk, "date": day.date}
                            for day in exhibitor_in_booth.days.all()
                        ],
                    }
                    for exhibitor_in_booth in ExhibitorInBooth.objects.filter(
                        booth=booth
                    )
                ],
            }
        )

    data = {
        "id": location.pk,
        "parent": (
            {"id": location.parent.pk, "name": location.parent.name}
            if location.parent
            else None
        ),
        "name": location.name,
        "map": (
            {
                "url": location.background.url,
                "width": location.background.width,
                "height": location.background.height,
            }
            if location.background
            else None
        ),
        "booths": booths,
    }

    return JsonResponse(data, safe=False)


def days(request):
    data = []

    for day in FairDay.objects.filter(fair__current=True):
        data.append({"id": day.pk, "date": day.date})

    return JsonResponse(data, safe=False)


@require_POST
def create_booth(request, location_pk):
    location_obj = get_object_or_404(Location, pk=location_pk)

    if not request.user:
        return JsonResponse({"message": "Authentication required."}, status=403)

    data = json.loads(request.body)

    booth = Booth.objects.create(
        location=location_obj, name=data["name"], boundaries=Polygon(data["boundaries"])
    )

    return JsonResponse({"booth": serializers.booth(booth)}, status=201)


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
