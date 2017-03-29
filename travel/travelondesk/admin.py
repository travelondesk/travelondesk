from django.contrib import admin

# Register your models here.
from .models import ServiceTicket, DemandTicket, Country

class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'intName', 'shortName', 'popular']

class ServiceTicketAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'pubDate', 'modifyDate']
    
class DemandTicketAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'pubDate', 'modifyDate']

admin.site.register(ServiceTicket, ServiceTicketAdmin)
admin.site.register(DemandTicket, DemandTicketAdmin)
admin.site.register(Country, CountryAdmin)