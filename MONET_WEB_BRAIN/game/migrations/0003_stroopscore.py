# Generated by Django 2.0.4 on 2018-05-16 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20180517_0149'),
    ]

    operations = [
        migrations.CreateModel(
            name='StroopScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(default=-1.0)),
                ('rt', models.FloatField(default=-1.0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.User')),
            ],
        ),
    ]
