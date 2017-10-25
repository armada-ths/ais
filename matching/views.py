from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required

from .models import *
from companies.models import Company
from exhibitors.models import Exhibitor
from fair.models import Fair

from .forms import RawQuestionForm

from collections import Counter

@staff_member_required
def index(request, template_name='matching/index.html'):
    '''
    A lightweight index view displaying the company questions.
    User may pick which questions to use to generate the matching questions
    for students.

    Returns 404 if current fair does not exist or exhibitor-matching survey does
    not exist.
    '''
    fair = get_object_or_404(Fair, current=True)
    exhibitors = Exhibitor.objects.filter(fair=fair)

    name_survey_raw = 'exhibitor-matching'
    survey_raw = get_object_or_404(Survey, fair=fair, name=name_survey_raw)
    try:
        survey_proc = Survey.objects.get(fair=fair, name='%s-processed'%name_survey_raw)
    except:
        survey_proc = Survey.objects.create(fair=fair,
            name='%s-processed'%name_survey_raw,
            description='processed data for %s'%name_survey_raw
        )
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
        update_processed_question(selected_ex_slider, survey_proc)
        selected_ex_grading = form.cleaned_data['questions_select_grading']
        update_processed_question(selected_ex_grading, survey_proc)

    return render(request, template_name, {'form': form})

def update_processed_question(exhibitor_q, survey):
    '''
    For now only add questions, no delete yet
    '''
    for ex_q in exhibitor_q:
        st_q = None
        try:
            if ex_q.question_type==Question.INT:
                st_q = StudentQuestionSlider.objects.get(survey=survey, company_question=ex_q)
            elif ex_q.question_type==Question.SELECT:
                st_q = StudentQuestionGrading.objects.get(survey=survey, company_question=ex_q)
        except:
            if ex_q.question_type==Question.INT:
                st_q = StudentQuestionSlider.objects.create(company_question=ex_q,
                    question='TODO from question: %s'%ex_q.text,
                    min_value=0.0,
                    max_value=1337.0,
                    )
                st_q.survey.add(survey)
                st_q.save()
                ex_q.survey.add(survey)
                ex_q.save()
