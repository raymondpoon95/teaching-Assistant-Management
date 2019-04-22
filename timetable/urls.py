from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('demonstrators/',views.viewDemonstrators, name='view_demonstrators'),
    path('register/',views.register, name='register'),
    path('login/', views.loginMate, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='timetable/logout.html'), name='logout'),
    path('profile/', views.viewProfile, name='profile'),
    path('lecturerprofile/', views.lecturerProfile, name='lecturer_profile'),
    path('editprofile/',views.editProfile,name='editProfile'),
    path('modules/', views.viewModules, name='modules'),
    path('modules/registerInterest/', views.registerInterest, name='registerInterest'),
    path('profile/approveDemonstrator/', views.approveDemonstrator, name='approveDemonstrator'),
    path('profile/removeDemonstrator/', views.removeDemonstrator, name='removeDemonstrator')
]
