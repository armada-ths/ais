from django.test import TestCase
from fair.models import Fair
from .models import Exhibitor 
from companies.models import Company, Contact
from orders.models import Order, Product, ProductType 
from django.contrib.auth.models import User
from django.test import Client
from django.core import mail

from django.contrib.auth.models import Permission
from django.template.loader import get_template


# Create your tests here.

class ExhibitorTestCase(TestCase):

    def setUp(self):
        fair = Fair.objects.create(name='Armada 2017', year=2017, current=True)
        user = User.objects.create(username='harry_potter', email='harry@potter.com')
        user.set_password('hej')
        user.save()
        company = Company.objects.create(name='TestCompany', organisation_number='123')
        contact = Contact.objects.create(user=user, belongs_to=company, email=user.email)        

        exhibitor = Exhibitor.objects.create(fair=fair, company=company, contact=contact, pk=1)

        product1 = Product.objects.create(fair=fair, name='product1', coa_number=5, price=100)
        product2 = Product.objects.create(fair=fair, name='product2', coa_number=5, price=200)

        editor = User.objects.create_user(username='editor', password='editor')
        editor.user_permissions.add(Permission.objects.get(codename='view_exhibitors'))


    def testEmailFunction(self):
        client = Client()
        exhibitor = Exhibitor.objects.get(pk=1)

        adminUser = User.objects.create(username='admin', email='admin@admin.com', is_superuser=True)
        adminUser.set_password('hej')
        adminUser.save()
        login=client.login(username='admin', password='hej')
        self.assertEqual(login, True)
        
        #Should NOT work to send email for user without staffstatus 
        response = client.get('/fairs/2017/exhibitors/1/')
        self.assertEqual(response.status_code, 200)
        response = client.get('/fairs/2017/exhibitors/1/send_emails/')
        self.assertEqual(response.status_code, 403)
        response = client.get('/fairs/2017/exhibitors/1/send_cr_receipts')
        self.assertEqual(response.status_code, 403)

        #Should work to send email for user with staff-status
        adminUser.is_staff=True
        adminUser.save()
        response = client.get('/fairs/2017/exhibitors/1/send_emails/')
        self.assertEqual(response.status_code, 200)
        response = client.get('/fairs/2017/exhibitors/1/send_cr_receipts')
        self.assertEqual(response.status_code, 200)
        response = client.get('/fairs/2017/exhibitors/1/emails_confirmation/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)

        #Correct message if no orders
        self.assertEqual(mail.outbox[0].body, get_template('exhibitors/cr_receipt.html').render(({
            'orders_info' : [],
            'total_price' : 0,
            'exhibitor_name' : exhibitor.company.name,
            }))
        )

        #Correct message if adding some orders
        product1= Product.objects.get(name='product1')
        product2=Product.objects.get(name='product2')
        Order.objects.create(exhibitor=exhibitor, product=product1, amount=1)
        Order.objects.create(exhibitor=exhibitor, product=product2, amount=2)

        response = client.get('/fairs/2017/exhibitors/1/send_emails/')
        self.assertEqual(response.status_code, 200)
        response = client.get('/fairs/2017/exhibitors/1/send_cr_receipts')
        self.assertEqual(response.status_code, 200)
        response = client.get('/fairs/2017/exhibitors/1/emails_confirmation/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 2)

        self.assertEqual(mail.outbox[1].body, get_template('exhibitors/cr_receipt.html').render(({
            'orders_info' : [
                {'product' : 'product1', 'price' : 100, 'amount' : 1},
                {'product' : 'product2', 'price' : 400, 'amount' : 2}],
            'total_price' : 500,
            'exhibitor_name' : exhibitor.company.name,
            }))
        )


    def testExhibitorViewEdit_nologin(self):
        client = Client()

        response = client.get('/fairs/2017/exhibitors/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue('?next=' in response.url)

        response = client.get('/fairs/2017/exhibitors/view')
        self.assertEqual(response.status_code, 302)
        self.assertTrue('?next=' in response.url)


    def testExhibitorView(self):
        client = Client()
        
        login=client.login(username='editor', password='editor')
        self.assertTrue(login)

        response = client.get('/fairs/2017/exhibitors/')
        
