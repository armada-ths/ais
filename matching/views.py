from django.contrib.auth.models import User

from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Min, Max

from .models import *
from companies.models import Company
from exhibitors.models import Exhibitor
from fair.models import Fair
from student_profiles.models import StudentProfile, MatchingResult

from .forms import RawQuestionForm, StudentQuestionForm, MapSubAreaForm, MapSwedenForm, WorkFieldForm

from collections import Counter

from .helpers_view import update_processed_question, delete_processed_question

from .process_data import processExhibitorAnswers as pea
from .algorithms import main_classify as classify

from .tasks import create_random_user
def test_matching(request, total):
    for i in range(int(total)):
        create_random_user.delay()
    return redirect('/')

@staff_member_required
def index(request, template_name='matching/index.html'):
    '''
    A lightweight index view displaying the company questions.
    User may pick which questions to use to generate the matching questions
    for students.

    Returns 404 if current fair does not exist or exhibitor-matching survey does
    not exist.
    '''
    #change this so the user can pick which survey to edit or create a new one
    name_survey_raw = 'exhibitor-matching'

    fair = get_object_or_404(Fair, current=True)
    exhibitors = Exhibitor.objects.filter(fair=fair)
    survey_raw = get_object_or_404(Survey, fair=fair, name=name_survey_raw)
    # get the id of the raw survey used so we can pass it between the views
    request.session['survey_raw_id'] = survey_raw.id
    try:
        survey_proc = Survey.objects.get(fair=fair, relates_to=survey_raw)
    except Survey.DoesNotExist:
        survey_proc = Survey.objects.create(fair=fair,
            name='%s-processed'%name_survey_raw,
            description='processed data for %s'%name_survey_raw,
            relates_to=survey_raw
        )
    # get the id of the processed survey used so we can pass it between the views
    request.session['survey_proc_id'] = survey_proc.id

    exhibitor_slider = Question.objects.filter(survey=survey_raw, question_type=Question.INT)
    exhibitor_grading = Question.objects.filter(survey=survey_raw, question_type = Question.SELECT)

    current_student_slider = StudentQuestionSlider.objects.filter(survey=survey_proc, company_question__in=exhibitor_slider)
    current_student_grading = StudentQuestionGrading.objects.filter(survey=survey_proc, company_question__in=exhibitor_grading)

    form = RawQuestionForm(
        request.POST or None,
        exhibitor_slider=exhibitor_slider,
        exhibitor_grading=exhibitor_grading,
        current_student_slider=current_student_slider,
        current_student_grading=current_student_grading,
    )
    if form.is_valid():
        selected_ex_slider = form.cleaned_data['questions_select_slider']
        selected_ex_grading = form.cleaned_data['questions_select_grading']
        # update or delete selected questions
        update_processed_question(selected_ex_slider, survey_proc)
        delete_processed_question(selected_ex_slider, survey_proc,'slider')
        update_processed_question(selected_ex_grading, survey_proc)
        delete_processed_question(selected_ex_grading, survey_proc, 'grading')

    return render(request, template_name, {'survey': survey_raw, 'form': form})

@staff_member_required
def init_choosen_sliders_gradings(request, template_name='matching/sliders_gradings.html'):
    '''
    edit questions text for student for choosen sliders and gradings
    '''
    fair = Fair.objects.get(current=True)
    survey_raw = Survey.objects.get(pk=request.session.get('survey_raw_id'))
    survey_proc = Survey.objects.get(pk=request.session.get('survey_proc_id'))

    slider_questions = StudentQuestionSlider.objects.filter(survey=survey_proc)
    #slider_ex_responses = Response.objects.filter(survey=survey_raw, question__in=[q.company_question for q in slider_questions])
    grading_questions = StudentQuestionGrading.objects.filter( survey=survey_proc)
    #grading_ex_responses = Response.objects.filter(survey=survey_raw, question__in=[q.company_question for q in grading_questions])
    slider_prefix = 'slider_question_'
    grading_prefix = 'grading_question_'

    form = StudentQuestionForm(
        request.POST or None,
        survey_raw = survey_raw,
        survey_proc = survey_proc,
        slider_questions=slider_questions,
        grading_questions = grading_questions,
        slider_prefix = slider_prefix,
        grading_prefix = grading_prefix,
    )
    if form.is_valid():
        for sq in slider_questions:
            sq.question = form.cleaned_data['%s%i'%(slider_prefix, sq.pk)]
            ex_responses = Response.objects.filter(question=sq.company_question, survey=survey_raw)
            sq.min_value = float(list(IntegerAns.objects.filter(response__in=ex_responses).aggregate(Min('ans')).values())[0])
            sq.max_value = float(list(IntegerAns.objects.filter(response__in=ex_responses).aggregate(Max('ans')).values())[0])
            sq.step = sq.max_value - sq.min_value
            sq.save()
            print(sq.min_value)
            print(sq.max_value)

        for gq in grading_questions:
            gq.question = form.cleaned_data['%s%i'%(grading_prefix, gq.pk)]
            gq.save()

    return render(request, template_name, {'survey': survey_raw, 'form': form})

@staff_member_required
def map_sweden(request, template_name='matching/sweden_regions.html'):
    '''
    edit questions text for student for choosen sliders and gradings
    '''
    fair = Fair.objects.get(current=True)
    survey_raw = Survey.objects.get(pk=request.session.get('survey_raw_id'))
    survey_proc = Survey.objects.get(pk=request.session.get('survey_proc_id'))
    try:
        question = Question.objects.get(survey=survey_raw, name='sweden-city')
    except:
        question = None
        form=None

    if question:
        exhibitors = Exhibitor.objects.filter(fair=fair)
        responses = Response.objects.filter(survey=survey_raw, question=question)
        answers_raw_all = TextAns.objects.filter(response__in=responses)
        regions = SwedenRegion.objects.filter(survey=survey_proc)
        prefix = 'response_'
        form = MapSwedenForm(
            request.POST or None,
            responses=responses,
            regions=regions,
            prefix=prefix
        )
        if form.is_valid():
            for key, values in form.cleaned_data.items():
                for ex in exhibitors:
                    if key.split(':')[0] == str(ex.pk):
                        #remove exhibitor from regions if in values
                        regions_to_exclude = [r for r in regions if r not in values]
                        for reg in regions_to_exclude:
                            try:
                                reg.exhibitors.remove(ex)
                            except:
                                pass
                        #add exhibitor to regions if in values
                        for val in values:
                            try:
                                val.exhibitors.add(ex)
                            except:
                                pass

    return render(request, template_name, {'form': form, 'survey': survey_raw, 'question': question})

@staff_member_required
def map_world(request, template_name='matching/world_regions.html'):
    '''
    map world to world representation in apps/web
    '''
    fair = Fair.objects.get(current=True)
    survey_raw = Survey.objects.get(pk=request.session.get('survey_raw_id'))
    survey_proc = Survey.objects.get(pk=request.session.get('survey_proc_id'))
    try:
        question = Question.objects.get(survey=survey_raw, name='world-country')
    except Question.DoesNotExist:
        question = None
        form = None

    countries = []
    incorrect_countries = []
    if question:
        # get all responses and pass them to the subregiongenerator
        responses = Response.objects.filter(survey=survey_raw, question=question)
        (correct_words, incorrect_words) = pea.genSubRegions(responses, survey_raw, survey_proc)
        # get exhibitor data to map each region to exhibitors
        answers_raw = TextAns.objects.filter(response__in=responses)
        exhibitor_values = [r.exhibitor.pk for r in responses]
        response_keys = [r.pk for r in responses]
        ex_resp_dict = dict(zip(response_keys, exhibitor_values))

        for w in correct_words:
            (country, isCreated) = Country.objects.get_or_create(name=w)
            if isCreated:
                for answer in answers_raw:
                    if country.name in answer.ans:
                        exhibitor = Exhibitor.objects.get(pk=ex_resp_dict[answer.response.pk])
                        country.exhibitor.add(exhibitor)
                        country.save()
            countries.append(country)

        for w in incorrect_words:
            (incorrect_word, isCreated) = Country.objects.get_or_create(name=w)
            if isCreated:
                for answer in answers_raw:
                    if incorrect_word.name in answer.ans:
                        exhibitor = Exhibitor.objects.get(pk=ex_resp_dict[answer.response.pk])
                        country.exhibitor.add(exhibitor)
            incorrect_countries.append(incorrect_word)

        region_prefix = 'country_'
        continents = Continent.objects.filter(survey=survey_proc)
        form = MapSubAreaForm(
            request.POST or None,
            survey_raw = survey_raw,
            survey_proc = survey_proc,
            sub_regions = countries,
            sub_regions_wrong = incorrect_countries,
            regions = continents,
            region_prefix = region_prefix
        )
        if form.is_valid():
            for sub_reg in countries + incorrect_countries:
                region_id = form.cleaned_data['%s%i'%(region_prefix, sub_reg.pk)]
                if region_id and region_id != 'None':
                    try:
                        sub_reg.continent = Continent.objects.get(pk=int(region_id))
                        sub_reg.save()
                    except ValueError:
                        pass #this should never happen! if you suspect something fishy contact Emma Backstrom
                else:
                    if sub_reg.continent:
                        sub_reg.continent = None
                        sub_reg.save()




    return render(request, template_name, {'form': form, 'survey': survey_raw, 'question': question})

@staff_member_required
def init_workfields(request, template_name='matching/init_workfields.html'):
    '''
    initialize processing and clustering on the workfields
    '''
    fair = Fair.objects.get(current=True)
    survey_raw = Survey.objects.get(pk=request.session.get('survey_raw_id'))
    survey_proc = Survey.objects.get(pk=request.session.get('survey_proc_id'))
    try:
        question = Question.objects.get(survey=survey_raw, name='workfields')
    except Question.DoesNotExist:
        question = None
        form = None

    if question:
        responses = Response.objects.filter(survey=survey_raw,question=question)

        ''' this does not work properly on the server, fix later
        workfields = WorkField.objects.filter(survey=survey_proc)
        if not workfields:
            (most_common_correct, most_common_incorrect) = pea.genWorkFields(responses, survey_raw, survey_proc, True)

            for key, value in most_common_correct:
                (wfield, isCreated) = WorkField.objects.get_or_create(work_field=key)
                try:
                    wfield.survey.add(survey_proc)
                    wfield.save()
                except:
                    pass
            for key, value in most_common_incorrect:
                (wfield, isCreated) = WorkField.objects.get_or_create(work_field=key)
                try:
                    wfield.survey.add(survey_proc)
                    wfield.save()
                except:
                    pass
        '''

        exhibitors = Exhibitor.objects.filter(fair=fair)
        answers_raw_all = TextAns.objects.filter(response__in=responses)
        workfields = WorkField.objects.filter(survey=survey_proc)
        form = WorkFieldForm(
            request.POST or None,
            responses=responses,
            workfields=workfields,
        )
        if form.is_valid():
            for key, workfields_selected in form.cleaned_data.items():
                for ex in exhibitors:
                    if key.split(':')[0] == str(ex.pk):
                        #remove exhibitor from regions if in values
                        wfields_to_exclude = [w for w in workfields if w not in workfields_selected]
                        for wfield in wfields_to_exclude:
                            try:
                                wfield.exhibitors.remove(ex)
                            except:
                                pass
                        #add exhibitor to regions if in values
                        for wfield in workfields_selected:
                            try:
                                wfield.exhibitors.add(ex)
                            except:
                                pass


    return render(request, template_name, {'survey': survey_raw, 'form': form, 'question': question})

@staff_member_required
def finalize_workfields(request, template_name='matching/finalize_workfields.html'):
    '''
    finalize the workfields by mapping them to work areas as a group
    '''
    print(request)
    fair = Fair.objects.get(current=True)
    survey_raw = Survey.objects.get(pk=request.session.get('survey_raw_id'))
    survey_proc = Survey.objects.get(pk=request.session.get('survey_proc_id'))


    return render(request, template_name, {'survey': survey_raw})

@staff_member_required
def init_classifier(request, template_name='matching/init_classifier.html'):
    '''
    Initialize the classifier with a buttom and print the stats of it TODO
    '''
    fair = Fair.objects.get(current=True)
    survey_raw = Survey.objects.get(pk=request.session.get('survey_raw_id'))
    survey_proc = Survey.objects.get(pk=request.session.get('survey_proc_id'))

    created_text = 'You already have a classifier set as current!'

    created = classify.init_classifier(survey_proc.pk)
    if created:
        created_text = 'KNN Classifier successfully created!'

    return render(request, template_name, {'survey': survey_raw, 'created_text': created_text})

@staff_member_required
def overwatch(request, template_name='matching/overwatch.html'):
    '''
    A simple view to return the matching algorithm status for students
    '''
    survey_raw = Survey.objects.get(pk=request.session.get('survey_raw_id'))
    survey_proc = Survey.objects.get(pk=request.session.get('survey_proc_id'))

    students = StudentProfile.objects.all()
    results = MatchingResult.objects.filter(student__in=students)

    return render(request, template_name, {'survey': survey_raw, 'students': students, 'results': results})
