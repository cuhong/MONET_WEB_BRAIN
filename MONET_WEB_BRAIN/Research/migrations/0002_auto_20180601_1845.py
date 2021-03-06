# Generated by Django 2.0.5 on 2018-06-01 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Research', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mindstate',
            name='anger',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='mindstate',
            name='appearance',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='mindstate',
            name='attitude',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='selfevaluation',
            name='friend_value',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='selfevaluation',
            name='parent_value',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='selfevaluation',
            name='self_value',
            field=models.CharField(max_length=50),
        ),
    ]
