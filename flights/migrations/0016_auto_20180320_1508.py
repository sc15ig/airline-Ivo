# Generated by Django 2.0.1 on 2018-03-20 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0015_auto_20180319_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='invoice_amount',
            field=models.PositiveIntegerField(),
        ),
    ]
