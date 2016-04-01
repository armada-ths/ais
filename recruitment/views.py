from django.shortcuts import render

# Create your views here.
#list all companies
def recruitment(request, template_name='recruitment/recruitment.html'):
    data = {}
    return render(request, template_name, data)
