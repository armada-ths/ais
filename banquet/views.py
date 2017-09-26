from django.forms import modelform_factory
from django.shortcuts import render, redirect, get_object_or_404
from banquet.models import BanquetteAttendant
from django.urls import reverse
from fair.models import Fair

def banquet_attendants(request, year, template_name='banquet/banquet_attendants.html'):
    fair = get_object_or_404(Fair, year=year)
    if request.user.is_authenticated():
        banquet_attendants = BanquetteAttendant.objects.filter(fair=fair)
        return render(request, template_name, {
            'banquet_attendants': banquet_attendants,
            'fair': fair
        })

    return render(request, 'login.html', {'next': next, 'fair': fair})
