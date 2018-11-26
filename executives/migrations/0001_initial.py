# Generated by Django 2.1.3 on 2018-11-26 18:11

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import executives.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userAuth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Executive',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('fullname', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[ a-zA-Z]*$', 'Only alphabets are allowed.')])),
                ('photo', models.ImageField(blank=True, upload_to=executives.models.upload_path_handler)),
                ('complaints_queue', models.IntegerField(default=0)),
            ],
        ),
    ]
