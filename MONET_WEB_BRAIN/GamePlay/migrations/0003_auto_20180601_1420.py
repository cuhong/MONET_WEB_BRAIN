# Generated by Django 2.0.5 on 2018-06-01 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GamePlay', '0002_auto_20180601_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardsorting',
            name='cardNum',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='nback',
            name='nbackNum',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='stroop',
            name='stroopNum',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
