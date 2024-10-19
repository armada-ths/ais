import csv

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.forms import modelformset_factory

from fair.models import Fair
from companies.models import Company
from accounting.models import Product, Order
from exhibitors.models import Exhibitor

from .models import Order, Product, ExportBatch
from .forms import (
    GenerateCompanyInvoicesForm,
    BaseCompanyCustomerIdFormSet,
    CompanyCustomerIdForm,
)


@permission_required("accounting.base")
def accounting(request, year):
    fair = get_object_or_404(Fair, year=year)

    return render(request, "accounting/accounting.html", {"fair": fair})


@permission_required("accounting.base")
@permission_required("accounting.export_orders")
def export_orders(request, year):
    fair = get_object_or_404(Fair, year=year)
    orders = (
        Order.objects.filter(product__revenue__fair=fair, export_batch=None)
        .exclude(purchasing_company=None)
        .exclude(unit_price=0)
    )

    companies = []

    for order in orders:
        if (
            order.purchasing_company not in companies
            and order.purchasing_company.has_invoice_address()
            and order.purchasing_company.ths_customer_id is not None
        ):
            companies.append(order.purchasing_company)

    form_generate_company_invoices = GenerateCompanyInvoicesForm(
        request.POST if request.POST else None,
        initial={
            "text": fair.name
            + "."
            + " For questions and feedback, please contact armada@ths.kth.se."
        },
    )

    companies.sort(key=lambda x: x.name)
    form_generate_company_invoices.fields["companies"].choices = [
        (company.pk, company.name) for company in companies
    ]

    if request.POST and form_generate_company_invoices.is_valid():
        if form_generate_company_invoices.cleaned_data["mark_exported"]:
            export_batch = ExportBatch(user=request.user)
            export_batch.save()
            filename = (
                "fakturaunderlag " + export_batch.timestamp.strftime("%s") + ".txt"
            )

        else:
            export_batch = None
            filename = "fakturaunderlag.txt"

        invoices = []

        for company in form_generate_company_invoices.cleaned_data["companies"]:
            if company not in companies:
                continue

            orders_company = []

            for order in orders:
                if order.purchasing_company == company:
                    orders_company.append(order)

            if len(orders_company) != 0:
                invoices.append({"company": company, "orders": orders_company})

        txt = "Rubrik	THS Armada\r\n"
        txt += "Datumformat	YYYY-MM-DD\r\n"

        for invoice in invoices:
            fields_invoice = [""] * 47

            fields_invoice[1] = "Kundfaktura"
            fields_invoice[5] = invoice["company"].ths_customer_id
            fields_invoice[13] = form_generate_company_invoices.cleaned_data[
                "our_reference"
            ]
            fields_invoice[15] = "Faktura ARMADA"
            fields_invoice[16] = form_generate_company_invoices.cleaned_data["text"]
            if (
                invoice["company"].invoice_reference is not None
                and len(invoice["company"].invoice_reference) > 30
            ):
                fields_invoice[16] += (
                    "<CR>Reference: " + invoice["company"].invoice_reference
                )
            if invoice["company"].invoice_email_address is not None:
                fields_invoice[16] += (
                    "<CR>E-mail address: " + invoice["company"].invoice_email_address
                )
            if (
                invoice["company"].invoice_reference is not None
                and len(invoice["company"].invoice_reference) <= 30
            ):
                fields_invoice[17] = invoice["company"].invoice_reference
            if invoice["company"].invoice_address_line_1 is not None:
                fields_invoice[26] += invoice["company"].invoice_address_line_1 + "<CR>"
            if invoice["company"].invoice_address_line_2 is not None:
                fields_invoice[26] += invoice["company"].invoice_address_line_2 + "<CR>"
            if invoice["company"].invoice_address_line_3 is not None:
                fields_invoice[26] += invoice["company"].invoice_address_line_3 + "<CR>"
            fields_invoice[26] += (
                invoice["company"].invoice_zip_code
                + " "
                + invoice["company"].invoice_city
            )
            if invoice["company"].invoice_country != "SWEDEN":
                fields_invoice[26] += "<CR>" + invoice["company"].invoice_country
            if invoice["company"].invoice_name is not None:
                fields_invoice[27] = invoice["company"].invoice_name
            if invoice["company"].e_invoice is not True:
                fields_invoice[44] += str(0)
            else:
                fields_invoice[44] += str(1)

            del fields_invoice[0]

            txt_orders = []

            for order in invoice["orders"]:
                fields_order = [""] * 21

                fields_order[1] = "Fakturarad"
                fields_order[2] = "3"
                fields_order[4] = str(order.quantity)
                fields_order[5] = str(
                    order.unit_price
                    if order.unit_price is not None
                    else order.product.unit_price
                )
                fields_order[8] = order.product.revenue.name
                fields_order[7] = (
                    order.name if order.name is not None else order.product.name
                )
                fields_order[12] = "st"
                fields_order[16] = str(order.product.result_center)
                fields_order[19] = str(order.product.cost_unit)

                del fields_order[0]

                txt_orders.append("\t".join(fields_order))

            txt += "\t".join(fields_invoice) + "\r\n"
            for txt_order in txt_orders:
                txt += txt_order + "\r\n"
            txt += "Kundfaktura-slut\r\n"

        if export_batch is not None:
            for invoice in invoices:
                for order in invoice["orders"]:
                    order.export_batch = export_batch
                    order.save()

        txt = txt.encode("windows-1252")

        response = HttpResponse(txt, content_type="text/plain; charset=windows-1252")
        response["Content-Length"] = len(txt)
        response["Content-Disposition"] = 'attachment; filename="' + filename + '"'

        return response

    return render(
        request,
        "accounting/export_orders.html",
        {
            "fair": fair,
            "missing_ths_customer_ids": companies_with_orders(fair).count(),
            "form_generate_company_invoices": form_generate_company_invoices,
        },
    )


@permission_required("accounting.base")
@permission_required("accounting.ths_customer_ids")
def companies_without_ths_customer_ids(request, year):
    fair = get_object_or_404(Fair, year=year)

    CompanyCustomerIdFormSet = modelformset_factory(
        Company, fields=["invoice_name", "ths_customer_id"], extra=0
    )
    formset = CompanyCustomerIdFormSet(
        request.POST if request.POST else None, queryset=companies_with_orders(fair)
    )

    if request.POST and formset.is_valid():
        formset.save()
        formset = CompanyCustomerIdFormSet(queryset=companies_with_orders(fair))

    return render(
        request,
        "accounting/companies_without_ths_customer_ids.html",
        {"fair": fair, "formset": formset},
    )


@permission_required("accounting.base")
def product_summary(request, year):
    fair = get_object_or_404(Fair, year=year)

    products = []
    j = 1

    for product_raw in Product.objects.filter(revenue__fair=fair):
        product = {
            "i": j,
            "name": product_raw.name,
            "category": product_raw.category.name if product_raw.category else None,
            "unit_price": product_raw.unit_price,
            "orders": [],
            "total_quantity": 0,
            "total_price": 0,
        }

        j += 1

        for order_raw in (
            Order.objects.select_related("export_batch")
            .filter(product=product_raw)
            .order_by("purchasing_company")
        ):
            price = (
                order_raw.unit_price
                if order_raw.unit_price is not None
                else product_raw.unit_price
            ) * order_raw.quantity

            product["orders"].append(
                {
                    "pk": order_raw.id,
                    "purchasing_company": order_raw.purchasing_company,
                    "name": order_raw.name,
                    "quantity": order_raw.quantity,
                    "unit_price": order_raw.unit_price,
                    "price": price,
                    "comment": order_raw.comment,
                }
            )

            product["total_quantity"] += order_raw.quantity
            product["total_price"] += price

        products.append(product)

    grandTotalPrice = 0
    for product in products:
        grandTotalPrice = grandTotalPrice + product["total_price"]

    return render(
        request,
        "accounting/product_summary.html",
        {"fair": fair, "products": products, "grandTotalPrice": grandTotalPrice},
    )


def companies_with_orders(fair):
    orders = (
        Order.objects.filter(product__revenue__fair=fair)
        .exclude(purchasing_company=None)
        .exclude(unit_price=0)
    )
    companies_with_orders = []

    for order in orders:
        if order.purchasing_company.pk not in companies_with_orders:
            companies_with_orders.append(order.purchasing_company.pk)

    companies = Company.objects.filter(
        ths_customer_id=None, id__in=companies_with_orders
    )

    return companies


def export_companys(request, year):
    fair = get_object_or_404(Fair, year=year)
    orders = (
        Order.objects.filter(product__revenue__fair=fair)
        .select_related("product")
        .exclude(purchasing_company=None)
        .exclude(unit_price=0)
    )
    company_order_total = dict()

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="companys.csv"'

    writer = csv.writer(response, delimiter=",", quoting=csv.QUOTE_ALL)
    writer.writerow(
        [
            "Company",
            "Org nr",
            "Address line 1",
            "Address line 2",
            "Postnr",
            "Postort",
            "Country",
            "FakturaRef",
            "Mail",
            "THS Customer ID",
            "Kommentar",
            "Order total without VAT",
        ]
    )

    for order in orders:
        if company_order_total.get(order.purchasing_company.pk) is None:
            company_order_total[order.purchasing_company.pk] = order.quantity * (
                order.unit_price if order.unit_price else order.product.unit_price
            )
        else:
            company_order_total[order.purchasing_company.pk] += order.quantity * (
                order.unit_price if order.unit_price else order.product.unit_price
            )

    for e in Exhibitor.objects.filter(fair__year=year):
        writer.writerow(
            [
                e.company.invoice_name if e.company.invoice_name else e.company.name,
                e.company.identity_number,
                e.company.invoice_address_line_1,
                e.company.invoice_address_line_2,
                e.company.invoice_address_line_3,
                e.company.invoice_zip_code,
                e.company.invoice_city,
                e.company.invoice_country,
                e.company.invoice_email_address,
                e.company.ths_customer_id,
                e.company.invoice_reference,
                (
                    company_order_total.get(e.company.pk)
                    if company_order_total.get(e.company.pk)
                    else None
                ),
            ]
        )

    return response
