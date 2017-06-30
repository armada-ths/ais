from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.core import urlresolvers
from django.contrib import messages

from .models import Question, Survey
from .forms import ResponseForm

from exhibitors.models import Exhibitor
from companies.models import Company, Contact
from fair.models import Fair


def index(request, template_name = 'matching/exhibitor_questions.html'):
    currentFair = Fair.objects.get(current=True)
    if request.user.is_authenticated():
        contact = Contact.objects.get(user=request.user)
        # make sure user is connected to a 'Contact'
        if contact is None:
            return redirect('anmalan:logout')
        else:
            # make sure a 'Company' is connected to contact
            company = contact.belongs_to
            if company is None:
                return redirect('anmalan:logout')

            exhibitor = None
            try:
                exhibitor = Exhibitor.objects.get(company=company)
            except Exhibitor.DoesNotExist:
                pass

    survey = Survey.objects.get(fair = currentFair, name='exhibitor-matching')
    survey_questions = Question.objects.filter(survey = survey)
    form = ResponseForm(request.POST or None,
            survey=survey,
            questions =survey_questions,
            exhibitor=exhibitor)
    if form.is_valid():
        response = form.save()

    return render(request, template_name, {'response_form': form, 'survey': survey, 'exhibitor': exhibitor})
    return render(request)
