from django.forms import modelform_factory
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .models import BanquetteAttendant
from .forms import BanquetteAttendantForm, ExternalBanquetSignupForm
from django.urls import reverse
from fair.models import Fair
from register.views import external_signup
from django.contrib.auth.models import User

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

    #banquet_attendants = BanquetteAttendant.objects.filter(fair=fair)
    #users_all = User.objects.all()
    #forbidden_users = []
    #for b in banquet_attendants:
    #    if b.user:
    #        forbidden_users.append(b.user)
    #
    #try:
    #    currentUser = banquet_attendant.user
    #    users = [currentUser.pk] + [u.pk for u in users_all if u not in forbidden_users]
    #except User.DoesNotExist:
    #    users = [u.pk for u in users_all if u not in forbidden_users]
    #    currentUser = None
    #
    if request.user.is_authenticated():
        form = BanquetteAttendantForm(
            request.POST or None,
            instance=banquet_attendant,
            #users=users,
            #user=currentUser
        )
        if form.is_valid():
            banquet_attendant = form.save(commit=False)
            banquet_attendant.fair = fair
            #banquet_attendant.user = form.cleaned_data['users_choice']
            banquet_attendant.save()
            return render(request, template_name, {'form': form, 'fair': fair })
        return render(request, template_name, {'form': form, 'fair': fair })

    # not authenticated:
    return render(request, 'login.html', {'next': next, 'fair': fair})

def new_banquet_attendant(request, year, template_name='banquet/banquet_attendant.html'):
    fair = get_object_or_404(Fair, year=year)

    #banquet_attendants = BanquetteAttendant.objects.filter(fair=fair)
    #users_all = User.objects.all()
    #forbidden_users = []
    #for b in banquet_attendants:
    #    if b.user:
    #        forbidden_users.append(b.user)
    #users = [u.pk for u in users_all if u not in forbidden_users]
    #
    if request.user.is_authenticated():
        form = BanquetteAttendantForm(
            request.POST or None,
            instance=None,
            #users=users,
            #user = None
        )
        if form.is_valid():
            banquet_attendant = form.save(commit=False)
            banquet_attendant.fair = fair
            #banquet_attendant.user = User.objects.get(pk=form.cleaned_data['users_choice'])
            banquet_attendant.save()
            return HttpResponseRedirect(reverse('banquet_attendants', kwargs={'year': fair.year }))
        return render(request, template_name, {'form': form, 'fair': fair })

    # not authenticated:
    return render(request, 'login.html', {'next': next, 'fair': fair})

def banquet_external_signup(request, year, template_name='banquet/external_signup.html'):
    fair = get_object_or_404(Fair, year=year)

    if request.user.is_authenticated():
        try:
            banquet_instance = BanquetteAttendant.objects.get(user=request.user, fair=fair)
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
    return redirect('/register/external/signup')

def thank_you(request, year, template_name='banquet/thank_you.html'):
    fair = get_object_or_404(Fair, year=year)
    return render(request, 'banquet/thank_you.html', {'fair': fair })
