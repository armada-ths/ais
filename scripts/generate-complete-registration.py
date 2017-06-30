# This script creates all you need to have a good experience
# while testing the complete registration form.
# It Basically creates some example products to fill ut the form
# Use this script when you've just setup the environment/started using a new branch
#
# INSTRUCTIONS:
#
# 1. Create a superuser with 'manage.py createsuperuser' and make sure that you only have ONE user!
#
# 2. Run 'manage.py shell < generate-complete-registration.py'
#
# Created by Adam Jacobs, June 2017

from django.contrib.auth.models import User
from exhibitors import models
from orders.models import Order, Product, ProductType
from fair.models import Fair
from companies.models import Company, Contact
from datetime import date

# Get super user
u = User.objects.get()

fair = Fair(name="fair1", year=2017, description="description", current=True )
fair.save()

company = Company(name="TestCompany", organisation_type='company')
company.save()

contact = Contact(user=u, belongs_to=company, name="contact name", email="email@hotmail.com", active=True, confirmed=True)
contact.save()

banquetType = ProductType(name="Banquet", description="...")
banquetType.save()
lunchType = ProductType(name="AdditionalLunch", description="...")
lunchType.save()
eventsType = ProductType(name="Events", description="...")
eventsType.save()
roomsType = ProductType(name="Rooms", description="...")
roomsType.save()
novaType = ProductType(name="Nova", description="...")
novaType.save()
standType = ProductType(name="Additional Stand Area", description="...")
standType.save()
heightType = ProductType(name="Additional Stand Height", description="...")
heightType.save()


stand1 = Product(fair=fair, name="2x4 meters +14 000", description="...", price=14000, product_type=standType, coa_number=5)
stand1.save()
stand2 = Product(fair=fair, name="2x5 meters +26 000", description="...", price=26000, product_type=standType, coa_number=5)
stand2.save()
stand3 = Product(fair=fair, name="2x6 meters + 36 000", description="...", price=36000, product_type=standType, coa_number=5)
stand3.save()
stand4 = Product(fair=fair, name="2x7 meters +44 000", description="...", price=44000, product_type=standType, coa_number=5)
stand4.save()
height1 = Product(fair=fair, name="Height 2,31 - 3m +1000", description="...", price=1000, product_type=heightType, coa_number=5)
height1.save()
height2 = Product(fair=fair, name="Height 3 - 5m +2000", description="...", price=1000, product_type=heightType, coa_number=5)
height2.save()
lunch1 = Product(fair=fair, name="Additional lunch tickets day 1 (21 November) +125 /Ticket", description="...", price=125, product_type=lunchType, coa_number=5)
lunch1.save()
lunch2 = Product(fair=fair, name="Additional lunch tickets day 2 (22 November) +125 /Ticket", description="...", price=125, product_type=lunchType, coa_number=5)
lunch2.save()
room1 = Product(fair=fair, name="DIVERSITY ROOM (Base price + 10 000)", description="Students at KTH prioritize companies working with diversity, thus one of THS Armada core values is Diversity. This year a focus room called Diversity Room. Lorem ipsum..", price=10000, product_type=roomsType, coa_number=5)
room1.save()
room2 = Product(fair=fair, name="GREEN ROOM (Base price + 10 000)", description="THS Armada emphasize the importance a sustainable future, therefore an exclusive area of the fair called Green Room. Lorem ipsum..", price=10000, product_type=roomsType, coa_number=5)
room2.save()
event1 = Product(fair=fair, name="INNOVATION NIGHT (15 000 SEK)", description="Innovation night is an opportunity for your company to show how you work with innovation and how employees. Lorem ipsum..", price=15000, product_type=eventsType, coa_number=5)
event1.save()
event2 = Product(fair=fair, name="ARMADA RUN (500 SEK / representative) – under progress", description="lorem ipsum blablllabalbla lorem ipsum blabla.", price=500, product_type=eventsType, coa_number=5)
event2.save()
event3 = Product(fair=fair, name="INDIVIDUAL MEETINGS (10 000 SEK/day)", description="lorem ipsum blablllabalbla lorem ipsum blabla.", price=10000, product_type=eventsType, coa_number=5)
event3.save()
banquet1 = Product(fair=fair, name="Banquet Ticket - Company Representative", description="...", price=1000, product_type=banquetType, coa_number=5)
banquet1.save()
banquet2 = Product(fair=fair, name="Banquet Ticket - Student", description="...", price=1000, product_type=banquetType, coa_number=5)
banquet2.save()
banquet3 = Product(fair=fair, name="Drink Coupon", description="...", price=135, product_type=banquetType, coa_number=5)
banquet3.save()
nova1 = Product(fair=fair, name="NOVA EXCLUSIVE OFFER", description="As a strategic talent attraction and recruitment lorem ipsum.", price=10000, product_type=novaType, coa_number=5)
nova1.save()
