from django.db import models
from datetime import timedelta

class Aircraft(models.Model):
    aircraft_type = models.CharField(max_length=20)
    aircraft_regNum = models.CharField(max_length=10)
    aircraft_seats = models.PositiveIntegerField()

    def __str__(self):
        return self.aircraft_type

class Airport(models.Model):
    airport_name = models.CharField(max_length=30)
    airport_country = models.CharField(max_length=30)
    airport_timeZone = models.CharField(max_length=30)

    def __str__(self):
        return self.airport_name

class Passenger(models.Model):
    passenger_firstName = models.CharField(max_length=20)
    passenger_surname = models.CharField(max_length=20)
    passenger_email = models.EmailField()
    passenger_mobile = models.CharField(max_length=15)

    def __str__(self):
        return u'%s %s' % (self.passenger_firstName, self.passenger_surname)

class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    depart_airport = models.ForeignKey(Airport, related_name='departure', on_delete=models.CASCADE)
    dest_airport = models.ForeignKey(Airport, related_name='destination', on_delete=models.CASCADE)
    depart_dateTime = models.DateTimeField()
    arrive_dateTime = models.DateTimeField()
    flight_duration = models.DurationField()
    flight_aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    seat_price = models.PositiveIntegerField()

    def __str__(self):
        return "Flight number: %s \n Departure airport: %s \n Destination airport: %s \n Departure time: %s \n Arrival time: %s \n Flight duration: %s \n Seat price: %s \n" % (self.flight_number,
        self.depart_airport, self.dest_airport,self.depart_dateTime,
         self.arrive_dateTime, self.flight_duration, self.seat_price)


class Booking(models.Model):
    STATUS_CHOICES = (
        ('ONHOLD','ONHOLD'),
        ('CONFIRMED','CONFIRMED'),
        ('CANCELLED','CANCELLED'),
        ('TRAVELLED','TRAVELLED'),
    )

    booking_number = models.CharField(max_length=10, unique=True)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    booked_seats = models.PositiveIntegerField()
    passenger = models.ManyToManyField(Passenger)
    booking_status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='ONHOLD')
    booking_duration = models.DurationField(default=timedelta(minutes=20))

    def __str__(self):
        return self.booking_number

class PaymentProvider(models.Model):
    provider_name = models.CharField(max_length=30)
    provider_address = models.URLField()
    account_num = models.IntegerField()
    airline_username = models.CharField(max_length=20, default='')
    airline_password = models.CharField(max_length=30, default='')

    def __str__(self):
        return self.provider_name

class Invoice(models.Model):
    # invoice_airline_num = models.CharField(max_length=10, unique=True)
    invoice_provider_num = models.CharField(max_length=10, unique=True, blank=True)
    invoice_book_num = models.OneToOneField(Booking, on_delete=models.CASCADE)
    invoice_amount = models.PositiveIntegerField()
    invoice_status = models.BooleanField(default=False)
    invoice_stamp = models.CharField(max_length=10, blank=True)
