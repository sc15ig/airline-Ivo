# Generated by Django 2.0.1 on 2018-03-19 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0011_remove_flight_is_flex'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='invoice_airline_num',
        ),
    ]
