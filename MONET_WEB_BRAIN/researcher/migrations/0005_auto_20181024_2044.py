# Generated by Django 2.1.2 on 2018-10-24 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('researcher', '0004_researcherexpscore_gyro_mag'),
    ]

    operations = [
        migrations.RenameField(
            model_name='researcherexpscore',
            old_name='gyro_mag',
            new_name='gyro_x_avg',
        ),
        migrations.AddField(
            model_name='researcherexpscore',
            name='gyro_y_avg',
            field=models.FloatField(default=-1.0),
        ),
        migrations.AddField(
            model_name='researcherexpscore',
            name='gyro_z_avg',
            field=models.FloatField(default=-1.0),
        ),
    ]