from collections import OrderedDict
from lib.util import unix_time
from people.models import Profile

from matching.models import StudentQuestionType as QuestionType


MISSING_IMAGE = "/static/missing.png"
MISSING_MAP = "/static/nymble_2048.png"
MISSING_PERSON = "/static/images/no-image.png"


def tags_mappings(items):
    tags = [i.name for i in items]
    return [
        ("diversity", "Diversity" in tags),
        ("sustainability", "Sustainability" in tags),
        ("startup", "Startup" in tags),
    ]


def absolute_url(request, path):
    protocol = "https://" if request.is_secure() else "http://"
    url = request.META["HTTP_HOST"]
    return "{}{}/{}".format(protocol, url, path)


def image_url_or_missing_relative(image, missing=MISSING_IMAGE):
    return image.url if image else missing


# This function does not handle trailing slashes
# A common response is "http://localhost:3000//static/images/no-image.png"
#
# Another problem is the usage of ais buckets
# A common response is "https://ais.armada.nu/https://armada-ais-files.s3.amazonaws.com/profiles/picture_original/3d867d2a75f84e3eb32..."
#
# Please use `image_url_or_missing_relative`
def image_url_or_missing(request, image, missing=MISSING_IMAGE):
    return absolute_url(request, image.url if image else missing)


def obj_name(obj):
    if not obj:
        return {}
    return OrderedDict([("id", obj.pk), ("name", obj.name)])


def names(objects):
    return [obj_name(obj) for obj in objects.all()]


# This seems unused. Seems like exhibitors/api.py is
# preferred. They are very similar.
def exhibitor(request, exhibitor, company):
    img_placeholder = request.GET.get("img_placeholder") == "true"

    return OrderedDict(
        [
            ("id", exhibitor.pk),
            ("name", company.name),
            ("type", company.type.type),
            ("company_website", company.website),
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
            ("contact_name", exhibitor.catalogue_contact_name),
            ("contact_email_address", exhibitor.catalogue_contact_email_address),
            ("contact_phone_number", exhibitor.catalogue_contact_phone_number),
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
                    for group in company.groups.filter(
                        fair=exhibitor.fair, allow_exhibitors=True
                    )
                ],
            ),
            ("fair_locations", []),  # Shouldn't this be something...?
        ]
    )


def companies(request, company):
    return OrderedDict(
        [
            ("Organization Name", company.name),
            ("id", company.id),
        ]
    )


def event(request, event):
    tags = tags_mappings(event.tags.all())
    signup_link = (
        event.external_signup_url
        if event.external_signup_url
        else absolute_url(request, "/fairs/2017/events/" + str(event.pk) + "/signup")
    )
    return OrderedDict(
        [
            ("id", event.pk),
            ("name", event.name),
            ("image_url", image_url_or_missing(request, event.image_original)),
            ("location", event.location),
            ("description_short", event.description_short),
            ("description", event.description),
            ("signup_link", signup_link),
            ("event_start", unix_time(event.event_start)),
            ("event_end", unix_time(event.event_end)),
            ("registration_required", event.registration_required),
            ("registration_start", unix_time(event.registration_start)),
            ("registration_end", unix_time(event.registration_end)),
            (
                "registration_last_day_cancel",
                unix_time(event.registration_last_day_cancel),
            ),
        ]
        + tags
    )


def newsarticle(request, newsarticle):
    return OrderedDict(
        [
            ("id", newsarticle.pk),
            ("title", newsarticle.title),
            ("date_published", unix_time(newsarticle.publication_date)),
            ("html_article_text", newsarticle.html_article_text),
            ("image", image_url_or_missing(request, newsarticle.image)),
        ]
    )


def partner(request, partner):
    return OrderedDict(
        [
            ("id", partner.pk),
            ("name", partner.name),
            ("logo_url", absolute_url(request, partner.logo.url)),
            ("link_url", partner.url),
            ("is_main_partner", partner.main_partner),
        ]
    )


def person_v2(user):
    # Check that there is a profile for the user
    try:
        profile = user.profile

        try:
            programme = profile.programme.name
        except AttributeError:
            programme = None

        return OrderedDict(
            [
                ("id", profile.user.pk),
                ("name", profile.user.get_full_name()),
                ("email", profile.armada_email),
                (
                    "picture",
                    image_url_or_missing_relative(
                        profile.picture_original, MISSING_PERSON
                    ),
                ),
                ("linkedin_url", profile.linkedin_url),
                ("programme", programme),
                ("role", user.delegated_role.__str__()),
            ]
        )
    except Profile.DoesNotExist:  # There is no profile for this user
        return OrderedDict(
            [
                ("id", user.pk),
                ("name", user.user.get_full_name()),
                (
                    "role",
                    user.delegated_role.__str__() if user.delegated_role else None,
                ),
            ]
        )


# Todo: Deprecate the usage of this serializer (used by armada.nu)
def person(request, person, role):
    # Check that there are a profile for the user
    try:
        profile = person.profile
        try:
            programme = profile.programme.name
        except AttributeError:
            programme = None
        return OrderedDict(
            [
                ("id", profile.user.pk),
                ("name", profile.user.get_full_name()),
                (
                    "picture",
                    image_url_or_missing(
                        request, profile.picture_original, MISSING_PERSON
                    ),
                ),
                ("linkedin_url", profile.linkedin_url),
                ("programme", programme),
                ("role", role),
            ]
        )
    except Profile.DoesNotExist:  # There are no profile for this user
        return OrderedDict(
            [("id", person.pk), ("name", person.get_full_name()), ("role", role)]
        )


def organization_group(request, group):
    people = [person(request, p, group.name) for p in group.user_set.all()]
    return OrderedDict([("id", group.pk), ("role", group.name), ("people", people)])


def serialize_slider(question):
    """
    Serialize a SLIDER question.
    """
    question = question.studentquestionslider
    return OrderedDict(
        [
            ("id", question.pk),
            ("type", question.question_type),
            ("question", question.question),
            ("min", question.min_value),
            ("max", question.max_value),
            ("logarithmic", question.logarithmic),
            ("units", question.units),
        ]
    )


def serialize_grading(question):
    """
    Serialize a GRADING question.
    """
    question = question.studentquestiongrading
    return OrderedDict(
        [
            ("id", question.pk),
            ("type", question.question_type),
            ("question", question.question),
            ("count", question.grading_size),
        ]
    )


# A dictionary of serializer functions, that avoids a huge (eventually) switch-block
QUESTION_SERIALIZERS = {
    QuestionType.SLIDER.value: serialize_slider,
    QuestionType.GRADING.value: serialize_grading,
}


def question(question):
    """
    Serialize a StudentQuestionBase child question.
    """
    # theoretically we could have a common process for every question (the question itself and its type)
    # but that adds unncecessary complexity to the code, without optimizing or simplifying it
    if question.question_type in QUESTION_SERIALIZERS:
        return QUESTION_SERIALIZERS[question.question_type](question)
    else:
        raise NotImplementedError(
            "Couldn't serialize " + question.question_type + " type!"
        )
    return []  # could not serialize a type


def work_area(area):
    """
    Serialize a work field area
    """
    return OrderedDict(
        [
            ("id", area.pk),
            ("field", area.work_field),
            ("area", area.work_area.work_area),
        ]
    )


def matching_result(matching):
    """
    Serialize a matching for a student_profile
    """
    return OrderedDict(
        [
            ("exhibitor", matching.exhibitor.pk),
            ("percent", matching.score),
            (
                "reasons",
                ["", "", ""],
            ),  # This is just empty strings for now. Might change if we get any reasons from the matching algortithm.
        ]
    )


def student_profile(profile):
    """
    Serializes StudentProfile
    """
    return OrderedDict(
        [
            ("nickname", profile.nickname),
            ("linkedin_profile", profile.linkedin_profile),
            ("facebook_profile", profile.facebook_profile),
            ("phone_number", profile.phone_number),
        ]
    )
