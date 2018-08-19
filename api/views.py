from collections import OrderedDict
from datetime import datetime

import platform, subprocess, json

from django.contrib.auth.models import Group
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.cache import cache_page

import api.serializers as serializers, api.deserializers as deserializers

from banquet.models import BanquetteAttendant
from events.models import Event
from exhibitors.models import Exhibitor, CatalogInfo
from fair.models import Partner, Fair
from django.utils import timezone
from matching.models import StudentQuestionBase as QuestionBase, WorkField, Survey
from news.models import NewsArticle
from recruitment.models import RecruitmentPeriod, RecruitmentApplication, Role
from student_profiles.models import StudentProfile, MatchingResult

def root(request):
    return JsonResponse({'message': 'Welcome to the Armada API!'})


@cache_page(60 * 5)
def exhibitors(request):
    '''
    Returns the existing cataloginfo for exhibitors in current fair.
    Does not return anything for those exhibitors that are without catalog info.
    '''
    fair = Fair.objects.get(current=True)
    exhibitors = Exhibitor.objects.filter(fair=fair).exclude(status='withdrawn')

    data = [serializers.exhibitor(request, exhibitor, exhibitor.company)
            for exhibitor in exhibitors]
    #data.sort(key=lambda x: x['company_name'].lower())
    return JsonResponse(data, safe=False)

@cache_page(60 * 5)
def events(request):
    '''
    Returns all events for this years fair
    '''
    fair = Fair.objects.get(current=True)
    events = Event.objects.filter(published=True, fair=fair)
    data = [serializers.event(request, event) for event in events]
    return JsonResponse(data, safe=False)



@cache_page(60 * 5)
def news(request):
    '''
    Returns all news
    '''
    news = NewsArticle.public_articles.all()
    data = [serializers.newsarticle(request, article) for article in news]
    return JsonResponse(data, safe=False)

@cache_page(60 * 5)
def partners(request):
    '''
    Returns all partners for current fair
    '''
    fair = Fair.objects.get(current=True)
    partners = Partner.objects.filter(
        fair=fair
    ).order_by('-main_partner')
    data = [serializers.partner(request, partner) for partner in partners]
    return JsonResponse(data, safe=False)

@cache_page(60 * 5)
def organization(request):
    '''
    Returns all roles for current fair
    '''
    all_groups = Group.objects \
        .prefetch_related('user_set__profile') \
        .order_by('name')

    # We only want groups that belong to roles that have been recruited during the current fair
    fair = Fair.objects.get(current=True)
    recruitment_period_roles = [period.recruitable_roles.all() for period in fair.recruitmentperiod_set.all()]
    role_groups = [role.group for roles in recruitment_period_roles for role in roles]
    groups = [group for group in all_groups if group in role_groups]

    data = [serializers.organization_group(request, group) for group in groups]
    return JsonResponse(data, safe=False)


def status(request):
    hostname = platform.node()
    python_version = platform.python_version()
    git_hash = subprocess.check_output('cd ~/git && git rev-parse HEAD', shell=True).decode("utf-8").strip()
    data = OrderedDict([
        ('status', "OK"),
        ('time', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        ('hostname', hostname),
        ('commit', git_hash),
        ('python_version', python_version),
    ])
    return JsonResponse(data, safe=False)

@cache_page(60 * 5)
def banquet_placement(request):
    '''
    Returns all banquet attendance for current fair.
    The field job_title depends on weather a attendant is a user or exhibitor.
    '''

    fair = get_object_or_404(Fair, current = True)

    banquet_attendees = BanquetteAttendant.objects.filter(fair=fair)

    recruitment_applications = RecruitmentApplication.objects.filter(status='accepted')
    data = []
    for attendence in banquet_attendees:
        if attendence.user:
            recruitment_application = recruitment_applications.filter(user=attendence.user).first()
            if recruitment_application:
                attendence.job_title = 'Armada: ' + recruitment_application.delegated_role.name
            try:
                if not attendence.linkedin_url & attendence.user.profile.linkedin_url:
                    attendence.linkedin_url = attendence.user.profile.linkedin_url
            except:
                pass
        if attendence.exhibitor:
            job_title = attendence.job_title
            attendence.job_title = attendence.exhibitor.company.name
            if job_title:
                attendence.job_title += ': ' + job_title

        data.append(serializers.banquet_placement(request, attendence))
    return JsonResponse(data, safe=False)


@csrf_exempt
def student_profile(request):
    '''
    GET student profiles nickname by their id.
    Url: /student_profile?student_id={STUDENTPROFILEID}
    or
    PUT student profile nickname by the id
    URL: /api/student_profile?student_id={STUDENT_PROFILE_ID}
    DATA: json'{"nickname" : "{NICKNAME}"}'
    '''
    if request.method == 'GET':
        student_id = request.GET['student_id']
        student = get_object_or_404(StudentProfile, pk=student_id)
        data = serializers.student_profile(student)
    elif request.method == 'PUT':
        if request.body:
            student_id = request.GET['student_id']
            (student_profile, wasCreated) = StudentProfile.objects.get_or_create(pk=student_id)
            try:
                data = json.loads(request.body.decode())
            except Exception:
                if wasCreated:
                    student_profile.delete()
                return HttpResponse('Misformatted json!', content_type='text/plain', status=406)
            # Here is where the actual deserialization happens:
            if deserializers.student_profile(data, student_profile):
                return HttpResponse('Profile updated sucessfully!', content_type='text/plain')
            else:
                if wasCreated:
                    student_profile.delete()
                return HttpResponse('Failed to update profile (deserialization error)!', content_type='text/plain', status=406)
        else:
            return HttpResponse('No payload detected!', content_type='text/plain', status=406)
    else:
        return HttpResponseBadRequest('Unsupported method!', content_type='text/plain')

    return JsonResponse(data, safe=False)


def questions_GET(request):
    '''
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
    '''
    current_fair = get_object_or_404(Fair, current=True)
    survey = get_object_or_404(Survey, fair=current_fair)
    questions = QuestionBase.objects.filter(survey=survey)
    areas = WorkField.objects.filter(survey=survey)
    data = OrderedDict([
        ('questions', [serializers.question(question) for question in questions]),
        ('areas', [serializers.work_area(area) for area in areas])
    ])
    return JsonResponse(data, safe=False)

def matching_result(request):
    '''
    ais.armada.nu/api/matching_result?student_id=STUDENT_PROFILE_PK
    returns the result for a student after the matching algorithm is done (=> when length of result is the same as MATCHING_DONE)
    The result is an array of MAX_MATCHES matching exhibitors.
    If there are no result yet, it will return an empty list [].
    '''
    MATCHING_DONE = 6
    MAX_MATCHES = 5
    current_fair = get_object_or_404(Fair, current=True)
    student_id = request.GET['student_id']
    try:
        student = StudentProfile.objects.get(pk=student_id)
    except StudentProfile.DoesNotExist:
        return HttpResponse('No such student', content_type='text/plain', status=404)

    number_of_matches = MatchingResult.objects.filter(student=student, fair=current_fair).count()
    if number_of_matches < MATCHING_DONE:
        data = None
    else:
        matches = MatchingResult.objects.filter(student=student).order_by('-score')[:MAX_MATCHES]
        data = [serializers.matching_result(matching) for matching in matches]

    return JsonResponse(data, safe=False)

def intChoices(objectType, data, student, survey, function):
    '''
    help function for questions_PUT. Checks if there data has an objectType with a list of Integers.
    Returns the list and True if the list is valid.
    '''
    allChosen = [];
    for chosen in data[objectType]:
        if type(chosen) is int:
            allChosen.append(chosen)
    function(allChosen, student, survey)
    return allChosen


def questions_PUT(request):
    '''
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
    '''
    if request.body:
        student_id = request.GET['student_id']
        (student, wasCreated) = StudentProfile.objects.get_or_create(pk=student_id)
        fair = get_object_or_404(Fair, current=True)
        survey = get_object_or_404(Survey, fair=fair)
        try:
            data = json.loads(request.body.decode())
        except Exception:
            if wasCreated:
                student.delete()
            return HttpResponse('Misformatted json!', content_type='text/plain', status=406)
        modified = False
        (modified_count, total_count) = (0, 0)

        if type(data) is not dict:
            return HttpResponse('Wrong payload format!', content_type='text/plain', status=406)

        if 'questions' in data and type(data['questions']) is list:
            (modified_count, total_count) = deserializers.answers(data['questions'], student, survey)

        if 'areas' in data and type(data['areas']) is list:
            intChoices('areas', data, student, survey, deserializers.fields)
            modified = True
        if 'regions' in data and type(data['regions']) is list:
            intChoices('regions', data, student, survey, deserializers.regions)
            modified = True
        if 'continents' in data and type(data['continents']) is list:
            intChoices('continents', data, student, survey, deserializers.continents)
            modified = True
        if 'looking_for' in data and type(data['looking_for']) is list:
            intChoices('looking_for', data, student, survey, deserializers.jobtype)
            modified = True

        if modified or modified_count > 0:
            answer = 'Answers submitted! (' + str(modified_count) + '/' + str(total_count) + ' question answers were saved, fields were '
            if not modified:
                answer += 'not '
            answer += 'updated)'
            return HttpResponse(answer, content_type='text/plain')
        else:
            if wasCreated:
                student.delete()
            return HttpResponse('No answers were found in payload!', content_type='text/plain', status=406)
    else:
        return HttpResponse('No payload detected!', content_type='text/plain', status=406)


@csrf_exempt
def questions(request):
    '''
    ais.armada.nu/api/questions
    Handles GET request with questions_GET
    Handles PUT request with questions_PUT
    '''
    if request.method == 'GET':
        return questions_GET(request)
    elif request.method == 'PUT':
        return questions_PUT(request)
    else:
        return HttpResponseBadRequest('Unsupported method!', content_type='text/plain')


def recruitment(request):
    '''
    ais.armada.nu/api/recruitment
    Returns all open recruitments and information about availeble roles for each recruitment.
    If there areno open recrutiment it returns an empty list.
    '''
    fair = Fair.objects.get(current=True)
    recruitments = RecruitmentPeriod.objects.filter(fair=fair)
    recruitments = list(filter(lambda rec: (rec.start_date < timezone.now()) & (rec.end_date > timezone.now()), recruitments)) #Make sure only current recruitments are shown
    data = []
    for recruitment in recruitments:
        roles_info = dict()
        roles = recruitment.recruitable_roles.all()
        #Adds all roles available for this recruitment
        for role in roles:
            organization_group = role.organization_group
            if organization_group == None or organization_group =='':
                organization_group = 'Other'
            role = OrderedDict([
                    ('name', role.name),
                    ('parent', role.parent_role.name if role.parent_role else None),
                    ('description', role.description),
                    ])
            if organization_group in roles_info:
                roles_info[organization_group].append(role)
            else:
                roles_info[organization_group] = [role]

        data.append(OrderedDict([
            ('name', recruitment.name),
            ('link', '/fairs/' + str(fair.year) + '/recruitment/'),
            ('start_date', recruitment.start_date),
            ('end_date', recruitment.end_date),
            ('groups', roles_info),
            ]))

    return JsonResponse(data, safe=False)
