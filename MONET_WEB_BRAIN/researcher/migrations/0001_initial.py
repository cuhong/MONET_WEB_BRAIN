# Generated by Django 2.0.7 on 2018-08-02 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Researcher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('email', models.CharField(max_length=100, unique=True)),
                ('pw', models.CharField(max_length=30)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ResearcherExp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exp_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ResearcherExpScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accuracy', models.FloatField(default=-1.0)),
                ('avg_rt', models.FloatField(default=-1.0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('exp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='researcher.ResearcherExp')),
            ],
        ),
        migrations.CreateModel(
            name='ResearcherExpStimulus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rt', models.FloatField(default=-1.0)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('rgs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='researcher.ResearcherExpScore')),
            ],
        ),
        migrations.CreateModel(
            name='ResearcherPrj',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prj_name', models.CharField(max_length=20)),
                ('comment', models.TextField(max_length=200)),
                ('path', models.CharField(max_length=150)),
                ('researcher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='researcher.Researcher')),
            ],
        ),
        migrations.AddField(
            model_name='researcherexp',
            name='prj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='researcher.ResearcherPrj'),
        ),
    ]
