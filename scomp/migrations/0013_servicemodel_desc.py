# Generated by Django 3.0.4 on 2020-08-26 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scomp', '0012_notificationmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicemodel',
            name='desc',
            field=models.CharField(default='', max_length=200),
        ),
    ]
