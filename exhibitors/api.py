from collections import OrderedDict

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page

from exhibitors.models import Exhibitor, Location, Booth, ExhibitorInBooth
from fair.models import Fair, FairDay


def serialize_exhibitor(exhibitor, request):
	img_placeholder = request.GET.get('img_placeholder') == 'true'
	
	return OrderedDict([
		('id', exhibitor.pk),
		('name', exhibitor.company.name),
		('type', exhibitor.company.type.type),
		('company_website', exhibitor.company.website),
		('about', exhibitor.catalogue_about),
		('purpose', exhibitor.catalogue_purpose),
		('logo_squared', (exhibitor.catalogue_logo_squared.url) if exhibitor.catalogue_logo_squared else (MISSING_IMAGE if img_placeholder else None)),
		('logo_freesize', (exhibitor.catalogue_logo_freesize.url) if exhibitor.catalogue_logo_freesize else (MISSING_IMAGE if img_placeholder else None)),
		('contact_name', exhibitor.catalogue_contact_name),
		('contact_email_address', exhibitor.catalogue_contact_email_address),
		('contact_phone_number', exhibitor.catalogue_contact_phone_number),
		('industries', [{'id': industry.pk, 'name': industry.industry} for industry in exhibitor.catalogue_industries.all()]),
		('values', [{'id': value.pk, 'name': value.value} for value in exhibitor.catalogue_values.all()]),
		('employments', [{'id': employment.pk, 'name': employment.employment} for employment in exhibitor.catalogue_employments.all()]),
		('locations', [{'id': location.pk, 'name': location.location} for location in exhibitor.catalogue_locations.all()]),
		('benefits', [{'id': benefit.pk, 'name': benefit.benefit} for benefit in exhibitor.catalogue_benefits.all()]),
		('average_age', exhibitor.catalogue_average_age),
		('founded', exhibitor.catalogue_founded),
		('groups', [{'id': group.pk, 'name': group.name} for group in exhibitor.company.groups.filter(fair = exhibitor.fair, allow_exhibitors = True)]),
		('fair_locations', [])
	])


@cache_page(60 * 5)
def exhibitors(request):
	data = []
	
	for exhibitor in Exhibitor.objects.filter(fair = Fair.objects.get(current = True)):
		data.append(serialize_exhibitor(exhibitor, request))
	
	return JsonResponse(data, safe = False)


def locations(request):
	data = []
	
	for location in Location.objects.filter(fair__current = True):
		data.append({
			'id': location.pk,
			'parent': {
				'id': location.parent.pk,
				'name': location.parent.name
			} if location.parent else None,
			'name': location.name,
			'has_map': bool(location.background)
		})
	
	return JsonResponse(data, safe = False)


def location(request, location_pk):
	location = get_object_or_404(Location, fair__current = True, pk = location_pk)
	
	booths = []
	
	for booth in Booth.objects.filter(location = location):
		booths.append({
			'name': booth.name,
			'boundaries': booth.boundaries.coords,
			'centroid': booth.boundaries.centroid.coords,
			'exhibitors': [{
				'id': exhibitor_in_booth.exhibitor.pk,
				'name': exhibitor_in_booth.exhibitor.company.name,
				'comment': exhibitor_in_booth.comment,
				'days': [{
					'id': day.pk,
					'name': day.name
				} for day in exhibitor_in_booth.days.all()],
			} for exhibitor_in_booth in ExhibitorInBooth.objects.filter(booth = booth)]
		})
	
	data = {
		'id': location.pk,
		'parent': {
				'id': location.parent.pk,
				'name': location.parent.name
			} if location.parent else None,
		'name': location.name,
		'map': {
			'url': location.background.url,
			'width': location.background.width,
			'height': location.background.height
		} if location.background else None,
		'booths': booths
	}
	
	return JsonResponse(data, safe = False)


def days(request):
	data = []
	
	for day in FairDay.objects.filter(fair__current = True):
		data.append({
			'id': day.pk,
			'name': day.name
		})
	
	return JsonResponse(data, safe = False)
