from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required

from fair.models import Fair

@permission_required('events.base')
def list(request, year):
	fair = get_object_or_404(Fair, year=year)
	
	return render(request, 'events/list.html', {
		'fair': fair
	})
