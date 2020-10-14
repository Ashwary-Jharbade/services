# Generated by Django 3.0.4 on 2020-08-14 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0002_useraddressmodel_userpersonaldata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddressmodel',
            name='area',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='useraddressmodel',
            name='city',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='useraddressmodel',
            name='district',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='useraddressmodel',
            name='flat',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='useraddressmodel',
            name='landmark',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='useraddressmodel',
            name='pin',
            field=models.CharField(max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='useraddressmodel',
            name='state',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='useraddressmodel',
            name='street',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='userpersonaldata',
            name='aadhar',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='userpersonaldata',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
