from django.shortcuts import render
from .forms import ChoiceAnsForm, TextAnsForm, BooleanAns
from .models import Question


def index(request, template_name = 'matching/exhibitor_questions.html'):
    questions = Question.objects.all()
    if request.method == 'POST':
        print(request.POST)
        for q in questions:
            try:
                data = {u'%s-answer'%q.id: request.POST[u'%s-answer'%q.id]}
            except:
                data = {u'%s-answer'%q.id: None}
            q.form = q.answer_type.model_class().form(prefix='%s'%q.id, data = data)
    else:
        for q in questions:
            q.form = q.ans_type.model_class().form(prefix='%s'%q.id)
    return render(request, template_name, {'questions': questions,})
