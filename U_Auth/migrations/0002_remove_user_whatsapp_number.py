# Generated by Django 4.2.3 on 2023-08-01 05:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('U_Auth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='whatsapp_number',
        ),
    ]