from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from locations.models import Location
from locations.forms import LocationForm

def location_list(request, template_name='locations/location_list.html'):
    locations = Location.objects.all()
    data = {}
    data['object_list'] = locations
    return render(request, template_name, data)

def location_create(request, template_name='locations/location_form.html'):
    form = LocationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('location_form')
    return render(request, template_name, {'form':form})

def location_update(request, pk, template_name='locations/location_form.html'):
    location = get_object_or_404(Location, pk=pk)
    form = LocationForm(request.POST or None, instance=location)
    if form.is_valid():
        form.save()
        return redirect('location_list')
    return render(request, template_name, {'form':form})

def location_delete(request, pk, template_name='locations/location_confirm_delete.html'):
    location = get_object_or_404(Location, pk=pk)
    if request.method=='POST':
        location.delete()
        return redirect('location_list')
    return render(request, template_name, {'object':location})