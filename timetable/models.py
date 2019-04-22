from django.db import models
from django.contrib.auth.models import User


class Course_module(models.Model):
    course_ID = models.CharField(max_length=10)
    course_name = models.CharField(max_length=50)

    def __str__(self):
        return self.course_ID

class Student(User):
    YEAR_OF_STUDY_CHOICES = {
        ('2', 'Second Year Student'),
        ('3', 'Third Year Student'),
        ('4','Masters Student'),
        ('5','PhD Student')
    }

    course_id_interest = models.ManyToManyField(Course_module, related_name='course_interest', blank=True)
    is_demonstrating = models.ManyToManyField(Course_module, related_name='course_demonstrating',blank=True)
    year_of_study = models.CharField(max_length=1, choices=YEAR_OF_STUDY_CHOICES, default='')
    qualifications = models.TextField(default='No qualifications', blank=False)

    def __str__(self):
        return self.username

class Lecturer(User):
    lecturerModules = models.ManyToManyField(Course_module)

    def __str__(self):
        return self.username
