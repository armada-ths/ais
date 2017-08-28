# Run the script of adam first (or make sure there is a fair with current set as True), then from the root of the repo run:
# python manage.py shell < ./scripts/generate-exhibitor-matching.py --settings local_settings
# Note: python version should be 3.x.x

import sys
from django.contrib.auth.models import User
from exhibitors import models
from matching.models import Question, Survey, Response, Answer, TextAns, ChoiceAns, IntegerAns, BooleanAns
from fair.models import Fair

#PUT QUESTIONS AND QUESTIONS TYPES HERE IN THE SEPARATE LISTS, deleta any questions priod to running this script from <url>admin//matching/questions, if questions are added later make sure you dont add the same question agan!
qTexts = ['How many employees do you have?',
        'How many offices does your organization have in Sweden?',
        'Please list towns in Sweden where you have offices relevant to KTH students',
        'How many countries other than Sweden do you have offices in?',
        'Please list the countries where you have international offices',
        'Percentage of your organizations workforce come from an engineering or scientific background?',
        'Average number of team building/social events per year?', ###
        'Average hours spent on employee education per year?',
        'If there exists, please list what type of education',
        'If there exists, please list any certain interest groups the employee can be part of in your organization, i.e, sport teams, bookcircles, etc.',
        'Number of summerjobs available?',
        'Number of trainee positions available?',
        'Number of part time jobs during studies available?',
        'Number of masters thesis projects available?',
        'Does the employees typically work in project groups?',
        'What is the average number of months for a project?',
        'Does your organization have employees spending working hours on own innovation projects?',
        'Does your organization have employees spending working hours on volontary work to help society?',
        'Does your employees work in an open office environment?',
        'Does your employees travel for business to other Swedish cities frequently?',
        'Does your employees travel for business to other countries frequently?',
        'What is the average length of an employment (in jobs related to KTH students) in months?',
        'Please list the fields your company work in',
        'How many patents does your company own?',
        'If any, within which fields do you own patents?'
        ]
qTypes = [Question.INT,
        Question.INT,
        Question.TEXT,
        Question.INT,
        Question.TEXT,
        Question.INT,
        Question.INT,
        Question.INT,
        Question.TEXT,
        Question.TEXT,
        Question.INT,
        Question.INT,
        Question.INT,
        Question.INT,
        Question.SELECT,
        Question.INT,
        Question.SELECT,
        Question.SELECT,
        Question.SELECT,
        Question.SELECT,
        Question.SELECT,
        Question.INT,
        Question.TEXT,
        Question.INT,
        Question.TEXT
        ]
comma_help = '(please use comma as a delimiter)'

if len(qTexts) != len(qTypes):
    print('Wrong input of questins')
    sys.exit()

#u = User.objects.get()
try:
    current_fair = Fair.objects.get(current=True)
except Fair.DoesNotExist:
    sys.exit()

survey_name = 'exhibitor-matching'
try:
    survey_matching = Survey.objects.get(fair=current_fair, name=survey_name)
except Survey.DoesNotExist:
    survey_matching = Survey.objects.create(fair=current_fair, name=survey_name, description='Survey for exhibitor matching')


for i, input in enumerate(qTexts):
    try:
        Question.objects.get(text=qTexts[i])
    except Question.DoesNotExist:
        q = Question.objects.create(question_type=qTypes[i],text=qTexts[i], name=qTexts[i][0:int(len(qTexts[i])/3)])
        if q.question_type == Question.TEXT:
            q.help_text = comma_help
        #q.save() #need to have an pk before manytomany relation with survey is est
        q.survey.add(survey_matching)
        q.save()
