from django.contrib.auth.models import User
from exhibitors.models import Exhibitor
from orders.models import Product, ProductType, Order
from companies.models import Company, Contact
from fair.models import Fair

# This script generate a readable invoice text file for each exhibitor
for exhibitor in Exhibitor.objects.filter(fair=Fair.objects.get(current=True)):
    with open('invoice_readable/' + exhibitor.company.name + '.txt','w') as f:
        # File information
        f.write('FAKTURA FÖR: ' + exhibitor.company.name + '\n')
        f.write('\n')
        f.write('------------------------------------------------------------------ \n')
        f.write('Detta dokument innehåller information kring fakturan samt en lista \n')
        f.write('av köp med respektive pris, följt av den totala summan av alla köp \n')
        f.write('OBS: om ett fält i fakturainfot är tomt betyder det att det ej är ifyllt. \n')
        f.write('------------------------------------------------------------------ \n')

        # Invoice information
        f.write('\n')
        f.write('INFORMATION: \n\n')
        f.write('Fakturareferens: ' + exhibitor.invoice_reference + '\n')
        f.write('Köpordernummer: ' + exhibitor.invoice_purchase_order_number + '\n')
        f.write('Referens telefon: ' + exhibitor.invoice_reference_phone_number + '\n')
        f.write('Organisationsnamn: ' + exhibitor.invoice_organisation_name + '\n')
        f.write('Adress: ' + exhibitor.invoice_address + '\n')
        f.write('Postbox: ' + exhibitor.invoice_address_po_box + '\n')
        f.write('Postnummer: ' + exhibitor.invoice_address_zip_code + '\n')
        f.write('Fakturaidentifikation: ' + exhibitor.invoice_identification + '\n')
        f.write('Övrig info: ' + exhibitor.invoice_additional_information + '\n')
        f.write('\n')
        f.write('------------------------------------------------------------------ \n')
        f.write('\n')

        # Order list
        f.write('KÖPLISTA: \n\n')
        for order in Order.objects.filter(exhibitor=exhibitor):
            f.write(order.product.name + ': ' + str(order.amount) + ' x ' + str(order.product.price) + ' = ' + str(order.price()) + '\n')
        f.write('\n')
        f.write('------------------------------------------------------------------ \n')
        f.write('\n')

        # Total sum
        f.write('TOTALA SUMMA: \n')
        f.write(str(exhibitor.total_cost()) + ' SEK \n\n')
        f.write('------------------------------------------------------------------ \n')
