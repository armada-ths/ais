from django.contrib import admin

from .models import *

class CompanyAddressInline(admin.StackedInline):
	model = CompanyAddress

class CompanyLogInline(admin.StackedInline):
	model = CompanyLog

class CompanyCustomerResponsibleInline(admin.StackedInline):
	model = CompanyCustomerResponsible

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
	ordering = ("fair__year", "parent__name", "name",)
	list_display = ("fair", "__str__",)
	list_filter = ("fair__year",)

@admin.register(CompanyContact)
class CompanyContactAdmin(admin.ModelAdmin):
	ordering = ("name",)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
	search_fields = ("name",)
	ordering = ("name",)
	inlines = [CompanyAddressInline, CompanyLogInline]
	
	def save_model(self, request, obj, form, change):
		obj.modified_by = request.user.id
		super(CompanyAdmin, self).save_model(request, obj, form, change)

@admin.register(CompanyType)
class CompanyTypeAdmin(admin.ModelAdmin):
	ordering = ("type",)

@admin.register(CompanyCustomer)
class CompanyCustomerAdmin(admin.ModelAdmin):
	ordering = ("fair__year", "company__name",)
	list_display = ("fair", "company",)
	list_filter = ("fair__year",)
	inlines = [CompanyCustomerResponsibleInline]
