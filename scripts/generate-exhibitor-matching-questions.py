# Run the script of adam first, then Run:
# python manage.py shell < generate-exhibitor-matching.py

from django.contrib.auth.models import User
from exhibitors import models
from matching.models import Question, Survey, Response, Answer, TextAns, ChoiceAns, IntegerAns, BooleanAns
from fair.models import Fair


u = User.objects.get()

current_fair = Fair.objects.get(current=True)

survey_matching = Survey(fair=current_fair, name='exhibitor-matching', description='Survey for exhibitor matching')
survey_matching.save()

q1 = Question(question_type=Question.INT, text='Average number of team building/social events per year?')
q1.save()
#cont to add questions in the same manner...

# all questions need to have an id before its ManyToMany relation is established
q1.survey.add(survey_matching)
q1.save()
