# Generated by Django 5.2 on 2025-07-10 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0008_alter_booking_vehicle_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='vehicle_latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='vehicle_longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
