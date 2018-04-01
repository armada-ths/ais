from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.contrib.auth.decorators import permission_required
import datetime

from .models import Sale, SaleComment
from fair.models import Fair
from companies.models import Contact
from recruitment.models import RecruitmentApplication
from companies.models import Company
from register.models import SignupLog

from .forms import SalesSearchForm

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = '__all__'
        labels = {
            'contact_by_date': 'Contact by date'
        }
        widgets = {
            'contact_by_date': forms.DateInput(attrs = {'placeholder' : 'YYYY-MM-DD'})
        }
        exclude = ('preliminary_registration',)

class ImportForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ('fair',)

class SaleCommentForm(forms.ModelForm):
    class Meta:
        model = SaleComment
        fields = '__all__'

@permission_required('sales.base')
def sales_list(request, year, template_name='sales/sales_list.html'):
    fair = get_object_or_404(Fair, year=year)
    sales_list = Sale.objects.filter(fair=fair).order_by('company__name')
    my_sales = filter(lambda sale: sale.responsible == request.user, sales_list)
    signups = SignupLog.objects.filter(contract__fair=fair)
    signedup = [signup.company.name for signup in signups]
    
    users = [(recruitment_application.user, recruitment_application.delegated_role) for recruitment_application in RecruitmentApplication.objects.filter(status='accepted', recruitment_period__fair=fair).order_by('user__first_name', 'user__last_name')]
    
    search_form = SalesSearchForm(request.GET or None)
    search_form.fields['responsible'].choices = [('', '---------')] + [(user[0].pk, user[0].get_full_name()) for user in users]

    if search_form.is_valid():
        sales_list = search_form.sales_matching_search(sales_list, fair)
    
    class SearchField(object):
        def __init__(self, name, model_field_name):
            self.name = name
            self.model_field_name = model_field_name
    
    search_fields = [
        SearchField('Company', 'sale__company'),
        SearchField('Responsible', 'sale__responsible'),
        SearchField('Status', 'sale__status'),
        SearchField('Contact by', 'sale__contact_by_date'),
        SearchField('DR', 'sale__diversity_room'),
        SearchField('GR', 'sale__green_room'),
        SearchField('E', 'sale__events'),
        SearchField('Nova', 'sale__nova'),
        SearchField('Registered', None),
    ]
    
    return render(request, template_name, {'sales': sales_list, 'fair': fair, 'my_sales': my_sales, 'signedup': signedup, 'search_form': search_form, 'search_fields': search_fields })

@permission_required('sales.base')
def sale_edit(request, year, pk=None, template_name='sales/sale_form.html'):
    fair = get_object_or_404(Fair, year=year)
    sale = None
    if pk != None:
        sale = get_object_or_404(Sale, pk=pk)
    form = SaleForm(request.POST or None, instance=sale)
    users = [(recruitment_application.user, recruitment_application.delegated_role) for recruitment_application in
     RecruitmentApplication.objects.filter(status='accepted', recruitment_period__fair=fair).order_by('user__first_name', 'user__last_name')]

    form.fields['responsible'].choices = [('', '---------')] + [
            (user[0].pk, user[0].get_full_name() + ' - ' + user[1].name) for user in users]
    if form.is_valid():
        form.save()
        return redirect('sales', fair.year)
    return render(request, template_name, {'form': form, 'sale': sale, 'fair':fair})

@permission_required('sales.base')
def import_companies(request, year):
    fair = get_object_or_404(Fair, year=year)
    form = ImportForm(request.POST or None)
    if form.is_valid():
        for company in Company.objects.all():
            # Create a sale entity
            sale = Sale(fair=fair, company=company)
            sale.save()
        return redirect('sales', fair.year)
    return render(request, 'sales/sale_form.html', {'form':form, 'fair':fair})

@permission_required('sales.base')
def sale_show(request, year,pk, template_name='sales/sale_show.html'):
    fair = get_object_or_404(Fair, year=year)
    sale = get_object_or_404(Sale, pk=pk)
    comments = SaleComment.objects.filter(sale=sale).order_by('-created_date')
    company_name = sale.company.name
    company_contacts = Contact.objects.filter(belongs_to=sale.company)
    previous_sales = Sale.objects.filter(company=sale.company)
    signups = SignupLog.objects.filter(company=sale.company, contract__fair=fair)
    return render(request, template_name, {'sale': sale,
                                            'comments':comments,
                                            'company_name':company_name,
                                            'company_contacts':company_contacts,
                                            'previous_sales':previous_sales,
                                            'fair':fair,
                                            'signups':signups})

@permission_required('sales.base')
def sale_delete(request, year, pk, template_name='sales/sale_delete.html'):
    fair = get_object_or_404(Fair, year=year)
    sale = get_object_or_404(Sale, pk=pk)
    sale.delete()
    return redirect('sales', fair.year)

@permission_required('sales.base')
def sale_comment_create(request, year, pk, template_name='sales/sale_show.html'):
    fair = get_object_or_404(Fair, year=year)
    sale = get_object_or_404(Sale, pk=pk)
    comment = SaleComment()
    comment.user = request.user
    comment.sale = sale
    comment.comment = request.POST['comment']
    comment.save()
    return redirect('sale_show', year, pk)

@permission_required('sales.base')
def sale_comment_delete(request, year, sale_pk, comment_pk):
    comment = get_object_or_404(SaleComment, pk=comment_pk)
    comment.delete()
    return redirect('sale_show', year, sale_pk)
