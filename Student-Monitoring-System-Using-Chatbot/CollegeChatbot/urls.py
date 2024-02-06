"""StudentAttendanceManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from chatbot.views import login, logout, activateAccount, facultyregistration, studentregistration, \
    getfacultys, \
    getstudents, \
    deletefaculty, deletestudent, viewattendanceaction, addattendance, submitattendanceaction, addmarks, \
    viewpercentage, viewstudentpercentage, viewstudentpercentageaction, addinternship, viewstudentinternshipaction, \
    get_bot_response

from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [

    # Add the landing page URL pattern
    path('', TemplateView.as_view(template_name='landing_page.html'), name='landing_page'),

    path('admin/', admin.site.urls),

    #path('',TemplateView.as_view(template_name = 'index.html'),name='login'),
    path('login/',TemplateView.as_view(template_name = 'index.html'),name='login'),
    path('loginaction/',login,name='loginaction'),
    path('activateAccount/',activateAccount,name='activateAccount'),
    path('logout/',logout,name='logout'),

    path('facultyregistration/',TemplateView.as_view(template_name = 'facultyregistration.html'),name='registration'),
    path('facultyregaction/',facultyregistration,name='regaction'),

    path('studentregistration/',TemplateView.as_view(template_name = 'studentregistration.html'),name='registration'),
    path('studentregaction/',studentregistration,name='regaction'),

    path('getstudents/',getstudents,name='regaction'),
    path('getfacultys/',getfacultys,name='regaction'),

    path('deletestudent/',deletestudent,name='regaction'),
    path('deletefaculty/',deletefaculty,name='regaction'),

    path('addattendance/',TemplateView.as_view(template_name = 'addattendance.html'),name='registration'),
    path('addattendanceaction/',addattendance, name='regaction'),
    path('submitattendance/',submitattendanceaction, name='regaction'),

    path('viewattendance/',TemplateView.as_view(template_name = 'viewattendance.html'),name='regaction'),
    path('viewattendanceaction/',viewattendanceaction, name='regaction'),

    path('addmarks/',TemplateView.as_view(template_name = 'addmarks.html'),name='registration'),
    path('addmarksaction/',addmarks, name='regaction'),

    path('viewpercentage/',TemplateView.as_view(template_name = 'viewpercentage.html'),name='registration'),
    path('viewpercentageaction/',viewpercentage, name='regaction'),

    path('viewstudentpercentage/',TemplateView.as_view(template_name = 'viewstudentwisepercentage.html'),name='registration'),
    path('viewstudentpercentageaction/',viewstudentpercentageaction, name='regaction'),

    path('addinternship/',TemplateView.as_view(template_name = 'addinternship.html'),name='registration'),
    path('addinternshipaction/',addinternship, name='regaction'),

    path('viewinternship/',TemplateView.as_view(template_name = 'viewinternship.html'),name='registration'),
    path('viewinternshipaction/',viewstudentinternshipaction, name='regaction'),

    path('chat/',TemplateView.as_view(template_name = 'chat.html'), name='regaction'),
    path('get/',get_bot_response, name='regaction'),
]
