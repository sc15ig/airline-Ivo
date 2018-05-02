"""cwk_1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from flights.views import find_flight, book_flight, payment_methods, pay_for_booking, finalize_booking, booking_status, cancel_booking

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/findflight/$', find_flight),
    url(r'^api/bookflight/$', book_flight),
    url(r'^api/paymentmethods/$', payment_methods),
    url(r'^api/payforbooking/$', pay_for_booking),
    url(r'^api/finalizebooking/$', finalize_booking),
    url(r'^api/bookingstatus/$', booking_status),
    url(r'^api/cancelbooking/$', cancel_booking)
]
