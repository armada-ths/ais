from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.template.defaultfilters import date as date_filter
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

import json
import requests as r

from fair.models import Fair
from people.models import Profile
from companies.models import Company
from exhibitors.models import Exhibitor
from .models import RecruitmentPeriod, RecruitmentApplication, RoleApplication, RecruitmentApplicationComment, Role, \
    create_project_group, Programme, CustomFieldArgument, CustomFieldAnswer


from django.forms import modelform_factory
from django import forms
from .forms import RoleApplicationForm, RecruitmentPeriodForm, RecruitmentApplicationSearchForm, \
    RolesForm, ProfileForm, ProfilePictureForm


def import_members(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    create_project_group()
    return redirect('recruitment')

def assign_roles(request, year):
    if not request.user.has_perm('recruitment.administer_roles'):
        return HttpResponseForbidden()

    # Save all roles because that will guarantee that all roles have a group
    for role in Role.objects.all():
        role.save()

    # Remove permission groups from everyone that does not have a role this year
    for application in RecruitmentApplication.objects.all().exclude(recruitment_period__fair__year=year, delegated_role=None):
        application.user.groups.clear()
        application.user.user_permissions.clear()
    # There should be no accepted applications without a delegated role, if there is one then recruitment manager has messed up
    # But we don't want this to crash if that's case so exclude all without a delegated role
    for application in RecruitmentApplication.objects.filter(recruitment_period__fair__year=year, status='accepted').exclude(delegated_role=None):
        application.delegated_role.add_user_to_groups(application.user)

    return redirect('recruitment', year)


def recruitment(request, year, template_name='recruitment/recruitment.html'):
    fair = get_object_or_404(Fair, year=year)

    recruitment_periods = RecruitmentPeriod.objects.filter(fair=fair).order_by('-start_date')
    roles = []
    for period in recruitment_periods:
        for role in period.recruitable_roles.all():
            roles.append(role)



    return render(request, template_name, {
        'recruitment_periods': RecruitmentPeriod.objects.filter(fair=fair).order_by('-start_date'),
        'fair': fair,
        'roles': [{'parent_role': role,
                   'child_roles': [child_role for child_role in roles if child_role.has_parent(role)]} for
                  role in Role.objects.filter(parent_role=None)],
    })



def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timezone.timedelta(n)


import time
from django.http import JsonResponse

@permission_required('recruitment.view_recruitment_applications', raise_exception=True)
def interview_state_counts(request, year, pk):
    recruitment_period = get_object_or_404(RecruitmentPeriod, pk=pk)
    application_list = recruitment_period.recruitmentapplication_set.order_by(
        '-submission_date').all().prefetch_related('roleapplication_set')

    ignored_application_states = ['new', 'accepted', 'rejected']
    interview_count_states = [state for state in recruitment_period.state_choices() if
                              state[0] not in ignored_application_states]

    interview_state_count_map = {}

    for interviewer in recruitment_period.interviewers():
        interview_state_count_map[interviewer] = dict([(state[0], 0) for state in interview_count_states])

    for application in application_list:
        if application.interviewer:
            if not application.interviewer in interview_state_count_map:
                interview_state_count_map[application.interviewer] = dict([(state[0], 0) for state in interview_count_states])

            application_state = application.state()
            if application_state in interview_state_count_map[application.interviewer]:
                interview_state_count_map[application.interviewer][application_state] += 1



    return JsonResponse({
        'data': [dict([('name', interviewer.get_full_name())] + [(state_name, state_count) for state_name,state_count in state_counts.items()] + [('total', sum(state_counts.values()))]) for interviewer,state_counts in interview_state_count_map.items()]
    })


@permission_required('recruitment.view_recruitment_applications', raise_exception=True)
def recruitment_period_graphs(request, year, pk):
    start = time.time()
    recruitment_period = get_object_or_404(RecruitmentPeriod, pk=pk)
    application_list = recruitment_period.recruitmentapplication_set.order_by('-submission_date').all().prefetch_related('roleapplication_set')

    # Graph stuff :)
    class ValueCounter(object):
        def __init__(self, description, monocolor, charts, values=None, sort_key=None):
            self.data = {}
            self.description = description
            self.monocolor = monocolor
            self.charts = charts
            self.sort_key = sort_key
            self.y_limit = None

            if values:
                self.add_values(values)

        def add_value(self, value):
            if not value in self.data:
                self.data[value] = 0
            self.data[value] += 1

        def add_values(self, values):
            for value in values:
                self.add_value(value)

        def sorted_values(self):
            return sorted(self.data.keys(), key=self.sort_key)

        def sorted_value_counts(self):
            return [self.data[key] for key in self.sorted_values()]

        def json(self):
            return {
                'description': self.description,
                'monocolor': self.monocolor,
                'charts': self.charts,
                'sorted_values': self.sorted_values(),
                'sorted_value_counts': self.sorted_value_counts(),
                'y_limit': self.y_limit,
            }

    date_dictionary = dict([(date_filter(application.submission_date, "d M"), application.submission_date) for application in application_list])
    applications_per_date_count = ValueCounter(
        'Applications per date',
        True,
        ['bar'],
        [date_filter(application.submission_date, "d M") for application in application_list],
        lambda x: date_dictionary[x]
    )

    role_applications = RoleApplication.objects.filter(recruitment_application__recruitment_period=recruitment_period).prefetch_related('role')

    total_role_application_count = ValueCounter(
        'Total number of applications per role',
        False,
        ['bar', 'pie'],
        [role_application.role.name for role_application in role_applications]
    )

    first_preference_role_application_count = ValueCounter(
        'Number of first preference applications per role',
        False,
        ['bar', 'pie'],
        [role_application.role.name for role_application in role_applications.filter(order=0)]
    )

    # Add graphs also for application questions where users select from a fixed set of arguments
    custom_field_counts = []
    for custom_field in recruitment_period.application_questions.customfield_set.all():
        try:
            arguments = custom_field.customfieldargument_set.all()
            if len(arguments) > 0:
                custom_field_count = ValueCounter(
                    custom_field.question,
                    False,
                    ['bar'],
                    [arguments.get(pk=int(answer.answer)).value for answer in custom_field.customfieldanswer_set.all()]
                )
                custom_field_counts.append(custom_field_count)

                # Also, for each argument we want to plot bar graphs so we can see the number of english or swedish applicants per date
                argument_per_date_counts = []
                y_limit = 0
                for argument in arguments:
                    date_dictionary = dict(
                        [(date_filter(application.submission_date, "d M"), application.submission_date) for application in
                         application_list])

                    argument_per_date_count = ValueCounter(
                        argument.value,
                        True,
                        ['bar'],
                        [date_filter(application.submission_date, "d M") for application in application_list if CustomFieldAnswer.objects.filter(user=application.user, answer=str(argument.pk)).exists()],
                        lambda x: date_dictionary[x]
                    )

                    for date in daterange(recruitment_period.start_date, min(timezone.now(), recruitment_period.end_date)):
                        date_string = date_filter(date, "d M")
                        if not date_string in argument_per_date_count.data:
                            argument_per_date_count.data[date_string] = 0
                            date_dictionary[date_string] = date

                    y_limit = max(y_limit, max(argument_per_date_count.data.values()))
                    argument_per_date_counts.append(argument_per_date_count)

                for argument_per_date_count in argument_per_date_counts:
                    argument_per_date_count.y_limit = y_limit
                    custom_field_counts.append(argument_per_date_count)

        except (ValueError, ObjectDoesNotExist):
            print('Custom field error: %s' % custom_field.question)

    print('Counting applications took', time.time() - start)

    def user_has_programme(user):
        try:
            return user.profile
        except ObjectDoesNotExist:
            return False

    programme_applications_count = ValueCounter(
        'Applications per programme',
        True,
        ['bar'],
        [application.user.profile.programme.name for application in application_list.prefetch_related('user', 'user__profile', 'user__profile__programme') if user_has_programme(application.user) and application.user.profile.programme]
    )

    print('Counting programmes took', time.time() - start)

    value_counters = [applications_per_date_count, total_role_application_count, first_preference_role_application_count, programme_applications_count] + custom_field_counts

    return JsonResponse({
        'graph_datasets': [value_counter.json() for value_counter in value_counters]
    })


from django.http import HttpResponseRedirect
import urllib

def remember_last_query_params(url_name, query_params):

    """Stores the specified list of query params from the last time this user
    looked at this URL (by url_name). Stores the last values in the session.
    If the view is subsequently rendered w/o specifying ANY of the query params,
    it will redirect to the same URL with the last query params added to the URL.

    url_name is a unique identifier key for this view or view type if you want
    to group multiple views together in terms of shared history

    Example:

    @remember_last_query_params("jobs", ["category", "location"])
    def myview(request):
        pass

    """

    def is_query_params_specified(request, query_params):
        """ Are any of the query parameters we are interested in on this request URL?"""
        for current_param in request.GET:
            if current_param in query_params:
                return True
        return False

    def params_from_last_time(request, key_prefix, query_params):
        """ Gets a dictionary of JUST the params from the last render with values """
        params = {}
        for query_param in query_params:
            last_value = request.session.get(key_prefix + query_param)
            if last_value:
                params[query_param] = last_value
        return params

    def update_url(url, params):
        """ update an existing URL with or without paramters to include new parameters
        from http://stackoverflow.com/questions/2506379/add-params-to-given-url-in-python
        """
        if not params:
            return url
        if not url: # handle None
            url = ""
        url_parts = list(urllib.parse.urlparse(url))
        # http://docs.python.org/library/urlparse.html#urlparse.urlparse, part 4 == params
        query = dict(urllib.parse.parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = urllib.parse.urlencode(query)
        return urllib.parse.urlunparse(url_parts)

    def do_decorator(view_func):

        def decorator(*args, **kwargs):

            request = args[0]

            key_prefix =  url_name + "_"

            if is_query_params_specified(request, query_params):
                for query_param in query_params:
                    request.session[key_prefix + query_param] = request.GET.get(query_param)

            else:
                last_params = params_from_last_time(request, key_prefix, query_params)
                if last_params and last_params != {}:
                    current_url = "%s?%s" % (request.META.get("PATH_INFO"), request.META.get("QUERY_STRING"))
                    new_url = update_url(current_url, last_params)
                    return HttpResponseRedirect(new_url)

            return view_func(*args, **kwargs)

        return decorator

    return do_decorator


@remember_last_query_params('recruitment', [field for field in RecruitmentApplicationSearchForm().fields])
def recruitment_period(request, year, pk, template_name='recruitment/recruitment_period.html'):
    fair = get_object_or_404(Fair, year=year)
    start = time.time()
    recruitment_period = get_object_or_404(RecruitmentPeriod, pk=pk)
    user = request.user

    # user should be forbidden to look at a
    # recruitment periods that include their application
    # unless they're in the Project Core Team
    if not user.groups.filter(name='Project Core Team').exists():
        try:
            current_users_applications = RecruitmentApplication.objects.filter(user=user)
            for a in current_users_applications:
                if recruitment_period.pk == a.recruitment_period.pk:
                    return HttpResponseForbidden()
        except (RecruitmentApplication.DoesNotExist):
            pass

    sort_field = request.GET.get('sort_field')
    if not sort_field:
        sort_field = 'submission_date'
    sort_ascending = request.GET.get('sort_ascending') == 'true'

    order_by_query = ('' if sort_ascending else '-') + sort_field
    application_list = recruitment_period.recruitmentapplication_set.order_by(order_by_query, '-submission_date').all().prefetch_related('roleapplication_set')

    search_form = RecruitmentApplicationSearchForm(request.GET or None)
    search_form.fields['interviewer'].choices = [('', '---------')] + [(interviewer.pk, interviewer.get_full_name()) for
                                                                       interviewer in recruitment_period.interviewers()]
    search_form.fields['state'].choices = [('', '-------')] + recruitment_period.state_choices()
    search_form.fields['recommended_role'].choices = [('', '---------')] + [(role.pk, role.name) for
                                                                       role in recruitment_period.recruitable_roles.all()]

    if search_form.is_valid():
        application_list = search_form.applications_matching_search(application_list)

    number_of_applications_per_page = 25
    paginator = Paginator(application_list, number_of_applications_per_page)
    page = request.GET.get('page')
    try:
        applications = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        applications = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        applications = paginator.page(paginator.num_pages)

    print('Total time took', time.time() - start)


    class SearchField(object):

        def __init__(self, name, model_field_name):
            self.name = name
            self.model_field_name = model_field_name


    search_fields = [
        SearchField('Name', 'user__last_name'),
        SearchField('Programme', 'user__profile__programme'),
        SearchField('Registration year', 'user__profile__registration_year'),
        SearchField('Rating', 'rating'),
        SearchField('Submitted', 'submission_date'),
        SearchField('Roles', None),
        SearchField('Recommended role', 'recommended_role'),
        SearchField('Interviewer', 'interviewer__last_name'),
        SearchField('State', None),
    ]

    return render(request, template_name, {
        'recruitment_period': recruitment_period,
        'application': recruitment_period.recruitmentapplication_set.filter(user=request.user).first(),
        'interviews': (recruitment_period.recruitmentapplication_set.filter(interviewer=request.user) | recruitment_period.recruitmentapplication_set.filter(user=request.user)).all(),
        'paginator': paginator,
        'applications': applications,
        'now': timezone.now(),
        'search_form': search_form,
        'search_fields': search_fields,
        'fair': fair,
    })


@permission_required('recruitment.administer_recruitment', raise_exception=True)
def recruitment_period_delete(request, year, pk):
    recruitment_period = get_object_or_404(RecruitmentPeriod, pk=pk)
    recruitment_period.delete()
    return redirect('recruitment', year)


@permission_required('recruitment.administer_recruitment', raise_exception=True)
def recruitment_period_edit(request, year, pk=None, template_name='recruitment/recruitment_period_new.html'):
    fair = get_object_or_404(Fair, year=year)
    recruitment_period = RecruitmentPeriod.objects.filter(pk=pk).first()
    form = RecruitmentPeriodForm(request.POST or None, instance=recruitment_period)

    if request.POST:
        if form.is_valid():
            recruitment_period = form.save(commit=False)
            recruitment_period.fair = fair
            recruitment_period.save()
            recruitment_period.interview_questions.handle_questions_from_request(request, 'interview_questions')
            recruitment_period.application_questions.handle_questions_from_request(request, 'application_questions')
            for role in Role.objects.all():
                role_key = 'role_%d' % role.id
                if role_key in request.POST:
                    if not role in recruitment_period.recruitable_roles.all():
                        recruitment_period.recruitable_roles.add(role)
                else:
                    recruitment_period.recruitable_roles.remove(role)
            recruitment_period.save()
            return redirect('recruitment_period', year=year, pk=recruitment_period.id)

    return render(request, template_name, {
        'form': form,
        'roles': [{'parent_role': role,
                   'child_roles': [child_role for child_role in Role.objects.all() if child_role.has_parent(role)]} for
                  role in Role.objects.filter(parent_role=None)],
        'recruitment_period': recruitment_period,
        'interview_questions': [] if not recruitment_period else recruitment_period.interview_questions.customfield_set.all(),
        'application_questions': [] if not recruitment_period else recruitment_period.application_questions.customfield_set.all(),
        'fair': fair
    })



def roles_new(request, year, pk=None, template_name='recruitment/roles_form.html'):
    fair = get_object_or_404(Fair, year=year)
    role = Role.objects.filter(pk=pk).first()
    roles_form = RolesForm(request.POST or None, instance=role)

    if request.user.has_perm('recruitment.administer_roles'):
        if roles_form.is_valid():
            roles_form.save()
            return redirect('recruitment', fair.year)

    users = [application.user for application in
             RecruitmentApplication.objects.filter(delegated_role=role, status='accepted')]
    return render(request, template_name, {
        'role': role,
        'users': users,
        'roles_form': roles_form,
        'fair': fair
    })


@permission_required('recruitment.administer_roles', raise_exception=True)
def roles_delete(request, year, pk):
    fair = get_object_or_404(Fair, year=year)
    role = get_object_or_404(Role, pk=pk)
    role.delete()
    return redirect('recruitment', fair.year)


def recruitment_application_comment_new(request, year, pk):
    fair = get_object_or_404(Fair, year=year)
    application = get_object_or_404(RecruitmentApplication, pk=pk)
    comment = RecruitmentApplicationComment()
    comment.user = request.user
    comment.recruitment_application = application
    comment.comment = request.POST['comment']
    comment.save()
    return redirect('recruitment_application_interview', fair.year, application.recruitment_period.pk, application.id)



def recruitment_application_new(request, year, recruitment_period_pk, pk=None,
                                template_name='recruitment/recruitment_application_new.html'):
    fair = get_object_or_404(Fair, year=year)
    recruitment_period = get_object_or_404(RecruitmentPeriod, pk=recruitment_period_pk)

    if not pk:
        recruitment_application = recruitment_period.recruitmentapplication_set.filter(user=request.user).first()

        # If the user already has an application for this period redirect to it
        if recruitment_application:
            return redirect('recruitment_application_new', fair.year, recruitment_period.pk, recruitment_application.pk)

    recruitment_application = RecruitmentApplication.objects.filter(pk=pk).first()

    user = recruitment_application.user if recruitment_application else request.user
    profile = Profile.objects.filter(user=user).first()
    if not profile:
        p = Profile(user=user)
        p.save()

    now = timezone.now()

    if recruitment_period.start_date > now:
        return render(request, 'recruitment/recruitment_application_closed.html', {
            'recruitment_period': recruitment_period,
            'message': 'Application has not opened',
            'fair': fair
        })

    if recruitment_period.end_date < now:
        return render(request, 'recruitment/recruitment_application_closed.html', {
            'recruitment_period': recruitment_period,
            'message': 'Application closed',
            'fair': fair
        })

    profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)

    role_form = RoleApplicationForm(request.POST or None)

    for i in range(1, 4):
        key = 'role%d' % i
        role_form.fields[key].queryset = recruitment_period.recruitable_roles
        if recruitment_application:
            role_application = RoleApplication.objects.filter(
                recruitment_application=recruitment_application,
                order=i - 1
            ).first()
            if role_application:
                role_form.fields[key].initial = role_application.role.pk

    if request.POST:
        recruitment_period.application_questions.handle_answers_from_request(request, user)

        if role_form.is_valid() and profile_form.is_valid():

            if not recruitment_application:
                recruitment_application = RecruitmentApplication()

            recruitment_application.user = user
            recruitment_application.recruitment_period = recruitment_period
            recruitment_application.save()

            recruitment_application.roleapplication_set.all().delete()
            for i in range(1, 4):
                key = 'role%d' % i
                role = role_form.cleaned_data[key]
                if role:
                    RoleApplication.objects.create(
                        recruitment_application=recruitment_application,
                        role=role,
                        order=i - 1
                    )

            if pk == None: #Slack webhook for signup notifications

                r.post(settings.RECRUITMENT_HOOK_URL,
                        data=json.dumps({'text': ' {!s} {!s} just applied for {!s}!'.format(user.first_name, user.last_name, role_form.cleaned_data["role1"])}))

            profile_form.save()
            return redirect('recruitment_period', fair.year, recruitment_period.pk)

    return render(request, template_name, {
        'application_questions_with_answers': recruitment_period.application_questions.questions_with_answers_for_user(
            recruitment_application.user if recruitment_application else None),
        'recruitment_period': recruitment_period,
        'profile_form': profile_form,
        'profile': profile,
        'role_form': role_form,
        'new_application': pk == None,
        'fair': fair,
    })


def set_foreign_key_from_request(request, model, model_field, foreign_key_model):
    if model_field in request.POST:
        try:
            foreign_key_id = int(request.POST[model_field])
            role = foreign_key_model.objects.filter(id=foreign_key_id).first()
            setattr(model, model_field, role)
            model.save()
        except ValueError:
            setattr(model, model_field, None)
            model.save()


def set_int_key_from_request(request, model, model_field):
    if model_field in request.POST:
        try:
            setattr(model, model_field, int(request.POST[model_field]))
            model.save()
        except ValueError:
            setattr(model, model_field, None)
            model.save()


def set_string_key_from_request(request, model, model_field):
    if model_field in request.POST:
        try:
            setattr(model, model_field, request.POST[model_field])
            model.save()
        except (ValueError, ValidationError) as e:
            setattr(model, model_field, None)
            model.save()


def set_image_key_from_request(request, model, model_field, file_directory):
    image_key = model_field
    if image_key in request.FILES:
        try:
            file = request.FILES[image_key]
            file_extension = file.name.split('.')[-1]
            if file_extension in ['png', 'jpg', 'jpeg']:
                file_path = '%s/%d/image.%s' % (file_directory, model.pk, file_extension)
                if default_storage.exists(file_path):
                    default_storage.delete(file_path)
                default_storage.save(file_path, ContentFile(file.read()))
                setattr(model, model_field, file_path)
                model.save()
        except (ValueError, ValidationError) as e:
            setattr(model, model_field, None)
            model.save()



def recruitment_application_interview(request, year, recruitment_period_pk, pk, template_name='recruitment/recruitment_application_interview.html'):
    fair = get_object_or_404(Fair, year=year)
    application = get_object_or_404(RecruitmentApplication, pk=pk)
    user = request.user
    if not user.has_perm('recruitment.view_recruitment_interviews') and application.interviewer != user:
        return HttpResponseForbidden()

    # user should be forbidden to look at an interview
    # within recruitment periods that include their application
    # unless they're in the Project Core Team
    if not user.groups.filter(name='Project Core Team').exists():
        try:
            current_users_applications = RecruitmentApplication.objects.filter(user=user)
            for a in current_users_applications:
                if application.recruitment_period.pk == a.recruitment_period.pk:
                    return HttpResponseForbidden()
        except (RecruitmentApplication.DoesNotExist):
            pass

    exhibitors = [participation.company for participation in
                  Exhibitor.objects.filter(fair=application.recruitment_period.fair)]

    InterviewPlanningForm = modelform_factory(
        RecruitmentApplication,
        fields=('interviewer', 'interview_date', 'interview_location', 'recommended_role', 'scorecard', 'drive_document',
                'rating') if request.user.has_perm('recruitment.administer_recruitment_applications') else (
        'interview_date', 'interview_location', 'recommended_role', 'scorecard', 'drive_document', 'rating'),
        widgets={
            'rating': forms.Select(choices=[('', '---------')] + [(i, i) for i in range(1, 6)]),
            'interview_date': forms.DateTimeInput(format='%Y-%m-%d %H:%M', attrs = {'placeholder' : 'YYYY-MM-DD hh:mm'}),
            'scorecard' : forms.TextInput(attrs = {'placeholder' : 'Link to existing document'}),
            'drive_document' : forms.TextInput(attrs = {'placeholder' : 'Link to existing document'}),
        }
    )

    profile_pic_form = None
    if Profile.objects.filter(user=application.user).first():
        profile_pic_form = ProfilePictureForm(request.POST or None, request.FILES or None, instance=Profile.objects.get(user=application.user))

    interviewers = application.recruitment_period.interviewers()
    interview_planning_form = InterviewPlanningForm(request.POST or None, instance=application)
    interview_planning_form.fields['recommended_role'].queryset = application.recruitment_period.recruitable_roles
    if 'interviewer' in interview_planning_form.fields:
        interview_planning_form.fields['interviewer'].choices = [('', '---------')] + [
            (interviewer.pk, interviewer.get_full_name()) for interviewer in interviewers]

    RoleDelegationForm = modelform_factory(
        RecruitmentApplication,
        fields=('delegated_role', 'exhibitor', 'superior_user', 'status'),
    )
    if request.user.has_perm('recruitment.administer_recruitment_applications'):
        role_delegation_form = RoleDelegationForm(request.POST or None, instance=application)
        role_delegation_form.fields['delegated_role'].queryset = application.recruitment_period.recruitable_roles
        role_delegation_form.fields['superior_user'].choices = [('', '---------')] + [
            (interviewer.pk, interviewer.get_full_name()) for interviewer in interviewers]
        role_delegation_form.fields['exhibitor'].choices = [('', '---------')] + [
            (exhibitor.pk, exhibitor.name) for exhibitor in exhibitors]
    else:
        role_delegation_form = None

    if request.POST and (
            application.interviewer == request.user or request.user.has_perm('recruitment.administer_recruitment_applications')):
        application.recruitment_period.interview_questions.handle_answers_from_request(request, application.user)
        if interview_planning_form.is_valid():
            interview_planning_form.save()

            if role_delegation_form:
                if role_delegation_form.is_valid():
                    role_delegation_form.save()
                    return redirect('recruitment_period', fair.year, application.recruitment_period.pk)
            else:
                return redirect('recruitment_period', fair.year, application.recruitment_period.pk)

    return render(request, template_name, {
        'profile_pic_form': profile_pic_form,
        'application': application,
        'application_questions_with_answers': application.recruitment_period.application_questions.questions_with_answers_for_user(
            application.user),
        'interview_questions_with_answers': application.recruitment_period.interview_questions.questions_with_answers_for_user(
            application.user),
        'interview_planning_form': interview_planning_form,
        'role_delegation_form': role_delegation_form,
        'fair': fair,
    })


@permission_required('recruitment.administer_recruitment_applications', raise_exception=True)
def recruitment_application_delete(request, year, pk):
    fair = get_object_or_404(Fair, year=year)
    recruitment_application = get_object_or_404(RecruitmentApplication, pk=pk)
    recruitment_application.delete()
    return redirect('recruitment_period', fair.year, recruitment_application.recruitment_period.pk)
