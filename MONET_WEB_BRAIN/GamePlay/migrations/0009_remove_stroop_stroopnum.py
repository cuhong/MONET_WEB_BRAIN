# Generated by Django 2.0.5 on 2018-06-05 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GamePlay', '0008_auto_20180601_1845'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stroop',
            name='stroopNum',
        ),
    ]
