# Generated by Django 3.0.4 on 2020-08-13 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('scomp', '0009_packagemodel_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scomp.PackageModel')),
                ('userreg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scomp.UserRegistrationModel')),
            ],
            options={
                'unique_together': {('package', 'userreg')},
            },
        ),
    ]