from django.contrib import admin
from .models import Aircraft, Airport, Passenger, Flight, Booking, PaymentProvider, Invoice

admin.site.register(Aircraft)
admin.site.register(Airport)
admin.site.register(Passenger)
admin.site.register(Flight)
admin.site.register(Booking)
admin.site.register(PaymentProvider)
admin.site.register(Invoice)


# Register your models here.
