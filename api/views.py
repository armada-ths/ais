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
from exhibitors.models import Exhibitor
from fair.models import Partner
from news.models import NewsArticle
from exhibitors.models import BanquetteAttendant
from fair.models import Fair

fair = get_object_or_404(Fair, current=True)


def root(request):
    return JsonResponse({'message': 'Welcome to the Armada API!'})


@cache_page(60 * 5)
def exhibitors(request):
    exhibitors = Exhibitor.objects.filter(
        fair=fair
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
        fair=fair
    ).order_by('-main_partner')
    data = [serializers.partner(request, partner) for partner in partners]
    return JsonResponse(data, safe=False)


@cache_page(60 * 5)
def organization(request):
    all_groups = Group.objects \
        .prefetch_related('user_set__profile') \
        .order_by('name')

    # We only want groups that belong to roles that have been recruited during the current fair
    fair = get_object_or_404(Fair, current=True)
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

    from recruitment.models import RecruitmentApplication
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
