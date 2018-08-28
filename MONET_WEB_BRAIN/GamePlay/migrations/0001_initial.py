# Generated by Django 2.1 on 2018-08-27 08:29

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
                ('stage', models.CharField(max_length=50)),
                ('cardNum', models.CharField(max_length=50)),
                ('cardState', models.CharField(max_length=50)),
                ('accuracy', models.CharField(max_length=50)),
                ('reactionTime', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='GoNoGo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(max_length=50)),
                ('stage', models.CharField(max_length=50)),
                ('gonogoNumber', models.CharField(max_length=50)),
                ('omission_Error', models.CharField(max_length=50)),
                ('comission_Error', models.CharField(max_length=50)),
                ('success', models.CharField(max_length=50)),
                ('reactionTime', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='MissionSatisfaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(max_length=50)),
                ('mission', models.CharField(max_length=50)),
                ('underStood', models.CharField(max_length=50)),
                ('concentration', models.CharField(max_length=50)),
                ('satisfaction', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='NBack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(max_length=50)),
                ('stage', models.CharField(max_length=50)),
                ('nbackStage', models.CharField(max_length=50)),
                ('nbackNum', models.CharField(max_length=50)),
                ('accuracy', models.CharField(max_length=50)),
                ('reactionTime', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Stroop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(max_length=50)),
                ('stage', models.CharField(max_length=50)),
                ('stroopStage', models.CharField(max_length=50)),
                ('accuracy', models.CharField(max_length=50)),
                ('reactionTime', models.CharField(max_length=50)),
            ],
        ),
    ]
