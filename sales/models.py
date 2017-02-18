from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from exhibitors.models import Exhibitor
import datetime
import os

class SalesPeriod(models.Model):
    name = models.CharField(max_length=30)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    fair = models.ForeignKey('fair.Fair') 

    def __str__(self):
        return '%s' % (self.name)   

class Campaign(models.Model):
    name = models.CharField(max_length=30)
    sales_period = models.ForeignKey(SalesPeriod)

    def __str__(self):
        return '%s' % (self.name)

class Sale(models.Model):

    STATUS = (
        ('Not contacted', 'Not contacted'),
        ('Unreachable', 'Unreachable'),
        ('Not interested', 'Not interested'),
        ('Contacted', 'Contacted'),
        ('Interested', 'Interested'),
        ('Will register', 'Will register'), 
        ('Registered', 'Registered'),
        ('FA contacted', 'FA contacted'),
        ('FA on the go', 'FA on the go'),
        ('Pending ad approval','Pending ad approval'),
        ('Ad sent for approval', 'Ad sent for approval'),
        ('Ad wrong', 'Ad wrong'),
        ('Completed', 'Completed'),
        ('Rejected', 'Rejected'),
    )
    
    campaign = models.ForeignKey(Campaign)
    company = models.ForeignKey('companies.Company')
    responsible = models.ForeignKey(User, null=True, default=None, blank=True)

    status = models.CharField(max_length=30, choices=STATUS, null=True, default='not_contacted', blank=False)

    def __str__(self):
        return '%s at %s (%s)' % (self.exhibitor.company.name, self.campaign.name, self.campaign.sales_period.fair.year)

class SaleComment(models.Model):
    sale = models.ForeignKey(Sale)
    user = models.ForeignKey(User)
    created_date = models.DateTimeField(default=timezone.now, blank=True)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.user, self.created_date)

def one_week_ahead():
    return timezone.now() + timezone.timedelta(days=7)

class FollowUp(models.Model):
    STATUS = (
        ('contact_them', 'Contact them'),
        ('contact_us', 'Contact us'),
        ('no_follow_up', 'No follow up'),
    )

    sale = models.ForeignKey(Sale)
    status = models.CharField(max_length=30, choices=STATUS, null=True, default=None, blank=True)
    follow_up_date = models.DateTimeField(default=one_week_ahead, blank=True)

    def __str__(self):
        return '%s' % (self.follow_up_date)

  





