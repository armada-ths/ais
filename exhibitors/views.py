from django.forms import modelform_factory
from django.http import HttpResponseForbidden
from recruitment.models import RecruitmentApplication
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import TextInput
from exhibitors.models import Exhibitor
from companies.models import Company
from django.urls import reverse
from fair.models import Fair

def user_can_modify_exhibitor(user, exhibitor):
    return user.has_perm(
        'exhibitors.change_exhibitor') or user in exhibitor.hosts.all() or user in exhibitor.superiors()


def exhibitors(request, year, template_name='exhibitors/exhibitors.html'):
    if not request.user.has_perm('exhibitors.view_exhibitors'):
        return HttpResponseForbidden()

    fair = get_object_or_404(Fair, year=year)
    return render(request, template_name, {
        'exhibitors': Exhibitor.objects.prefetch_related('hosts').filter(fair=fair).order_by('company__name'),
        'fair': fair
    })


def exhibitor(request, year, pk, template_name='exhibitors/exhibitor.html'):
    exhibitor = get_object_or_404(Exhibitor, pk=pk)
    if not user_can_modify_exhibitor(request.user, exhibitor):
        return HttpResponseForbidden()

    fair = get_object_or_404(Fair, year=year)


    invoice_fields = (
    'invoice_reference', 'invoice_reference_phone_number', 'invoice_organisation_name', 'invoice_address',
    'invoice_address_po_box', 'invoice_address_zip_code', 'invoice_identification', 'invoice_additional_information')

    InvoiceForm = modelform_factory(
        Exhibitor,
        fields=invoice_fields
    )

    transport_to_fair_fields = (
    'transport_to_fair_type', 'number_of_packages_to_fair', 'number_of_pallets_to_fair', 'estimated_arrival')

    transport_from_fair_fields = (
    'transport_from_fair_type', 'number_of_packages_from_fair', 'number_of_pallets_from_fair',)

    armada_transport_from_fair_fields = (
    'transport_from_fair_address', 'transport_from_fair_zip_code', 'transport_from_fair_recipient_name',
    'transport_from_fair_recipient_phone_number',)

    stand_fields = (
    'location', 'requests_for_stand_placement', 'heavy_duty_electric_equipment', 'other_information_about_the_stand')

    exhibitor_excluded_fields = armada_transport_from_fair_fields + invoice_fields + transport_from_fair_fields + transport_to_fair_fields + stand_fields

    CompanyForm = modelform_factory(
        Company,
        fields='__all__'
    )

    TransportToFairForm = modelform_factory(
        Exhibitor,
        fields=transport_to_fair_fields,
    )

    TransportFromFairForm = modelform_factory(
        Exhibitor,
        fields=transport_from_fair_fields,
    )

    ArmadaTransportFromFairForm = modelform_factory(
        Exhibitor,
        fields=armada_transport_from_fair_fields,
    )

    StandForm = modelform_factory(
        Exhibitor,
        fields=stand_fields
    )

    ExhibitorForm = modelform_factory(
        Exhibitor,
        exclude=('company', 'fair') + exhibitor_excluded_fields if request.user.has_perm(
            'exhibitors.change_exhibitor') else ('company', 'fair', 'hosts', 'contact') + exhibitor_excluded_fields,
        widgets={'allergies': TextInput()}
    )

    # Because ExhibitorForm has a logo in it, we pass request.FILES to it
    exhibitor_form = ExhibitorForm(request.POST or None, request.FILES or None, instance=exhibitor)
    exhibitor_form.fields[
        'estimated_arrival_of_representatives'].label = 'Estimated arrival of representatives (format: 2016-12-24 13:37)'
    invoice_form = InvoiceForm(request.POST or None, instance=exhibitor)
    transport_to_fair_form = TransportToFairForm(request.POST or None, instance=exhibitor)
    transport_to_fair_form.fields['estimated_arrival'].label = 'Estimaded arrival (format: 2016-12-24 13:37)'
    transport_from_fair_form = TransportFromFairForm(request.POST or None, instance=exhibitor)
    armada_transport_from_fair_form = ArmadaTransportFromFairForm(request.POST or None, instance=exhibitor)
    stand_form = StandForm(request.POST or None, instance=exhibitor)
    company_form = CompanyForm(request.POST or None, instance=exhibitor.company)

    if exhibitor_form.is_valid() and invoice_form.is_valid() and transport_to_fair_form.is_valid() and transport_from_fair_form.is_valid() and company_form.is_valid() and armada_transport_from_fair_form.is_valid() and stand_form.is_valid():
        exhibitor_form.save()
        invoice_form.save()
        transport_to_fair_form.save()
        transport_from_fair_form.save()
        company_form.save()	
        armada_transport_from_fair_form.save()
        stand_form.save()
        return redirect('exhibitors', fair.year)

    users = [(recruitment_application.user, recruitment_application.delegated_role) for recruitment_application in
             RecruitmentApplication.objects.filter(status='accepted').order_by('user__first_name', 'user__last_name')]

    if request.user.has_perm('exhibitors.change_exhibitor'):
        exhibitor_form.fields['hosts'].choices = [('', '---------')] + [
            (user[0].pk, user[0].get_full_name() + ' - ' + user[1].name) for user in users]

    return render(request, template_name, {
        'exhibitor': exhibitor,
        'exhibitor_form': exhibitor_form,
        'invoice_form': invoice_form,
        'transport_to_fair_form': transport_to_fair_form,
        'transport_from_fair_form': transport_from_fair_form,
        'armada_transport_from_fair_form': armada_transport_from_fair_form,
        'company_form': company_form,
        'stand_form': stand_form,
        'fair': fair
    })


def related_object_form(model, model_name, delete_view_name):
    def view(request, year, exhibitor_pk, instance_pk=None, template_name='exhibitors/related_object_form.html'):
        fair = get_object_or_404(Fair, year=year)
        exhibitor = get_object_or_404(Exhibitor, pk=exhibitor_pk)
        if not user_can_modify_exhibitor(request.user, exhibitor):
            return HttpResponseForbidden()
        instance = model.objects.filter(pk=instance_pk).first()
        FormFactory = modelform_factory(model, exclude=(
        'exhibitor', 'user', 'table_name', 'seat_number', 'ignore_from_placement'))
        form = FormFactory(request.POST or None, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.exhibitor = exhibitor
            instance.save()
            return redirect('exhibitor', fair.year,exhibitor_pk)
        delete_url = reverse(delete_view_name, args=(
        fair.year,exhibitor_pk, instance_pk)) if instance_pk != None and delete_view_name != None else None
        return render(request, template_name,
                      {'form': form, 'exhibitor': exhibitor, 'instance': instance, 'model_name': model_name,
                       'delete_url': delete_url, 'fair':fair})

    return view


def related_object_delete(model):
    def view(request, year, exhibitor_pk, instance_pk):
        fair = get_object_or_404(Fair, year=year)
        instance = get_object_or_404(model, pk=instance_pk)
        exhibitor = get_object_or_404(Exhibitor, pk=exhibitor_pk)
        if not user_can_modify_exhibitor(request.user, exhibitor):
            return HttpResponseForbidden()
        instance.delete()
        return redirect('exhibitor', fair.year, exhibitor_pk)

    return view
