# Generated by Django 2.1 on 2018-08-29 19:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.PositiveIntegerField(default=0)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Balloon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('txt', models.CharField(max_length=50)),
                ('rt', models.FloatField(default=-1.0)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('response', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='BalloonScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rt', models.FloatField(default=-1.0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BalloonText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('txt', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CardsortScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(default=-1.0)),
                ('rt', models.FloatField(default=-1.0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CardsortStimulus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rt', models.FloatField(default=-1.0)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('cs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.CardsortScore')),
            ],
        ),
        migrations.CreateModel(
            name='DigitNbackScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(default=-1.0)),
                ('rt', models.FloatField(default=-1.0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DigitNbackStimulus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rt', models.FloatField(default=-1.0)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('ds', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.DigitNbackScore')),
            ],
        ),
        migrations.CreateModel(
            name='GonogoScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(default=-1.0)),
                ('rt', models.FloatField(default=-1.0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GonogoStimulus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rt', models.FloatField(default=-1.0)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('gs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.GonogoScore')),
            ],
        ),
        migrations.CreateModel(
            name='ImageNbackScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(default=-1.0)),
                ('rt', models.FloatField(default=-1.0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ImageNbackStimulus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rt', models.FloatField(default=-1.0)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('ims', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.ImageNbackScore')),
            ],
        ),
        migrations.CreateModel(
            name='Stroop2Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(default=-1.0)),
                ('rt', models.FloatField(default=-1.0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Stroop2Stimulus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rt', models.FloatField(default=-1.0)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('s2s', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Stroop2Score')),
            ],
        ),
        migrations.CreateModel(
            name='StroopScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(default=-1.0)),
                ('rt', models.FloatField(default=-1.0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StroopStimulus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rt', models.FloatField(default=-1.0)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('ss', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.StroopScore')),
            ],
        ),
        migrations.CreateModel(
            name='TetrisScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=-1.0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='balloon',
            name='bs',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.BalloonScore'),
        ),
    ]
