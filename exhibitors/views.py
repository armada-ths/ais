from django.forms import modelform_factory
from .models import Exhibitor
from recruitment.models import RecruitmentApplication
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required

@permission_required('exhibitors.change_exhibitor', raise_exception=True)
def exhibitors(request, template_name='exhibitors/exhibitors.html'):
	return render(request, template_name, {'exhibitors': Exhibitor.objects.all().order_by('company__name')})


@permission_required('exhibitors.change_exhibitor', raise_exception=True)
def exhibitor(request, pk, template_name='exhibitors/exhibitor.html'):
	exhibitor = get_object_or_404(Exhibitor, pk=pk)
	ExhibitorForm = modelform_factory(
		Exhibitor,
		exclude=('company', 'fair')
	)
	exhibitor_form = ExhibitorForm(request.POST or None, instance=exhibitor)
	if exhibitor_form.is_valid():
		exhibitor_form.save()
		return redirect('exhibitors')

	users = [(recruitment_application.user, recruitment_application.delegated_role)  for recruitment_application in RecruitmentApplication.objects.filter(status='accepted').order_by('user__first_name', 'user__last_name')]


	exhibitor_form.fields['hosts'].choices = [('', '---------')] + [(user[0].pk, user[0].get_full_name() + ' - ' + user[1].name) for
																		  user in users]

	return render(request, template_name, {
		'exhibitor': exhibitor,
		'exhibitor_form': exhibitor_form
	})

