# Generated by Django 2.0.1 on 2018-02-22 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0003_remove_flight_aircraft_seats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='flight_duration',
            field=models.DurationField(),
        ),
    ]