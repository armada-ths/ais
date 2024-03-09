import subprocess
import os

import json
import platform
import subprocess
from collections import OrderedDict
from datetime import datetime
from itertools import chain

from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from django.utils.crypto import get_random_string

import api.deserializers as deserializers
import api.serializers as serializers

from .util import json_to_csv_response

from exhibitors.models import (
    Exhibitor,
    CatalogueIndustry,
    CatalogueValue,
    CatalogueEmployment,
    CatalogueLocation,
    CatalogueCompetence,
)  # CatalogueBenefit
from exhibitors.api import serialize_exhibitor
from fair.models import Partner, Fair, FairDay, OrganizationGroup, current_fair
from matching.models import StudentQuestionBase as QuestionBase, WorkField, Survey
from news.models import NewsArticle
from recruitment.models import RecruitmentPeriod, RecruitmentApplication
from student_profiles.models import StudentProfile, MatchingResult
from companies.models import Company
from magic_link.models import MagicLink, link_expires_at


def root(request):
    return JsonResponse({"message": "Welcome to the Armada API!"})


@csrf_exempt
def matching(request):
    # Validate POST-input to make sure the given answers exist
    if request.method == "POST":
        if request.body:
            try:
                # convert json to dict
                data = json.loads(request.body.decode())
            except Exception:
                return HttpResponse(
                    "Misformatted json!", content_type="text/plain", status=406
                )

            # Here is where the actual deserialization happens:
            if deserializers.matching(data):
                docID = get_random_string(length=32)
                random_doc_name = os.path.join("/tmp/", docID + ".json")
                matching_script_loc = "/opt/matching.py"

                with open(random_doc_name, "w") as outfile:
                    json.dump(data, outfile)
                fair_id = current_fair()
                if current_fair() is None:
                    fair_id = 4  # Default to 2019

                retrieved = subprocess.Popen(
                    [
                        "python3",
                        matching_script_loc,
                        docID,
                        random_doc_name,
                        str(fair_id),
                    ],
                    stdout=subprocess.PIPE,
                )
                # have to wait for subprocess to finish
                retrieved.wait()
                matching_path = os.path.join("/tmp/", docID + "_output.json")
                with open(matching_path, "r") as matching_file:
                    matching_data = json.load(matching_file)

                # print(matching_data) # Leaving this for debugging purposes

                # Only serialize each exhibitor once, even if
                # one exhibitor appears as a top choice in several cateogories.
                exhibitors = {}
                for category, similar_companies in matching_data.items():
                    for company in similar_companies:
                        exhibitor_id = company["exhibitor_id"]
                        if exhibitor_id not in exhibitors:
                            exhibitors[exhibitor_id] = serialize_exhibitor(
                                Exhibitor.objects.filter(pk=exhibitor_id).first(),
                                request,
                            )

                response = {"similarities": matching_data, "exhibitors": exhibitors}

                return JsonResponse(response, safe=False)

            else:
                return HttpResponse(
                    "Failed to update profile (deserialization error)!",
                    content_type="text/plain",
                    status=406,
                )
    else:
        return HttpResponseBadRequest("Unsupported method!", content_type="text/plain")


# When using the matching function, this api can be used
# to present the questions that the user should answer.
# the response holds the questions, as well as
# the order in which they come.
@cache_page(60 * 15)
@csrf_exempt
def matching_choices(request):
    if request.method == "GET":
        # Get the choices that we include in the company forms
        competences = CatalogueCompetence.objects.filter(include_in_form=True).values(
            "id", "competence"
        )
        employments = CatalogueEmployment.objects.filter(include_in_form=True).values(
            "id", "employment"
        )
        values = CatalogueValue.objects.filter(include_in_form=True).values(
            "id", "value"
        )
        industries = CatalogueIndustry.objects.filter(include_in_form=True).values(
            "id", "industry"
        )
        locations = CatalogueLocation.objects.filter(include_in_form=True).values(
            "id", "location"
        )

        # We want to return a JSON object with the options the user has
        response = {"options": [], "meta": {}}

        # Indicates which order the questions/answers come in
        # in the options list.
        response["meta"]["order"] = [
            "values",
            "industries",
            "competences",
            "employments",
            "locations",
        ]

        current_fair_id = current_fair()
        if current_fair() is None:
            current_fair_id = 4  # Default to 2019

        response["meta"]["max_response_size"] = Exhibitor.objects.filter(
            fair_id=current_fair_id
        ).count()

        def append_component(key):
            if key == "competences":
                # Append competence choices to response
                comp = {}
                comp["question"] = "What competencies do you have?"
                comp["answers"] = []
                for competence in competences:
                    comp["answers"].append(
                        {
                            "value": competence["competence"],
                            "label": competence["competence"],
                            "id": competence["id"],
                        }
                    )
                response["options"].append(comp)

            elif key == "employments":
                # Append employment choices to results
                emp = {}
                emp["question"] = "What employment types are you interested in?"
                emp["answers"] = []
                for employment in employments:
                    emp["answers"].append(
                        {
                            "value": employment["employment"],
                            "label": employment["employment"],
                            "id": employment["id"],
                        }
                    )
                response["options"].append(emp)

            elif key == "values":
                # Append value choices to results
                val = {}
                val["question"] = "What values are important to you?"
                val["answers"] = []
                for value in values:
                    val["answers"].append(
                        {
                            "value": value["value"],
                            "label": value["value"],
                            "id": value["id"],
                        }
                    )
                response["options"].append(val)

            elif key == "industries":
                # # Append industry choices to results
                ind = {}
                ind["question"] = "What industries are you interested in?"
                ind["answers"] = []
                for industry in industries:
                    ind["answers"].append(
                        {
                            "value": industry["industry"],
                            "label": industry["industry"],
                            "id": industry["id"],
                        }
                    )
                response["options"].append(ind)

            elif key == "locations":
                # # Append location choices to results
                loc = {}
                loc["question"] = "Where in the world?"
                loc["answers"] = []
                for location in locations:
                    loc["answers"].append(
                        {
                            "value": location["location"],
                            "label": location["location"],
                            "id": location["id"],
                        }
                    )
                response["options"].append(loc)

        for key in response["meta"]["order"]:
            append_component(key)

        return JsonResponse(response, safe=False)

    else:
        return HttpResponseBadRequest("Unsupported method!", content_type="text/plain")


@cache_page(60 * 5)
def catalogueselections(request):
    selections = []

    selections.append(
        {
            "selection": "industries",
            "question": "Which industries does your company work in?",
            "options": [
                (industry.pk, industry.industry)
                for industry in CatalogueIndustry.objects.all()
            ],
        }
    )

    selections.append(
        {
            "selection": "values",
            "question": "Select up to three values that apply to the company.",
            "options": [
                (value.pk, value.value) for value in CatalogueValue.objects.all()
            ],
        }
    )

    selections.append(
        {
            "selection": "employments",
            "question": "What kind of employments does your company offer?",
            "options": [
                (employment.pk, employment.employment)
                for employment in CatalogueEmployment.objects.all()
            ],
        }
    )

    selections.append(
        {
            "selection": "locations",
            "question": "Where does your company operate?",
            "options": [
                (location.pk, location.location)
                for location in CatalogueLocation.objects.all()
            ],
        }
    )

    selections.append(
        {
            "selection": "benefits",
            "question": "Which benefits does your company offers its employees?",
            "options": [
                (benefit.pk, benefit.benefit)
                for benefit in CatalogueBenefit.objects.all()
            ],
        }
    )

    return JsonResponse(selections, safe=False)


@cache_page(60 * 5)
def news(request):
    """
    Returns all news
    """
    news = NewsArticle.public_articles.all()
    data = [serializers.newsarticle(request, article) for article in news]
    return JsonResponse(data, safe=False)


@cache_page(60 * 5)
def partners(request):
    """
    Returns all partners for current fair
    """
    fair = Fair.objects.get(current=True)
    partners = Partner.objects.filter(fair=fair).order_by("-main_partner")
    data = [serializers.partner(request, partner) for partner in partners]
    return JsonResponse(data, safe=False)


@permission_required("magic_link.add_magiclink")
def create_magic_link(request):
    id = request.GET.get("user", None)
    redirect_to = request.GET.get("redirect_to", None)

    if id == None:
        return JsonResponse({"error": "id required"}, status=400)

    user = User.objects.get(pk=id)
    link = MagicLink.objects.create(
        user=user,
        redirect_to=redirect_to if redirect_to != None else "/register",
        expires_at=link_expires_at(24 * 60 * 60),  # expires in 24h
    )
    url = request.build_absolute_uri(link.get_absolute_url())

    return JsonResponse({"url": url}, safe=False)


# Todo: Deprecate the usage of this serializer (used by armada.nu)
@cache_page(60 * 5)
def organization(request):
    """
    Returns all roles for current fair
    """
    all_groups = Group.objects.prefetch_related("user_set__profile").order_by("name")

    # We only want groups that belong to roles that have been recruited during the current fair
    fair = Fair.objects.get(current=True)
    recruitment_period_roles = [
        period.recruitable_roles.all() for period in fair.recruitmentperiod_set.all()
    ]
    role_groups = [role.group for roles in recruitment_period_roles for role in roles]
    groups = [group for group in all_groups if group in role_groups]

    data = [serializers.organization_group(request, group) for group in groups]
    return JsonResponse(data, safe=False)


@cache_page(60 * 5)
def organization_v2(request):
    fair = get_object_or_404(Fair, current=True)
    groups = OrganizationGroup.objects.filter(fair=fair)
    people = lambda group: [
        serializers.person_v2(
            user,
        )
        for user in RecruitmentApplication.objects.select_related("user")
        .filter(
            delegated_role__organization_group=group,
            status="accepted",
            recruitment_period__fair=fair,
        )
        .order_by(
            "delegated_role__organization_group",
            "recruitment_period__start_date",
            "delegated_role",
            "user__first_name",
            "user__last_name",
        )
    ]

    result = [
        OrderedDict(
            [
                ("name", group.name),
                ("people", people(group)),
            ]
        )
        for group in groups
    ]

    return JsonResponse(result, safe=False)


def dates(request):
    """
    GET date of fair, ticket deadline, IR and FR start and end dates
    """
    fair = Fair.objects.get(current=True)
    days = FairDay.objects.filter(fair=fair)

    return JsonResponse(
        {
            "fair": {
                "description": fair.description,
                "days": [day.date for day in days],
            },
            "ticket": {"end": fair.companies_ticket_deadline},
            "ir": {
                "start": fair.registration_start_date,
                "acceptance": fair.registration_acceptance_date,
                "end": fair.registration_end_date,
            },
            "fr": {
                "start": fair.complete_registration_start_date,
                "end": fair.complete_registration_close_date,
            },
            "events": {
                "start": fair.events_start_date,
                "end": fair.events_end_date,
            },
        },
        safe=False,
    )


@csrf_exempt
def student_profile(request):
    """
    GET student profiles nickname by their id.
    Url: /student_profile?student_id={STUDENTPROFILEID}
    or
    PUT student profile nickname by the id
    URL: /api/student_profile?student_id={STUDENT_PROFILE_ID}
    DATA: json'{"nickname" : "{NICKNAME}"}'
    """
    if request.method == "GET":
        student_id = request.GET["student_id"]
        student = get_object_or_404(StudentProfile, pk=student_id)
        data = serializers.student_profile(student)
    elif request.method == "PUT":
        if request.body:
            student_id = request.GET["student_id"]
            (student_profile, wasCreated) = StudentProfile.objects.get_or_create(
                pk=student_id
            )
            try:
                data = json.loads(request.body.decode())
            except Exception:
                if wasCreated:
                    student_profile.delete()
                return HttpResponse(
                    "Misformatted json!", content_type="text/plain", status=406
                )
            # Here is where the actual deserialization happens:
            if deserializers.student_profile(data, student_profile):
                return HttpResponse(
                    "Profile updated sucessfully!", content_type="text/plain"
                )
            else:
                if wasCreated:
                    student_profile.delete()
                return HttpResponse(
                    "Failed to update profile (deserialization error)!",
                    content_type="text/plain",
                    status=406,
                )
        else:
            return HttpResponse(
                "No payload detected!", content_type="text/plain", status=406
            )
    else:
        return HttpResponseBadRequest("Unsupported method!", content_type="text/plain")

    return JsonResponse(data, safe=False)


def questions_GET(request):
    """
    Handles a GET request to ais.armada.nu/api/questions
    Returns all questions and possible work fields, that belong to current survey.
    Each question can be of one of QuestionType types and have special fields depending on that type.
    Expected response:
    {
    "questions" : [
        {"id" : ID_0, "type" : "slider", "question" : "QUESTION_0", "min" : MIN, "max" : MAX, "logarithmic" : LOG, "units" : "UNITS"},
        {"id" : ID_1, "type" : "grading", "question" : "QUESTION_1", "count" : GRADING_COUNT},
        ...],
    "areas" : [
        {"id" : AREA_ID, "field" : "FIELD", "area" : "AREA"},
        ...]
    }
    Where:
        ID          - is an integer, identifying that specific question
        QUESTION    - is a string of that specific question
        MIN         - a float representing the lowest bound of the answer range
        MAX         - a float representing the highest bound of the answer range
        LOG         - a boolean value, selecting a logarithmic vs linear way of displaying the answer
        UNITS       - the name (plural) of units of entity in question
        AREA_ID     - is an integer, identifying that specific area
        FIELD       - the name of the field, which is a subcategory of AREA
        AREA        - the name of a field area, which is a supercategory of FIELD
    """
    current_fair = get_object_or_404(Fair, current=True)
    survey = get_object_or_404(Survey, fair=current_fair)
    questions = QuestionBase.objects.filter(survey=survey)
    areas = WorkField.objects.filter(survey=survey)
    data = OrderedDict(
        [
            ("questions", [serializers.question(question) for question in questions]),
            ("areas", [serializers.work_area(area) for area in areas]),
        ]
    )
    return JsonResponse(data, safe=False)


def matching_result(request):
    """
    ais.armada.nu/api/matching_result?student_id=STUDENT_PROFILE_PK
    returns the result for a student after the matching algorithm is done (=> when length of result is the same as MATCHING_DONE)
    The result is an array of MAX_MATCHES matching exhibitors.
    If there are no result yet, it will return an empty list [].
    """
    MATCHING_DONE = 6
    MAX_MATCHES = 5
    current_fair = get_object_or_404(Fair, current=True)
    student_id = request.GET["student_id"]
    try:
        student = StudentProfile.objects.get(pk=student_id)
    except StudentProfile.DoesNotExist:
        return HttpResponse("No such student", content_type="text/plain", status=404)

    number_of_matches = MatchingResult.objects.filter(
        student=student, fair=current_fair
    ).count()
    if number_of_matches < MATCHING_DONE:
        data = None
    else:
        matches = MatchingResult.objects.filter(student=student).order_by("-score")[
            :MAX_MATCHES
        ]
        data = [serializers.matching_result(matching) for matching in matches]

    return JsonResponse(data, safe=False)


def intChoices(objectType, data, student, survey, function):
    """
    help function for questions_PUT. Checks if there data has an objectType with a list of Integers.
    Returns the list and True if the list is valid.
    """
    allChosen = []
    for chosen in data[objectType]:
        if type(chosen) is int:
            allChosen.append(chosen)
    function(allChosen, student, survey)
    return allChosen


def questions_PUT(request):
    """
    Handles a PUT request to ais.armada.nu/api/questions?student_id=STUDENT_ID
    Where STUDENT_ID is a unique uuid for a student.
    Expected payload looks like:
    {
    "questions" : [
        {"id" : ID, "answer" : ANSWER},
        ...]
    "areas" : [AREA_ID, ...]
    }
    Where:
        ANSWER  - is either an int or a float, depending on the type of question
        AREA_ID - is an integer id for each area that was selected, that was sent with questions_PUT

    Should respond "Answers submitted!" to a valid PUT request
    """
    if request.body:
        student_id = request.GET["student_id"]
        (student, wasCreated) = StudentProfile.objects.get_or_create(pk=student_id)
        fair = get_object_or_404(Fair, current=True)
        survey = get_object_or_404(Survey, fair=fair)
        try:
            data = json.loads(request.body.decode())
        except Exception:
            if wasCreated:
                student.delete()
            return HttpResponse(
                "Misformatted json!", content_type="text/plain", status=406
            )
        modified = False
        (modified_count, total_count) = (0, 0)

        if type(data) is not dict:
            return HttpResponse(
                "Wrong payload format!", content_type="text/plain", status=406
            )

        if "questions" in data and type(data["questions"]) is list:
            (modified_count, total_count) = deserializers.answers(
                data["questions"], student, survey
            )

        if "areas" in data and type(data["areas"]) is list:
            intChoices("areas", data, student, survey, deserializers.fields)
            modified = True
        if "regions" in data and type(data["regions"]) is list:
            intChoices("regions", data, student, survey, deserializers.regions)
            modified = True
        if "continents" in data and type(data["continents"]) is list:
            intChoices("continents", data, student, survey, deserializers.continents)
            modified = True
        if "looking_for" in data and type(data["looking_for"]) is list:
            intChoices("looking_for", data, student, survey, deserializers.jobtype)
            modified = True

        if modified or modified_count > 0:
            answer = (
                "Answers submitted! ("
                + str(modified_count)
                + "/"
                + str(total_count)
                + " question answers were saved, fields were "
            )
            if not modified:
                answer += "not "
            answer += "updated)"
            return HttpResponse(answer, content_type="text/plain")
        else:
            if wasCreated:
                student.delete()
            return HttpResponse(
                "No answers were found in payload!",
                content_type="text/plain",
                status=406,
            )
    else:
        return HttpResponse(
            "No payload detected!", content_type="text/plain", status=406
        )


@csrf_exempt
def questions(request):
    """
    ais.armada.nu/api/questions
    Handles GET request with questions_GET
    Handles PUT request with questions_PUT
    """
    if request.method == "GET":
        return questions_GET(request)
    elif request.method == "PUT":
        return questions_PUT(request)
    else:
        return HttpResponseBadRequest("Unsupported method!", content_type="text/plain")


def recruitment(request):
    """
    ais.armada.nu/api/recruitment
    Returns all open recruitments and information about availeble roles for each recruitment.
    If there areno open recrutiment it returns an empty list.
    """
    fair = Fair.objects.get(current=True)
    recruitments = RecruitmentPeriod.objects.filter(fair=fair)
    recruitments = list(
        filter(
            lambda rec: (rec.start_date < timezone.now())
            & (rec.end_date > timezone.now()),
            recruitments,
        )
    )  # Make sure only current recruitments are shown
    data = []
    for recruitment in recruitments:
        roles_info = dict()
        roles = recruitment.recruitable_roles.all()
        # Adds all roles available for this recruitment
        for role in roles:
            organization_group = (
                str(role.organization_group)
                if role.organization_group is not None
                else ""
            )
            role = OrderedDict(
                [
                    ("name", role.name),
                    ("parent", role.parent_role.name if role.parent_role else None),
                    ("description", role.description),
                ]
            )
            if organization_group in roles_info:
                roles_info[organization_group].append(role)
            else:
                roles_info[organization_group] = [role]

        data.append(
            OrderedDict(
                [
                    ("name", recruitment.name),
                    ("link", "/fairs/" + str(fair.year) + "/recruitment/"),
                    ("start_date", recruitment.start_date),
                    ("end_date", recruitment.end_date),
                    ("groups", roles_info),
                ]
            )
        )

    return JsonResponse(data, safe=False)


@permission_required("recruitment.view_recruitment_applications")
def recruitment_data(request):
    """
    ais.armada.nu/api/recruitment_data?fair_year={FAIR_YEAR}
    Returns anonymized statistics of recruitment applications as a CSV file.
    If FAIR_YEAR is unset, defaults to the current fair.
    If the fair year does not exist, return 500 error.
    """
    fair_year = request.GET.get("fair_year") or None
    if fair_year:
        try:
            fair = Fair.objects.get(year=fair_year)
        except:
            return HttpResponse(status=500)
    else:
        fair = Fair.objects.get(current=True)

    applications = RecruitmentApplication.objects.filter(
        recruitment_period__in=RecruitmentPeriod.objects.filter(fair=fair)
    )

    def with_profile(user, callback):
        if user.profile:
            return callback(user.profile)
        else:
            return None

    def get_questions(application):
        return application.recruitment_period.application_questions.questions_with_answer_arguments_for_user(
            application.user
        )

    data = [
        OrderedDict(
            chain(
                [
                    (question[0].__str__(), question[1].__str__())
                    for question in get_questions(app)
                ],
                [("preferred_role_%d" % i, role) for (i, role) in enumerate(app.roles)],
                [
                    ("rating", app.rating),
                    ("recommended_role", app.recommended_role),
                    ("status", app.status),
                    (
                        "profile_gender",
                        with_profile(app.user, lambda profile: profile.gender),
                    ),
                    (
                        "programme",
                        with_profile(
                            app.user,
                            lambda profile: (
                                profile.programme and profile.programme.name
                            )
                            or None,
                        ),
                    ),
                    (
                        "profile_preferred_language",
                        with_profile(
                            app.user,
                            lambda profile: (
                                profile.preferred_language
                                and profile.preferred_language.name
                            )
                            or None,
                        ),
                    ),
                ],
            )
        )
        for app in applications
    ]

    return json_to_csv_response("recruitment_data", data)
