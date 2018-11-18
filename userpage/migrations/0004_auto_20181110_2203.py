# Generated by Django 2.1 on 2018-11-10 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0003_auto_20181106_0134'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.CharField(default='1', max_length=50)),
                ('notifiedfrom', models.CharField(max_length=50)),
                ('message', models.CharField(max_length=500)),
                ('seen', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='ItemsQuantity',
        ),
        migrations.AddField(
            model_name='order',
            name='agentid',
            field=models.CharField(default='a', max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='userid',
            field=models.CharField(default='1', max_length=50),
        ),
    ]