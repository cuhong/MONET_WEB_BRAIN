# Generated by Django 2.0.5 on 2018-05-19 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0009_auto_20180518_1626'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='balloonscore',
            name='score',
        ),
    ]
