import requests
import json
from datetime import date, datetime, timedelta

def register_account():

    first_name = input("First name: ")
    surname = input("Surname: ")
    email = str(input("E-mail: "))
    phone = str(input("Mobile: "))
    username = str(input("Username: "))
    password = str(input("Password: "))
    customer_type = str(input("Personal or Business: "))

    payload = {'first_name': first_name,'surname': surname,'email': email,
    'phone': phone,'username': username,'password': password,'customer_type': customer_type}
    r = requests.post('http://sc15rmdc.pythonanywhere.com/api/register/', data=json.dumps(payload))
    obj = r.json()


    print(r)

register_account()
