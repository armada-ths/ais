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

from .helpers_view import update_processed_question, delete_processed_question

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
        selected_ex_grading = form.cleaned_data['questions_select_grading']
        # update or delete selected questions
        update_processed_question(selected_ex_slider, survey_proc)
        delete_processed_question(selected_ex_slider, survey_proc,'slider')
        update_processed_question(selected_ex_grading, survey_proc)
        delete_processed_question(selected_ex_grading, survey_proc, 'grading')

    return render(request, template_name, {'form': form})
