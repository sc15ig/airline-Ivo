from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from flights.models import Flight, Booking, Passenger, Airport, PaymentProvider, Invoice
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime, timedelta
import string
from random import choice, choices

import json
import requests
import urllib

session = requests.Session()

from random import randint

# Create your views here.
def find_flight(request):

    if request.method == 'GET':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        dep_airport = body['dep_airport']
        dest_airport = body['dest_airport']
        dep_date = body['dep_date']
        num_passengers = body['num_passengers']
        is_flex = body['is_flex']

        converted_date = datetime.strptime(dep_date, "%Y-%m-%d").date()
        num_passengers = int(num_passengers)
        flights_list=[]
        new_dictionary={}


        if (is_flex == True):
            flights = Flight.objects.filter(depart_dateTime__range=[converted_date - timedelta(days=3), converted_date + timedelta(days=3)], depart_airport__airport_name=dep_airport,
            dest_airport__airport_name=dest_airport)
        elif (is_flex == False):
            flights = Flight.objects.filter(depart_dateTime__startswith=converted_date, depart_airport__airport_name=dep_airport,
        dest_airport__airport_name=dest_airport)


        try:
            dep_a = Airport.objects.get(airport_name=dep_airport)
        except:
            return HttpResponse("Could not create the object dep", status = 503)

        try:
            dest_a = Airport.objects.get(airport_name=dest_airport)
        except:
            return HttpResponse("Could not create the object dest", status = 503)



        for flight in flights:
            flights_dictionary={}
            flights_dictionary['flight_id'] = flight.id
            flights_dictionary['flight_num'] = format(flight.flight_number)
            flights_dictionary['dep_airport'] = format(dep_a)
            flights_dictionary['dest_airport'] = format(dest_a)
            flights_dictionary['dep_datetime'] = format(flight.depart_dateTime.strftime("%Y-%m-%d %H:%M"))
            flights_dictionary['arr_datetime'] = format(flight.arrive_dateTime.strftime("%Y-%m-%d %H:%M"))
            flights_dictionary['duration'] = format(flight.flight_duration)
            flights_dictionary['price'] = format(flight.seat_price)
            flights_list.append(flights_dictionary)
        new_dictionary['flights'] = flights_list

        if flights:
            return HttpResponse(json.dumps(new_dictionary), status=200)
        else:
            return HttpResponse("No flights found!", status=503)


@csrf_exempt
def book_flight(request):

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    num_passenger = 0

    if request.method == 'POST':
        flight_id = body['flight_id']
        passengers = body['passengers']
        print(passengers)
        if passengers:
            passenger_list = []
            for new_passenger in passengers:
                num_passenger += 1
                passenger = Passenger(passenger_firstName=new_passenger['first_name'], passenger_surname=new_passenger['surname'],
                 passenger_email=new_passenger['email'], passenger_mobile=new_passenger['phone'])
                passenger.save()
                passenger_list.append(passenger)

            booked_s = int(len(passengers))
            string_val = "".join(choice(string.ascii_uppercase + string.digits) for i in range(6))
            book_n = str(string_val.upper())
            selected_flight = Flight.objects.filter(pk=flight_id).first()
            tot_price = int(selected_flight.seat_price * num_passenger)


            booking = Booking(booking_number=book_n, flight=selected_flight, booked_seats=booked_s)
            booking.save()
            booking.passenger.set(passenger_list)
            booking.save()

            payload = {}
            payload['booking_num'] = booking.booking_number
            payload['booking_status'] = booking.booking_status
            payload['tot_price'] = tot_price


        if booking:
            return HttpResponse(json.dumps(payload), status=201)
        else:
            return HttpResponse("No seats are available.", status=503)

def payment_methods(request):

    if request.method == 'GET':

        providers = PaymentProvider.objects.all()
        providers_list=[]
        new_dictionary={}

        for provider in providers:
            providers_dictionary={}
            providers_dictionary['pay_provider_id'] = provider.id
            providers_dictionary['pay_provider_name'] = provider.provider_name
            providers_list.append(providers_dictionary)
        new_dictionary['pay_providers'] = providers_list

        if providers:
            return HttpResponse(new_dictionary, status=200)
        else:
            return HttpResponse("No payment providers found!", status=503, safe=False)

@csrf_exempt
def pay_for_booking(request):

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if request.method == 'POST':
        booking_num = body['booking_num']
        pay_provider_id = body['pay_provider_id']

        if booking_num and pay_provider_id:
            selected_provider = PaymentProvider.objects.filter(pk=pay_provider_id).first()
            booking = Booking.objects.filter(booking_number=booking_num).first()
            flight = booking.flight
            seat_price = flight.seat_price
            booked_seats = booking.booked_seats
            amount = seat_price * booked_seats

            if selected_provider and booking:

                username = selected_provider.airline_username
                password = selected_provider.airline_password
                headers={'content-type': 'application/x-www-form-urlencoded'}
                data={'username': username, 'password': password}
                r = session.post('http://sc15rmdc.pythonanywhere.com/api/login/', data=urllib.parse.urlencode(data), headers=headers)
                # print(r.status_code)
                # print(r.text)

                account_num = selected_provider.account_num
                client_ref_num = booking.booking_number


                payload = {'account_num': account_num, 'client_ref_num': client_ref_num, 'amount': amount}
                headers={'content-type': 'application/json'}
                r = session.post('http://sc15rmdc.pythonanywhere.com/api/createinvoice/', data=json.dumps(payload), headers=headers)
                obj = r.json()

                if obj:
                    payprovider_ref_num = obj['payprovider_ref_num']
                    stamp_code = obj['stamp_code']
                    # print(payprovider_ref_num)
                    # print(stamp_code)

                    invoice = Invoice(invoice_provider_num=payprovider_ref_num, invoice_book_num=booking, invoice_amount=amount, invoice_stamp=stamp_code)
                    invoice.save()
                else:
                    print("There is no response from the Payment Provider.")


                client_response = {}
                client_response['pay_provider_id'] = selected_provider.id
                client_response['invoice_id'] = invoice.invoice_provider_num
                client_response['booking_num'] = booking.booking_number
                client_response['url'] = selected_provider.provider_address


                if invoice:
                    return HttpResponse(json.dumps(client_response), status=201)
                else:
                    return HttpResponse("Invoice could not be created!", status=503, safe=False)



@csrf_exempt
def finalize_booking(request):

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if request.method == 'POST':
        booking_num = body['booking_num']
        pay_provider_id = body['pay_provider_id']
        stamp = body['stamp']

        if booking_num and pay_provider_id and stamp:
            booking_number = Booking.objects.filter(booking_number=booking_num).first()
            paid_invoice = Invoice.objects.filter(invoice_book_num=booking_number).first()
            invoice_stamp = paid_invoice.invoice_stamp
            print(paid_invoice)
            print(invoice_stamp)
            if stamp == invoice_stamp:

                booking = Booking.objects.filter(booking_number=booking_num).first()
                booking.booking_status = "CONFIRMED"
                booking.save()

                payload = {}
                payload['booking_num'] = booking.booking_number
                payload['booking_status'] = booking.booking_status
                return HttpResponse(json.dumps(payload), status=201)

            else:
                warning = "Stamp code is not valid."
                return HttpResponse(warning, status=503, safe=False)

def booking_status(request):

    if request.method == 'GET':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        booking_num = body['booking_num']


        if booking_num:
            booking = Booking.objects.filter(booking_number=booking_num).first()
            flight = booking.flight

            payload = {}
            payload['booking_num'] = booking.booking_number
            payload['booking_status'] = booking.booking_status
            payload['flight_num'] = flight.flight_number
            # payload['dep_airport'] = flight.depart_airport
            # payload['dest_airport'] = flight.dest_airport
            payload['dep_datetime'] = format(flight.depart_dateTime.strftime("%Y-%m-%d %H:%M"))
            payload['arr_datetime'] = format(flight.arrive_dateTime.strftime("%Y-%m-%d %H:%M"))
            payload['duration'] = format(flight.flight_duration)

            return HttpResponse(json.dumps(payload), status=200)
        else:
            return HttpResponse("Server could not respond.", status=503, safe=False)

@csrf_exempt
def cancel_booking(request):

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if request.method == 'POST':
        booking_num = body['booking_num']

        if booking_num:
            booking_number = Booking.objects.filter(booking_number=booking_num).first()

            booking = Booking.objects.filter(booking_number=booking_num).first()
            booking.booking_status = "CANCELLED"
            booking.save()

            payload = {}
            payload['booking_num'] = booking.booking_number
            payload['booking_status'] = booking.booking_status
            return HttpResponse(json.dumps(payload), status=201)

        else:
            warning = "Stamp code is not valid."
            return HttpResponse(warning, status=503, safe=False)
