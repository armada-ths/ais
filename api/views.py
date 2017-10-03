from collections import OrderedDict
from datetime import datetime
import platform
import subprocess

from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.utils import timezone

import api.serializers as serializers
from events.models import Event
from exhibitors.models import Exhibitor
from fair.models import Partner, Fair
from news.models import NewsArticle
from exhibitors.models import BanquetteAttendant
from recruitment.models import RecruitmentPeriod, RecruitmentApplication, Role 


CURRENT_FAIR = 'Armada 2016'


def root(request):
    return JsonResponse({'message': 'Welcome to the Armada API!'})


@cache_page(60 * 5)
def exhibitors(request):
    exhibitors = Exhibitor.objects.filter(
        fair__name=CURRENT_FAIR
    ).select_related('cataloginfo').prefetch_related(
        'cataloginfo__programs',
        'cataloginfo__main_work_field',
        'cataloginfo__work_fields',
        'cataloginfo__job_types',
        'cataloginfo__continents',
        'cataloginfo__values',
    )
    data = [serializers.exhibitor(request, exhibitor.cataloginfo)
            for exhibitor in exhibitors]
    data.sort(key=lambda x: x['name'].lower())
    return JsonResponse(data, safe=False)


@cache_page(60 * 5)
def events(request):
    events = Event.objects.filter(published=True)
    data = [serializers.event(request, event) for event in events]
    return JsonResponse(data, safe=False)


@cache_page(60 * 5)
def news(request):
    news = NewsArticle.public_articles.all()
    data = [serializers.newsarticle(request, article) for article in news]
    return JsonResponse(data, safe=False)


@cache_page(60 * 5)
def partners(request):
    partners = Partner.objects.filter(
        fair__name=CURRENT_FAIR
    ).order_by('-main_partner')
    data = [serializers.partner(request, partner) for partner in partners]
    return JsonResponse(data, safe=False)


@cache_page(60 * 5)
def organization(request):
    all_groups = Group.objects \
        .prefetch_related('user_set__profile') \
        .order_by('name')

    # We only want groups that belong to roles that have been recruited during the current fair
    fair = Fair.objects.get(name=CURRENT_FAIR)
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
    # Tables and seats are mocked with this index, remove when implemented
    index = 0
    banquet_attendees = BanquetteAttendant.objects.all()

    recruitment_applications = RecruitmentApplication.objects.filter(status='accepted')
    data = []
    for attendence in banquet_attendees:
        if attendence.user:
            recruitment_application = recruitment_applications.filter(user=attendence.user).first()
            if recruitment_application:
                attendence.job_title = 'Armada: ' + recruitment_application.delegated_role.name
            if not attendence.linkedin_url:
                attendence.linkedin_url = attendence.user.profile.linkedin_url
        if attendence.exhibitor:
            job_title = attendence.job_title
            attendence.job_title = attendence.exhibitor.company.name
            if job_title:
                attendence.job_title += ': ' + job_title


        data.append(serializers.banquet_placement(request, attendence, index))
        index += 1
    return JsonResponse(data, safe=False)



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
        roles_info = []
        roles = recruitment.recruitable_roles.all()
        #Adds all roles available for this recruitment
        for role in roles:
            roles_info.append(OrderedDict([
                ('name', role.name),
                ('parent', role.parent_role.name),
                ('description', role.description),
                ]))
        data.append(OrderedDict([
            ('name', recruitment.name),
            ('start date', recruitment.start_date),
            ('end date', recruitment.end_date),
            ('roles', roles_info),
            ]))

    return JsonResponse(data, safe=False)






