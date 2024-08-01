MISSING_IMAGE = "/static/missing.png"


def exhibitor(request, exhibitor, company):
    img_placeholder = request.GET.get("img_placeholder") == "true"

    data = {
        "id": exhibitor.pk,
        "name": company.name,
        "type": company.type.type,
        "company_website": company.website,
        "about": exhibitor.catalogue_about,
        "purpose": exhibitor.catalogue_purpose,
        "logo_squared": (
            exhibitor.catalogue_logo_squared.url
            if exhibitor.catalogue_logo_squared
            else (MISSING_IMAGE if img_placeholder else None)
        ),
        "logo_freesize": (
            exhibitor.catalogue_logo_freesize.url
            if exhibitor.catalogue_logo_freesize
            else (MISSING_IMAGE if img_placeholder else None)
        ),
        "contact_name": exhibitor.catalogue_contact_name,
        "contact_email_address": exhibitor.catalogue_contact_email_address,
        "contact_phone_number": exhibitor.catalogue_contact_phone_number,
        "industries": [
            {"id": industry.pk, "name": industry.industry}
            for industry in exhibitor.catalogue_industries.all()
        ],
        "values": [
            {"id": value.pk, "name": value.value}
            for value in exhibitor.catalogue_values.all()
        ],
        "employments": [
            {"id": employment.pk, "name": employment.employment}
            for employment in exhibitor.catalogue_employments.all()
        ],
        "locations": [
            {"id": location.pk, "name": location.location}
            for location in exhibitor.catalogue_locations.all()
        ],
        "competences": [
            {"id": competence.pk, "name": competence.competence}
            for competence in exhibitor.catalogue_competences.all()
        ],
        "cities": (
            exhibitor.catalogue_cities if exhibitor.catalogue_cities is not None else ""
        ),
        "benefits": [
            {"id": benefit.pk, "name": benefit.benefit}
            for benefit in exhibitor.catalogue_benefits.all()
        ],
        "average_age": exhibitor.catalogue_average_age,
        "founded": exhibitor.catalogue_founded,
        "groups": [
            {"id": group.pk, "name": group.name}
            for group in company.groups.filter(
                fair=exhibitor.fair, allow_exhibitors=True
            )
        ],
        "fair_locations": [],
    }

    return data


def exhibitor_chat(chat):
    data = {
        "name": f"{chat.user.first_name},{chat.user.last_name}",
        "email": chat.user.email,
        "comment": chat.chat,
        "time": chat.timestamp,
        "is_armada": chat.is_armada_response,
    }
    return data


def lunch_ticket(lunch_ticket):
    data = {
        "id": lunch_ticket.pk,
        "company": lunch_ticket.company.name,
        "comment": lunch_ticket.comment,
        "day": lunch_ticket.day.name if lunch_ticket.day else None,
        "dietary_restrictions": [
            diet.name for diet in lunch_ticket.dietary_restrictions.all()
        ],
    }

    return data


def location(location):
    data = {
        "id": location.pk,
        "name": location.name,
        "booths": [booth(booth_obj) for booth_obj in location.booth_set.all()],
        "map": {
            "url": location.background.url,
            "width": location.background.width,
            "height": location.background.height,
        },
    }

    return data


def booth(booth):
    data = {
        "id": booth.pk,
        "name": booth.name,
        "boundaries": booth.boundaries.coords[0],
        "centroid": booth.boundaries.centroid.coords,
    }

    return data
