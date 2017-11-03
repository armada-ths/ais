
###########################################################
#   Helper foos for views.py in matching app
#
###########################################################
from .models import *


def update_processed_question(exhibitor_q, survey):
    '''
    Belongs to index foo in views.py

    For now only add questions, no delete yet

    Necessary fields:
    * exhibitor_q (list)    list of exhibitor question objects
    * survey (Survey object)
    '''
    for ex_q in exhibitor_q:
        st_q = None
        try:
            if ex_q.question_type == Question.INT:
                st_q = StudentQuestionSlider.objects.get(survey=survey, company_question=ex_q)
            elif ex_q.question_type == Question.SELECT:
                st_q = StudentQuestionGrading.objects.get(survey=survey, company_question=ex_q)
        except:
            if ex_q.question_type == Question.INT:
                st_q = StudentQuestionSlider.objects.create(company_question=ex_q,
                    question='TODO from question: %s'%ex_q.text,
                    min_value=0.0,
                    max_value=1337.0,
                    )
            elif ex_q.question_type == Question.SELECT:
                st_q = StudentQuestionGrading.objects.create(company_question=ex_q,
                question='TODO from question: %s'%ex_q.text)

            st_q.survey.add(survey)
            st_q.save()
            ex_q.survey.add(survey)
            ex_q.save()

def delete_processed_question(exhibitor_q, survey, qType):
    '''
    Belongs to index foo in views.py

    Delete Student questions and remove manytomany relation to processed
    survey for the exhibitor questions.
    '''
    exq_ids = [q.id for q in exhibitor_q]
    if qType == 'slider':
        stud_q_to_delete = StudentQuestionSlider.objects.filter(survey=survey, question_type=qType).exclude(company_question__in=exq_ids)
    elif qType == 'grading':
        stud_q_to_delete = StudentQuestionGrading.objects.filter(survey=survey, question_type=qType).exclude(company_question__in=exq_ids)

    exq_ids_to_remove = [q.company_question.pk for q in stud_q_to_delete]
    exq_to_remove = Question.objects.filter(id__in=exq_ids_to_remove)
    for exq in exq_to_remove:
        exq.survey.remove(survey)
    for sq in stud_q_to_delete:
        sq.delete()
