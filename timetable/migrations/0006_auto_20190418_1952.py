# Generated by Django 2.1.7 on 2019-04-18 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0005_auto_20190412_2221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='is_student',
        ),
        migrations.AlterField(
            model_name='student',
            name='year_of_study',
            field=models.CharField(choices=[('4', 'Masters Student'), ('5', 'PhD Student'), ('3', 'Third Year Student'), ('2', 'Second Year Student')], default='', max_length=1),
        ),
    ]
