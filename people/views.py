from django.shortcuts import render, redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from django.utils import timezone
from django import forms
from django.core.exceptions import PermissionDenied
from django.forms import ModelForm
from django.contrib.auth.decorators import permission_required

from fair.models import Fair, OrganizationGroup
from recruitment.models import RecruitmentApplication, RecruitmentPeriod

from .models import Profile
from .forms import ProfileForm


def list(request, year):
	fair = get_object_or_404(Fair, year = year)
	
	total = 0
	
	organization_groups = []
	
	users = RecruitmentApplication.objects.select_related('user').filter(delegated_role__organization_group = None, status = 'accepted', recruitment_period__fair = fair).order_by('recruitment_period__start_date', 'delegated_role', 'user__first_name', 'user__last_name')
	
	total = len(users)
	
	if total > 0:
		organization_groups.append({
			'name': None,
			'users': users
		})
	
	i = 0
	
	for organization_group in OrganizationGroup.objects.filter(fair = fair):
		users = RecruitmentApplication.objects.select_related('user').filter(delegated_role__organization_group = organization_group, status = 'accepted', recruitment_period__fair = fair).order_by('delegated_role__organization_group', 'recruitment_period__start_date', 'delegated_role', 'user__first_name', 'user__last_name')
		
		organization_groups.append({
			'i': i,
			'name': organization_group.name,
			'users': users
		})
		
		i += 1
		total += len(users)
	
	return render(request, 'people/list.html', {
		'fair': fair,
		'organization_groups': organization_groups,
		'total': total,
		'recruitment_periods': RecruitmentPeriod.objects.filter(fair = fair)
	})


def profile(request, year, pk):
	fair = get_object_or_404(Fair, year = year)
	user = get_object_or_404(User, pk = pk)
	
	profile = Profile.objects.filter(user = user).first()
	
	if not profile: profile = Profile.objects.create(user = user, no_dietary_restrictions = False)
	
	application = RecruitmentApplication.objects.filter(user = user, status = 'accepted', recruitment_period__fair = fair).first()
	
	return TemplateResponse(request, 'people/profile.html', {
		'fair': fair,
		'profile': profile,
		'role': application.delegated_role if application else None,
		'roles': RecruitmentApplication.objects.filter(user = user, status = 'accepted').order_by('recruitment_period__fair')
	})

def profile_delete(request, year, pk):
	fair = get_object_or_404(Fair, year = year)
	user = request.session['user']

	if request.method == 'POST':
		Profile.objects.filter(user = request.user).delete()
		User.objects.filter(pk = pk).delete()
		return redirect('/accounts/logout?next=/register')
	
	profile = Profile.objects.filter(user = user).first()
	
	return TemplateResponse(request, 'people/profile.html', {
			'fair': fair,
			'profile': profile,
			'roles': RecruitmentApplication.objects.filter(user = user, status = 'accepted').order_by('recruitment_period__fair')
		})


def edit(request, year):
	fair = get_object_or_404(Fair, year = year)
	
	profile = Profile.objects.filter(user = request.user).first()
	
	if not profile: profile = Profile.objects.create(user = request.user)
	
	form = ProfileForm(request.POST or None, request.FILES or None, instance = profile)
	
	if form.is_valid():
		form.save()
		return redirect('people:profile', fair.year, request.user.pk)
	
	application = RecruitmentApplication.objects.filter(recruitment_period__fair = fair, user = request.user, status = 'accepted').first()
	
	return TemplateResponse(request, 'people/edit.html', {
		'fair': fair,
		'profile': profile,
		'role': application.delegated_role if application else None,
		'form': form
	})

