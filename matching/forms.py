from django.forms import ModelForm, Form, Select, RadioSelect, ChoiceField, ModelMultipleChoiceField, CheckboxSelectMultiple, CharField
from django.utils.html import mark_safe, format_html
from fair.models import Fair
from .models import *
from exhibitors.models import Exhibitor
from companies.models import Company

import datetime

class RawQuestionForm(Form):
    '''
    Used in the index view to pick which questions to use from the raw input
    matching-survey filled in by the companies
    '''

    def __init__(self, *args, **kwargs):
        exhibitor_slider = kwargs.pop('exhibitor_slider')
        exhibitor_grading = kwargs.pop('exhibitor_grading')
        current_student_slider = kwargs.pop('current_student_slider')
        current_student_grading = kwargs.pop('current_student_grading')
        super(RawQuestionForm, self).__init__(*args, **kwargs)

        if exhibitor_slider:
            self.questions_as_select_field(exhibitor_slider, current_student_slider, 'questions_select_slider')
        if exhibitor_grading:
            self.questions_as_select_field(exhibitor_grading, current_student_grading, 'questions_select_grading')


    class QuestionMultiChoiceField(ModelMultipleChoiceField):
        def label_from_instance(self, object):
            responses = Response.objects.filter(question=object)
            return format_html("<span class='btn btn-armada-checkbox product-description'>{} #Responses: {}</span>",
            mark_safe(object.text),
            mark_safe(len(responses)),
            )

    def questions_as_select_field(self, exhibitor_questions, current_student_q, fieldname):
        '''
        Generates a choice field of the questions
        '''
        initQuestions = []
        for q in current_student_q:
            initQuestions.append(q.company_question)

        self.fields[fieldname] = self.QuestionMultiChoiceField(queryset=exhibitor_questions,
            required=False, widget=CheckboxSelectMultiple())
        self.fields[fieldname].initial = initQuestions



    def clean(self):
        super(RawQuestionForm, self).clean()

class StudentQuestionForm(Form):
    '''
    Used for settings the slider and grading questions for students
    '''

    def __init__(self, *args, **kwargs):
        survey_raw = kwargs.pop('survey_raw')
        survey_proc = kwargs.pop('survey_proc')
        slider_questions = kwargs.pop('slider_questions')
        slider_ex_responses = kwargs.pop('slider_ex_responses')
        grading_questions = kwargs.pop('grading_questions')
        grading_ex_responses = kwargs.pop('grading_ex_responses')
        slider_prefix = kwargs.pop('slider_prefix')
        grading_prefix = kwargs.pop('grading_prefix')
        super(StudentQuestionForm, self).__init__(*args, **kwargs)

        self.init_slider_fields(slider_questions, slider_ex_responses, slider_prefix, survey_raw)
        self.init_grading_fields(grading_questions, grading_prefix)

    def init_slider_fields(self, slider_questions, slider_ex_responses, slider_prefix):
        '''
        Initialize all fields and propose a min/max value for slider
        '''
        pass

    def init_grading_fields(self, grading_questions, prefix):
        '''
        Initialize all grading fields does not need any grading length since this
        is set earlier in the index view, here we only want to change the text
        '''
        for gq in grading_questions:
            self.fields['%s%i'%(prefix, gq.pk)] = CharField(initial=gq.question)
