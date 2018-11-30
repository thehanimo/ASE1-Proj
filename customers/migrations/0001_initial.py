# Generated by Django 2.1.3 on 2018-11-30 13:28

import customers.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userAuth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('fullname', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[ a-zA-Z]*$', 'Only alphabets are allowed.')])),
                ('photo', models.ImageField(blank=True, upload_to=customers.models.upload_path_handler)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, unique=True)),
                ('zipcode', models.CharField(default='', max_length=6, validators=[django.core.validators.RegexValidator('^[0-9]{6}$', 'Only 6-digit zipcodes supported.')])),
                ('street', models.CharField(default='', max_length=100)),
                ('area', models.CharField(default='', max_length=30, validators=[django.core.validators.RegexValidator('^[ a-zA-Z]*$', 'Only alphabets are allowed.')])),
            ],
        ),
    ]
