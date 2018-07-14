# Generated by Django 2.0.5 on 2018-05-31 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CardSorting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(max_length=50)),
                ('stage', models.PositiveIntegerField()),
                ('cardState', models.CharField(max_length=50)),
                ('accurancy', models.FloatField()),
                ('reactionTime', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='GoNoGo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(max_length=50)),
                ('stage', models.PositiveIntegerField()),
                ('gonogoNumber', models.PositiveIntegerField()),
                ('omission_Error', models.BooleanField()),
                ('comission_Error', models.BooleanField()),
                ('success', models.BooleanField()),
                ('reactionTime', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='MissionSatisfaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(max_length=50)),
                ('mission', models.PositiveIntegerField()),
                ('underStood', models.PositiveIntegerField()),
                ('concentration', models.PositiveIntegerField()),
                ('satisfaction', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='NBack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(max_length=50)),
                ('stage', models.PositiveIntegerField()),
                ('nbackStage', models.PositiveIntegerField()),
                ('accurancy', models.FloatField()),
                ('reactionTime', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Stroop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(max_length=50)),
                ('stage', models.PositiveIntegerField()),
                ('stroopStage', models.PositiveIntegerField()),
                ('accurancy', models.FloatField()),
                ('reactionTime', models.FloatField()),
            ],
        ),
    ]