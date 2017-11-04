from django.forms import ModelForm, Form, Select, RadioSelect, ChoiceField, ModelMultipleChoiceField, CheckboxSelectMultiple, CharField
from django.utils.html import mark_safe, format_html
from django.db.models import Min, Max

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
        grading_questions = kwargs.pop('grading_questions')
        slider_prefix = kwargs.pop('slider_prefix')
        grading_prefix = kwargs.pop('grading_prefix')
        super(StudentQuestionForm, self).__init__(*args, **kwargs)

        self.init_question_fields(slider_questions, slider_prefix)
        self.init_question_fields(grading_questions, grading_prefix)

    def init_question_fields(self, questions, prefix):
        '''
        Initialize all grading fields does not need any grading length since this
        is set earlier in the index view, here we only want to change the text
        '''
        for q in questions:
            self.fields['%s%i'%(prefix, q.pk)] = self.QuestionCharField(object = q, initial=q.question)

    class QuestionCharField(CharField):
        def __init__(self, object, *args, **kwargs):
            CharField.__init__(self, *args, **kwargs)
            ex_q = Question.objects.get(pk=object.company_question.pk)
            self.label='Exhibitor Question: %s Current Text: %s'%(ex_q.text, object.question)

    def clean(self):
        super(StudentQuestionForm, self).clean()

class MapSubAreaForm(Form):
    '''
    Used to map cities and countries to the regions predefined in the app and
    on the ais db, for now this is also called by the workfield for the teams
    to get some nice data to use
    '''
    def __init__(self, *args, **kwargs):
        survey_raw = kwargs.pop('survey_raw')
        survey_proc = kwargs.pop('survey_proc')
        sub_regions = kwargs.pop('sub_regions')
        sub_regions_wrong = kwargs.pop('sub_regions_wrong')
        regions = kwargs.pop('regions')
        region_prefix = kwargs.pop('region_prefix')
        super(MapSubAreaForm, self).__init__(*args, **kwargs)
        self.init_area_fields(sub_regions, regions, region_prefix)
        self.init_area_fields(sub_regions_wrong, regions, region_prefix, True)

    def init_area_fields(self, sub_regions, regions, prefix, wFlag=False):
        '''
        init the field with a select choice of
        wFlag indicates if the label should be flagged by an error text
        '''
        region_select = [(None, 'This data is wrong!')]
        for region in regions:
            tup = (region.pk, region.name)
            region_select.append(tup)

        for sub_region in sub_regions:
            self.fields['%s%i'%(prefix, sub_region.pk)] = self.AreaSelectField(choices=region_select, object = sub_region, required=False, wFlag=wFlag)


    class AreaSelectField(ChoiceField):
        def __init__(self, object, wFlag, *args, **kwargs):
            ChoiceField.__init__(self, *args, **kwargs)
            if wFlag == False:
                self.label='%s'%object.name
            else:
                self.label='DataError (could not process): %s'%object.name
