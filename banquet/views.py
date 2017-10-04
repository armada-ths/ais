from django.forms import modelform_factory
from django.shortcuts import render, redirect, get_object_or_404
from .models import BanquetteAttendant
from .forms import BanquetteAttendantForm, ExternalBanquetSignupForm
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

def banquet_attendant(request, year, pk, template_name='banquet/banquet_attendant.html'):
    fair = get_object_or_404(Fair, year=year)
    banquet_attendant = get_object_or_404(BanquetteAttendant, fair=fair, pk=pk)

    if request.user.is_authenticated():
        form = BanquetteAttendantForm(
            request.POST or None,
            instance=banquet_attendant,
        )
        if form.is_valid():
            banquet_attendant = form.save(commit=False)
            banquet_attendant.fair = fair
            banquet_attendant.save()
            return render(request, template_name, {'form': form, 'fair': fair })
        return render(request, template_name, {'form': form, 'fair': fair })

    # not authenticated:
    return render(request, 'login.html', {'next': next, 'fair': fair})

def new_banquet_attendant(request, year, template_name='banquet/banquet_attendant.html'):
    fair = get_object_or_404(Fair, year=year)

    if request.user.is_authenticated():
        form = BanquetteAttendantForm(
            request.POST or None,
            instance=None,
        )
        if form.is_valid():
            banquet_attendant = form.save(commit=False)
            banquet_attendant.fair = fair
            banquet_attendant.save()
            return render(request, template_name, {'form': form, 'fair': fair })
        return render(request, template_name, {'form': form, 'fair': fair })

    # not authenticated:
    return render(request, 'login.html', {'next': next, 'fair': fair})

def banquet_external_signup(request, year, template_name='banquet/external_signup.html'):
    fair = get_object_or_404(Fair, year=year)
    
    if request.user.is_authenticated():
        try:
            banquet_instance = BanquetteAttendant.objects.get(user=request.user)
        except BanquetteAttendant.DoesNotExist:
            banquet_instance = None

        form = ExternalBanquetSignupForm(
            request.POST or None,
            instance = banquet_instance,
        )
        if form.is_valid():
            banquet_attendant = form.save(commit=False)
            banquet_attendant.fair = fair
            banquet_attendant.user = request.user
            banquet_attendant.save()
            return render(request, 'banquet/thank_you.html', {'fair': fair })
        return render(request, template_name, {'form': form, 'fair': fair })
    # not authenticated
    return render(request, 'login.html', {'next': next, 'fair': fair})

def thank_you(request, year, template_name='banquet/thank_you.html'):
    fair = get_object_or_404(Fair, year=year)
    return render(request, 'banquet/thank_you.html', {'fair': fair })
