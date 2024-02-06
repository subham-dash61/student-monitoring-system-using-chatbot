from django.db import models

from django.db.models import Model

class FacultyModel(Model):

    username=models.CharField(max_length=50)
    name=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    mobile=models.CharField(max_length=50)
    department=models.CharField(max_length=50)

class StudentModel(Model):

    username=models.CharField(max_length=50)
    name=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    mobile=models.CharField(max_length=50)
    department=models.CharField(max_length=50)
    year=models.CharField(max_length=50)
    section=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    regulation = models.CharField(max_length=50)

class AttendanceModel(Model):

    username=models.CharField(max_length=50,default="")
    date = models.CharField(max_length=50,default="")
    department = models.CharField(max_length=50,default="")
    year = models.CharField(max_length=50,default="")
    semester=models.CharField(max_length=50,default="")
    section = models.CharField(max_length=50,default="")
    subject=models.CharField(max_length=50,default="")
    isattended=models.CharField(max_length=50,default="")

class MarksModel(Model):

    halticket_number=models.CharField(max_length=50,default="")
    Subject_Code=models.CharField(max_length=50,default="")
    Subject_Name=models.CharField(max_length=50,default="")
    Internal_Marks=models.CharField(max_length=50,default="")
    ExterNal_Marks=models.CharField(max_length=50,default="")
    Total=models.CharField(max_length=50,default="")
    Credits=models.CharField(max_length=50,default="")
    year_sem=models.CharField(max_length=50,default="")
    actualmarks=models.CharField(max_length=50,default="")

class InternshipModel(Model):

    halticket_number=models.CharField(max_length=50,default="")
    Company_Name=models.CharField(max_length=50,default="")