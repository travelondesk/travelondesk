from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=1000)
    intName = models.CharField(max_length=1000, blank=True)
    shortName = models.CharField(max_length=3, blank=True)
    popular = models.BooleanField(default=False, blank=True)
    def __str__(self):
        return self.name
    def countService(self):
        return ServiceTicket.objects.filter(countryTable=self.id).count()
    def countDemand(self):
        return DemandTicket.objects.filter(countryTable=self.id).count()
    
# Класс тикет
class Ticket(models.Model):
    name = models.CharField(max_length=1000)
    author = models.ForeignKey('auth.User')
    pubDate = models.DateTimeField(blank=True)
    modifyDate = models.DateTimeField(auto_now=True, blank=True)
    description = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    place = models.CharField(max_length=1000)
    latitude = models.CharField(max_length=1000, blank=True, null=True)
    longitude = models.CharField(max_length=1000, blank=True, null=True)
    country = models.CharField(max_length=1000, blank=True, null=True)
    countryShort = models.CharField(max_length=3, blank=True)
    region = models.CharField(max_length=1000, blank=True, null=True)
    city = models.CharField(max_length=1000, blank=True, null=True)
    countryTable = models.ForeignKey(Country, blank=True, null=True, default=None)
    state_choices = (
        ('active', _('Active')),
        ('nonactive', _('Non active'))
    )
    state = models.CharField(max_length=10, choices=state_choices, default='active')
    category_choices = (
        ('rent', _('Rent')),
        ('service', _('Service')),
        ('goods', _('Goods')),
        ('other', _('Other')),
    )
    category = models.CharField(max_length=10, choices=category_choices, default='service')
    img = models.ImageField(upload_to='media', blank=True, null=True)

    class Meta:
        abstract = True
    
class ServiceTicket(Ticket):
    coast = models.CharField(max_length=10, blank=True, null=True)
    
    
class DemandTicket(Ticket):
    coast = models.CharField(max_length=10, blank=True, null=True)
