from django.shortcuts import render, redirect
from django.core.validators import validate_email
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

import datetime

from .models import Course_module, Student, Lecturer
 
def login_required(view_function):
    def new_view_function(request):
        if 'email' in request.session:
            return view_function(request)
        else:
            template = 'timetable/login.html'
            return render(request,template)
    return new_view_function

def is_lecturer(view_function):
    def new_view_function(request):
        try:
            lecturer = Lecturer.objects.get(username=request.user)
            return view_function(request)
        except Exception as e:
            print(e)
            template = 'timetable/accessdenied.html'
            return render(request,template)
    return new_view_function

def index(request):
    return render(request, 'timetable/index.html')

def about(request):
    return render(request, 'timetable/about.html')


# lists all of the demonstrators (maybe implement a search and filter)
@login_required
@is_lecturer
def viewDemonstrators(request):
    student = Student.objects.order_by('year_of_study')
    paginator = Paginator(student, 4)
    page = request.GET.get('page')
    page_of_students = paginator.get_page(page)
    context = {
    'student': page_of_students
    }
    return render(request, 'timetable/demonstrators.html', context)


def register(request):
    year_of_study = Student.YEAR_OF_STUDY_CHOICES
    
    if not ('email' in request.POST and 'password' in request.POST and 'year_of_study' in request.POST and 'qualifications' in request.POST):
        return render(request, 'timetable/register.html',{
        'year_of_study':year_of_study
        })
    if not (request.POST['email'] and request.POST['password'] and request.POST['password'] and request.POST['qualifications']):
        return render(request, 'timetable/register.html',{
        'error_message':'Please enter all the fields.',
        'year_of_study':year_of_study
        })
    else:
        email = request.POST['email']
        try: 
            validate_email(email)
        except:
            return render(request, 'timetable/register.html',{
            'year_of_study':year_of_study,
            'error_message':'Please enter a proper email address!'
            })

        password = request.POST['password']
        year_of_study_ToSave = request.POST['year_of_study']
        qualifications = request.POST['qualifications']
        user = Student(username=email, email=email, year_of_study=year_of_study_ToSave, qualifications=qualifications)
        user.set_password(password)
        try:
            user.save()
        except IntegrityError:
            error ='User with that email ' + email + ' already exists!'
            return render(request, 'timetable/register.html', {
                'year_of_study':year_of_study,
                'error_message':error
            })
        return render(request, 'timetable/login.html')


@login_required
def viewProfile(request):
    if 'view' in request.GET:
        view = request.GET['view']
        if request.user.is_staff:
            try:
                lecturer = Lecturer.objects.get(username=request.user)
                student_user = Student.objects.get(username=view)
            except Student.DoesNotExist:
                raise Http404('Student does not exist')
            # create an empty list to store the lecturer modules to make a comparison later
            modulesInterested = []
            modulesAccepted =[]

            # loops through all the modules of the lecturer currently logged in so cannot see other tamper with other
            # lecturer modules








            for module in lecturer.lecturerModules.all():
        # loops through all of the student modules that they are interested in TAing
                for studentModule in student_user.course_id_interest.all():
                    # if statement to check which ones match the lecturer modules 
                    if module == studentModule:
                        # append the modules that match into the empty list
                        modulesInterested.append(module)

                for studentModule in student_user.is_demonstrating.all():
                    if module == studentModule:
                        # append the modules that match into the empty list
                        modulesAccepted.append(module)
            context = {
                'modulesInterested': modulesInterested,
                'modulesAccepted':modulesAccepted, 
                'username': student_user.username,
                'year_of_study': student_user.year_of_study,
                'qualifications': student_user.qualifications,
            }







            return render(request, 'timetable/studentprofile.html', context)
    else:
        students = Student.objects.get(username=request.user)
        context = {
            'year_of_study': students.year_of_study,
            'qualifications': students.qualifications,
            'interested': students.course_id_interest.all(),
            'demonstrating': students.is_demonstrating.all()
        }
        return render(request, 'timetable/profile.html', context)

@login_required
def lecturerProfile(request):
    lecturer = Lecturer.objects.get(username=request.user)
    context = {
        'modules': lecturer.lecturerModules.all()
    }
    return render(request, 'timetable/lecturerprofile.html',context)

@login_required
def editProfile(request):
    students = Student.objects.get(username=request.user)
    if('interestedList[]' in request.POST and 'qual' in request.POST):
        interestedList = request.POST.getlist("interestedList[]")
        qual = request.POST["qual"]
        students.qualifications = qual
        students.course_id_interest.clear()
        interestedList = interestedList[1:len(interestedList)]
        if(len(interestedList) != 0):
            for x in interestedList:
                courseToAdd = Course_module.objects.get(course_ID=x)
                students.course_id_interest.add(courseToAdd)
        try:
            students.save()
        except IntegrityError:
            print("Error")
        return redirect(viewProfile)
    else:
        context = {
            'year_of_study': students.year_of_study,
            'qualifications': students.qualifications,
            'interested': students.course_id_interest.all()
        }
        return render(request, 'timetable/editprofile.html', context)

@login_required
def viewModules(request):
    course = Course_module.objects.order_by('course_ID')
    paginator = Paginator(course, 5)
    page = request.GET.get('page')
    page_of_modules = paginator.get_page(page)
    context = {
    'course': page_of_modules,
    }
    return render(request, 'timetable/modules.html', context)

def loginMate(request):
    if not ('email' in request.POST and 'password' in request.POST):
        return render(request, 'timetable/login.html')
    else:
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            request.session['email'] = email
            context = {'user': user}
            response = redirect(viewModules)

            currentDateTime = datetime.datetime.utcnow()
            max_expiry = 60 * 60  #one hour
            expiryDate = currentDateTime + datetime.timedelta(seconds=max_expiry)
            format = "%a, %d-%b-%Y %H:%M:%S GMT"
            expiryDateString = datetime.datetime.strftime(expiryDate, format)
            response.set_cookie('login',currentDateTime,expires=expiryDateString)
            return response
        else:
            return render(request, 'timetable/login.html', {'error_message':'Invalid login details, please try again.'})

@login_required
def registerInterest(request):
    courseID = request.POST['courseID']
    student = Student.objects.get(username=request.user)
    courseToAdd = Course_module.objects.get(course_ID=courseID)
    student.course_id_interest.add(courseToAdd)
    return redirect(viewModules)

@login_required
def approveDemonstrator(request):
    courseID = request.POST['courseID']
    username = request.POST['username']
    studentSelected = Student.objects.get(username=username)

    course = Course_module.objects.get(course_ID=courseID)
    studentSelected.is_demonstrating.add(course)
    studentSelected.course_id_interest.remove(course)
    modulesInterested = []
    modulesAccepted =[]
    # loops through all the modules of the lecturer currently logged in so cannot see other tamper with other
    # lecturer modules
    lecturer = Lecturer.objects.get(username=request.user)
    for module in lecturer.lecturerModules.all():
        # loops through all of the student modules that they are interested in TAing
        for studentModule in studentSelected.course_id_interest.all():
            # if statement to check which ones match the lecturer modules 
            if module == studentModule:
                # append the modules that match into the empty list
                modulesInterested.append(module)

        for studentModule in studentSelected.is_demonstrating.all():
            if module == studentModule:
                # append the modules that match into the empty list
                modulesAccepted.append(module)
    context = {
        'modulesInterested': modulesInterested,
        'modulesAccepted':modulesAccepted, 
        'username': studentSelected.username,
        'year_of_study': studentSelected.year_of_study,
        'qualifications': studentSelected.qualifications,
    }
    return render(request, 'timetable/studentprofile.html', context)

@login_required
def removeDemonstrator(request):
    courseID = request.POST['courseID']
    username = request.POST['username']
    studentSelected = Student.objects.get(username=username)

    course = Course_module.objects.get(course_ID=courseID)
    studentSelected.course_id_interest.add(course)
    studentSelected.is_demonstrating.remove(course)
    modulesInterested = []
    modulesAccepted =[]

    lecturer = Lecturer.objects.get(username=request.user)
    for module in lecturer.lecturerModules.all():
        # loops through all of the student modules that they are interested in TAing
        for studentModule in studentSelected.course_id_interest.all():
            # if statement to check which ones match the lecturer modules 
            if module == studentModule:
                # append the modules that match into the empty list
                modulesInterested.append(module)

        for studentModule in studentSelected.is_demonstrating.all():
            if module == studentModule:
                # append the modules that match into the empty list
                modulesAccepted.append(module)
    context = {
        'modulesInterested': modulesInterested,
        'modulesAccepted':modulesAccepted, 
        'username': studentSelected.username,
        'year_of_study': studentSelected.year_of_study,
        'qualifications': studentSelected.qualifications,
    }
    return render(request, 'timetable/studentprofile.html', context)

        
                

