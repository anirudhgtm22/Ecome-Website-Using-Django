# Generated by Django 4.1.1 on 2023-03-18 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_customer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='pass1',
            new_name='password',
        ),
    ]
