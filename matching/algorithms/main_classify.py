from django.contrib.auth.models import User
from fair.models import Fair
from exhibitors.models import Exhibitor
from matching.models import *

from student_profiles.models import StudentProfile, MatchingResult

from random import randint
import math
import json

def genResult(student, exhibitor, score, fair):
    '''
    '''
    result = MatchingResult.objects.create(student=student,
        exhibitor=exhibitor,
        fair=fair,
        score=score)

def randomize_answers(student, survey, numberOfResults):
    '''
    Until algorithm is working corretly we write answers to MatchingResult for
    the apps to get some data
    '''
    fair = Fair.objects.get(current=True)
    exhibitors = list(Exhibitor.objects.filter(fair=fair))
    ex_len = len(exhibitors)
    for i in range(numberOfResults):
        if i == 0:
            score = 100
        else:
            score = randint(0,100)
        genResult(student, exhibitors[randint(0,ex_len-1)], score, fair)


def classify(student_id, survey_id, numberOfResults=10):
    '''
    Main classifer to be called from the api when the final put request is called
    from the apps

    required input is
    student_id (pk)         - a primary key to a StudentProfile object
    survey (pk)             - a primary key to the survey used
    numberOfResults (int)   - integer specifying how many results should be
                              generated for the student_id
    '''
    finished_flag = False
    # survey_raw = TODO add relates_to = models.ForeignKey('self') in Survey if nec
    try:
        student = StudentProfile.objects.get(pk=student_id)
        survey = Survey.objects.get(pk=survey_id)
        randomize_answers(student, survey, numberOfResults)
        finished_flag = True
    except (StudentProfile.DoesNotExist, Survey.DoesNotExist):
        pass
    return finished_flag

def init_classifier(survey_id, classifer_type = 'euclidian'):
    '''
    initialization of classifer using KNN only for now and euclidian dist as standard
    '''
    survey = Survey.objects.get(pk=survey_id)
    try:
        classifier = KNNClassifier.objects.get(survey=survey, current=True)

    except KNNClassifier.DoesNotExist:
        workfields = WorkField.objects.filter(survey=survey)
        exhibitors_all = [w.exhibitors.all() for w in workfields]
        exhibitors = set(exhibitors_all)
