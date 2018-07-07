# Generated by Django 2.0.5 on 2018-06-01 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GamePlay', '0007_auto_20180601_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardsorting',
            name='accuracy',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='cardsorting',
            name='cardNum',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='cardsorting',
            name='reactionTime',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='cardsorting',
            name='stage',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='missionsatisfaction',
            name='concentration',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='missionsatisfaction',
            name='mission',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='missionsatisfaction',
            name='satisfaction',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='missionsatisfaction',
            name='underStood',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='nback',
            name='accuracy',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='nback',
            name='nbackNum',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='nback',
            name='nbackStage',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='nback',
            name='reactionTime',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='stroop',
            name='accuracy',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='stroop',
            name='reactionTime',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='stroop',
            name='stage',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='stroop',
            name='stroopStage',
            field=models.CharField(max_length=50),
        ),
    ]