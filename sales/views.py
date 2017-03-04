from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.contrib.auth.decorators import permission_required
import datetime

from .models import SalesPeriod, Campaign, Sale, SaleComment 
from fair.models import Fair
from companies.models import Contact
from recruitment.models import RecruitmentApplication
from companies.models import Company


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = '__all__'


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = '__all__'

class ImportForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ('campaign',)


class SalesPeriodForm(forms.ModelForm):
    class Meta:
        model = SalesPeriod
        fields = '__all__'

        widgets = {
            "start_date": forms.TextInput(attrs={'class': 'datepicker'}),
            "end_date": forms.TextInput(attrs={'class': 'datepicker'}),
        }


class SaleCommentForm(forms.ModelForm):
    class Meta:
        model = SaleComment
        fields = '__all__'


def sales_list(request, year, template_name='sales/sales_list.html'):
    fair = get_object_or_404(Fair, year=year)
    sales_period = SalesPeriod.objects.filter(fair=fair)
    campaigns = Campaign.objects.filter(sales_period = sales_period)
    sales = Sale.objects.filter(campaign__in = campaigns).order_by('company__name')
    return render(request, template_name, {'sales': sales, 'fair': fair})


def sale_edit(request, year, pk=None, template_name='sales/sale_form.html'):
    fair = get_object_or_404(Fair, year=year)
    sale = None
    if pk != None:
        sale = get_object_or_404(Sale, pk=pk)
    form = SaleForm(request.POST or None, instance=sale)
    users = [(recruitment_application.user, recruitment_application.delegated_role) for recruitment_application in
     RecruitmentApplication.objects.filter(status='accepted').order_by('user__first_name', 'user__last_name')]
    form.fields['responsible'].choices = [('', '---------')] + [
            (user[0].pk, user[0].get_full_name() + ' - ' + user[1].name) for user in users]
    if form.is_valid():
        form.save()
        return redirect('sales', fair.year)
    return render(request, template_name, {'form': form, 'sale': sale, 'fair':fair})

def import_companies(request, year):
    fair = get_object_or_404(Fair, year=year)
    form = ImportForm(request.POST or None)
    if form.is_valid():
        campaign = Campaign.objects.get(pk=request.POST['campaign'])
        for company in Company.objects.all():
            # Create a sale entity
            sale = Sale(campaign=campaign, company=company)
            sale.save()
        return redirect('sales', fair.year)
    return render(request, 'sales/sale_form.html', {'form':form, 'fair':fair})
    


def sale_show(request, year,pk, template_name='sales/sale_show.html'):
    fair = get_object_or_404(Fair, year=year)
    sale = get_object_or_404(Sale, pk=pk)
    comments = SaleComment.objects.filter(sale=sale).order_by('-created_date')
    company_name = sale.company.name
    company_contacts = Contact.objects.filter(belongs_to=sale.company)
    previous_sales = Sale.objects.filter(company=sale.company)
    return render(request, template_name, {'sale': sale, 'comments':comments, 'company_name':company_name, 'company_contacts':company_contacts, 'previous_sales':previous_sales, 'fair':fair})


def sale_delete(request, year, pk, template_name='sales/sale_delete.html'):
    fair = get_object_or_404(Fair, year=year)
    sale = get_object_or_404(Sale, pk=pk)
    sale.delete()
    return redirect('sales', fair.year)


def sale_comment_create(request, year, pk, template_name='sales/sale_show.html'):
    fair = get_object_or_404(Fair, year=year)
    sale = get_object_or_404(Sale, pk=pk)
    comment = SaleComment()
    comment.user = request.user
    comment.sale = sale
    comment.comment = request.POST['comment']
    comment.save()
    return redirect('sale_show', year, pk)



def sale_comment_delete(request, year, sale_pk, comment_pk):
    comment = get_object_or_404(SaleComment, pk=comment_pk)
    comment.delete()
    return redirect('sale_show', year, sale_pk)













