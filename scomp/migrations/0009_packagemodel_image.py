# Generated by Django 3.0.4 on 2020-08-13 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scomp', '0008_advantagemodel_offermodel_packagemodel_packagetypemodel_termmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='packagemodel',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='packageImagesFolder'),
        ),
    ]
