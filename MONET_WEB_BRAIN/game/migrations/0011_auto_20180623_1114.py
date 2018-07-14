# Generated by Django 2.0.5 on 2018-06-23 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0010_remove_balloonscore_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='BehavGameScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_name', models.CharField(max_length=20)),
                ('score', models.FloatField(default=-1.0)),
                ('rt', models.FloatField(default=-1.0)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
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
        migrations.AddField(
            model_name='behavgamescore',
            name='researcher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Researcher'),
        ),
        migrations.AddField(
            model_name='behavgamescore',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.User'),
        ),
    ]