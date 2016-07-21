from django.http import JsonResponse
from companies.models import Company
from events.models import Event
from news.models import NewsArticle

from .serializers import company_serializer, event_serializer, newsarticle_serializer

def root(request):
    return JsonResponse({'message':'Welcome to the Armada API!'})

def exhibitors(request):
    companies = Company.objects.all()
    data = [company_serializer(company) for company in companies]
    return JsonResponse(data, safe=False)

def events(request):
    events = Event.objects.filter(make_event_public=True)
    data = [event_serializer(event) for event in events]
    return JsonResponse(data, safe=False)

def news(request):
    news = NewsArticle.public_articles.all()
    data = [newsarticle_serializer(article) for article in news]
    return JsonResponse(data, safe=False)
