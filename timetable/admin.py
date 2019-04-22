from django.contrib import admin
from timetable.models import Course_module, Student, Lecturer

# Register your models here.
admin.site.register(Course_module)
admin.site.register(Lecturer)
admin.site.register(Student)
