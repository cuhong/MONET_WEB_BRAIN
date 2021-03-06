# Generated by Django 2.0.5 on 2018-06-01 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GamePlay', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cardsorting',
            old_name='accurancy',
            new_name='accuracy',
        ),
        migrations.RenameField(
            model_name='nback',
            old_name='accurancy',
            new_name='accuracy',
        ),
        migrations.RenameField(
            model_name='stroop',
            old_name='accurancy',
            new_name='accuracy',
        ),
        migrations.AddField(
            model_name='cardsorting',
            name='cardNum',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='nback',
            name='nbackNum',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='stroop',
            name='stroopNum',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
