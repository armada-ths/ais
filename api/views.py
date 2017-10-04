from collections import OrderedDict
from datetime import datetime
import platform
import subprocess

from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404

import api.serializers as serializers
from events.models import Event     
from exhibitors.models import Exhibitor, CatalogInfo
from fair.models import Partner, Fair
from django.utils import timezone
from news.models import NewsArticle
from exhibitors.models import BanquetteAttendant
from recruitment.models import RecruitmentPeriod, RecruitmentApplication, Role 


def root(request):
    return JsonResponse({'message': 'Welcome to the Armada API!'})


@cache_page(60 * 5)
def exhibitors(request):
    '''
    Returns the existing cataloginfo for exhibitors in current fair. 
    Does not return anything for those exhibitors that are without catalog info.
    '''
    fair = Fair.objects.get(current=True)
    cataloginfos = CatalogInfo.objects.filter(exhibitor__in = Exhibitor.objects.filter(fair=fair)).prefetch_related(
        'programs',
        'main_work_field',
        'work_fields',
        'job_types',
        'continents',
        'values',
    )
    data = [serializers.exhibitor(request, cataloginfo)
            for cataloginfo in cataloginfos]
    data.sort(key=lambda x: x['name'].lower())
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
    Returns all banquet attendance. 
    The field hob_title depends on weather a attendant is a user or exhibitor.
    '''
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
            #if not attendence.linkedin_url & attendence.user.profile.linkedin_url:
            #    attendence.linkedin_url = attendence.user.profile.linkedin_url
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






