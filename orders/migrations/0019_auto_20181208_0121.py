# Generated by Django 2.1.3 on 2018-12-07 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0018_subscriptionorderitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriptionorderitem',
            name='order',
        ),
        migrations.DeleteModel(
            name='SubscriptionOrderItem',
        ),
    ]