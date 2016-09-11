from django.shortcuts import render, redirect
from recruitment.models import RecruitmentPeriod, Role

def index(request):
    next = request.GET.get('next')
    if next and next[-1] == '/':
        next = next[:-1]
    print(next)
    if request.user.is_authenticated():
       return render(request, 'home.html', {
           'recruitment_periods': RecruitmentPeriod.objects.all().order_by('-start_date'),
           'roles': [{'parent_role': role,
                      'child_roles': [child_role for child_role in Role.objects.all() if child_role.has_parent(role)]} for
                     role in Role.objects.filter(parent_role=None)],
       })
    return render(request, 'login.html', {'next': next})
# Create your views here.
