# Generated by Django 2.0.5 on 2018-06-01 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GamePlay', '0005_auto_20180601_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gonogo',
            name='reactionTime',
            field=models.CharField(max_length=50),
        ),
    ]
