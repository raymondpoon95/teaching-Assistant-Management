# Generated by Django 2.1.7 on 2019-03-13 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0002_auto_20190313_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='year_of_study',
            field=models.CharField(choices=[('3', 'Third Year Student'), ('5', 'PhD Student'), ('2', 'Second Year Student'), ('4', 'Masters Student')], default='', max_length=1),
        ),
    ]
