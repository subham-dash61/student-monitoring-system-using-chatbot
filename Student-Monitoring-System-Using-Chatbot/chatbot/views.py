import csv
import datetime

from django.shortcuts import render

from chatbot.forms import FacultyForm, StudentForm, MarksForm
from chatbot.models import FacultyModel,StudentModel,AttendanceModel,MarksModel,InternshipModel

import smtplib
import  os

from chatbot.service import getstudentsemmarks, getstudentsempercentage, getstudentpercentage, getstudentinternships, \
    getstudentsemattendance

PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))

def send_email(email,message):

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("studentfeedback.orbitdsnr@gmail.com", "9663729899")

    # sending the mail
    s.sendmail("studentfeedback.orbitdsnr@gmail.com",email, message)

    # terminating the session
    s.quit()

    return

def facultyregistration(request):

    if request.method == "POST":

        registrationForm = FacultyForm(request.POST)

        if registrationForm.is_valid():

            regModel = FacultyModel()
            regModel.name = registrationForm.cleaned_data["name"]
            regModel.email = registrationForm.cleaned_data["email"]
            regModel.mobile = registrationForm.cleaned_data["mobile"]
            regModel.department = registrationForm.cleaned_data["department"]
            regModel.username = registrationForm.cleaned_data["username"]
            regModel.password = registrationForm.cleaned_data["password"]

            user = FacultyModel.objects.filter(username=regModel.username).first()

            if user is not None:
                return render(request, 'facultyregistration.html', {"message": "User All Ready Exist"})
            else:
                try:
                    regModel.save()
                    return render(request, 'facultyregistration.html', {"message": "Faculty Added Successfully"})
                except:
                    return render(request, 'facultyregistration.html', {"message": "Registration Failed"})
        else:
            return render(request, 'facultyregistration.html', {"message": "Invalid Form"})

    return render(request, 'facultyregistration.html', {"message": "Invalid Request"})

def studentregistration(request):

    if request.method == "POST":

        registrationForm = StudentForm(request.POST)

        if registrationForm.is_valid():

            regModel = StudentModel()
            regModel.name = registrationForm.cleaned_data["name"]
            regModel.email = registrationForm.cleaned_data["email"]
            regModel.mobile = registrationForm.cleaned_data["mobile"]
            regModel.department = registrationForm.cleaned_data["department"]
            regModel.username = registrationForm.cleaned_data["username"]
            regModel.password = registrationForm.cleaned_data["password"]
            regModel.year = registrationForm.cleaned_data["year"]
            regModel.section = registrationForm.cleaned_data["section"]
            regModel.status ="no"
            regModel.regulation = registrationForm.cleaned_data["regulation"]

            user = StudentModel.objects.filter(username=regModel.username).first()

            if user is not None:
                return render(request, 'studentregistration.html', {"message": "User All Ready Exist"})
            else:
                try:
                    regModel.save()
                    return render(request, 'studentregistration.html', {"message": "Student Added Successfully"})
                except:
                    return render(request, 'studentregistration.html', {"message": "Registration Failed"})
        else:
            return render(request, 'studentregistration.html', {"message": "Invalid Form"})

    return render(request, 'studentregistration.html', {"message": "Invalid Request"})

#===============================================================================================
def deletestudent(request):
    student=request.GET['studentid']
    StudentModel.objects.get(id=student).delete()
    return render(request, 'students.html', {'students': StudentModel.objects.all()})

def deletefaculty(request):
    faculty=request.GET['facultyid']
    FacultyModel.objects.get(id=faculty).delete()
    return render(request, 'facultys.html', {'facultys': FacultyModel.objects.all()})

#===============================================================================================
def getfacultys(request):
    return render(request, "facultys.html", {"facultys":FacultyModel.objects.all()})

def getstudents(request):
    return render(request, "students.html", {"students":StudentModel.objects.all()})

#===============================================================================================
def login(request):

    uname = request.GET["username"]
    upass = request.GET["password"]
    type = request.GET["type"]

    if type in "admin":
        if uname == "admin" and upass == "admin":
            request.session['username'] = "admin"
            request.session['role'] = "admin"
            return render(request, "facultys.html", {"facultys":FacultyModel.objects.all()})
        else:
            return render(request, 'index.html', {"message": "Invalid Credentials"})

    if type in "student":
        student = StudentModel.objects.filter(username=uname, password=upass, status="yes").first()

        if student is not None:
            request.session['username'] = uname
            request.session['role'] = "student"
            return render(request, 'viewattendance.html')
        else:
            return render(request, "index.html", {"message": "Invalid Username and Password"})

    if type in "faculty":
        faculty = FacultyModel.objects.filter(username=uname, password=upass).first()
        if faculty is not None:
            request.session['username'] = uname
            request.session['role'] = "faculty"
            return render(request, 'addattendance.html')
        else:
            return render(request, 'index.html', {"message": "Invalid Username and Password"})

def activateAccount(request):

    username = request.GET['username']
    status=request.GET['status']

    StudentModel.objects.filter(username=username).update(status=status)
    return render(request, "students.html", {"students": StudentModel.objects.all()})

def logout(request):
    try:
        del request.session['username']
    except:
        pass
    return render(request, 'index.html', {})


def addattendance(request):

    department=request.GET["department"]
    year=request.GET["year"]
    sem=request.GET["sem"]
    section=request.GET["section"]
    regulation=request.GET["regulation"]
    subject = request.GET["subject"]

    request.session['department'] =department
    request.session['year'] =year
    request.session['sem'] = sem
    request.session['section'] = section
    request.session['regulation'] = regulation
    request.session['subject'] = subject

    return render(request, "addattendance.html", {"students": StudentModel.objects.filter(department=department,year=year,section=section,regulation=regulation,status='yes')})

def submitattendanceaction(request):

    list=request.GET.getlist('username')

    department = request.session['department']
    year = request.session['year']
    section = request.session['section']
    regulation = request.session["regulation"]
    sem = request.session['sem']
    subject = request.session['subject']

    print(department,year,section,regulation,sem,subject)

    for student in StudentModel.objects.filter(department=department,year=year,section=section,regulation=regulation,status='yes'):

        print("in for ",student.username,list)

        attendance = AttendanceModel()
        attendance.username = student.username
        attendance.date = datetime.datetime.now()
        attendance.department = department
        attendance.year = year
        attendance.semester = sem
        attendance.section = section
        attendance.subject = subject

        if student.username in list:
            attendance.isattended="yes"
        else:
            attendance.isattended = "no"
            #send_email(student.email,"Your Child is Not Attended to day Class")

        attendance.save()

    return render(request, "addattendance.html", {"message": 'Attendance Submitted Successfully'})

def viewattendanceaction(request):

    if request.session['role']=="faculty":

        department = request.GET["department"]
        year = request.GET["year"]
        sem = request.GET["sem"]
        section = request.GET["section"]
        regulation = request.GET["regulation"]

        percentagedict = dict()

        for student in StudentModel.objects.filter(department=department, year=year, section=section,
                                                   regulation=regulation):

            attendancedict = dict()

            count = AttendanceModel.objects.filter(department=department, year=year, section=section, semester=sem,
                                                   username=student.username).count()

            if count > 0:

                for attendance in AttendanceModel.objects.filter(department=department, year=year, section=section, semester=sem,
                                                                 username=student.username):

                    if attendance.isattended == "yes":
                        if attendance.username in attendancedict:
                            attendancedict[attendance.username] = attendancedict[attendance.username] + 1
                        else:
                            attendancedict[attendance.username] = 1
                    else:
                        if attendance.username in attendancedict:
                            attendancedict[attendance.username] = attendancedict[attendance.username]
                        else:
                            attendancedict[attendance.username] = 0

                for key, val in attendancedict.items():
                    print("Prasad", key, val, count)
                    percentagedict.update({key: (val / count) * 100})

        for key, val in percentagedict.items():
            print(key, val)

    elif request.session['role'] == "student":

        student=StudentModel.objects.filter(username=request.session['username']).first()

        department = student.department
        year = request.GET["year"]
        sem = request.GET["sem"]
        section = student.section

        percentagedict = dict()
        attendancedict = dict()

        count = AttendanceModel.objects.filter(department=department, year=year, section=section, semester=sem,
                                               username=student.username).count()
        if count > 0:

            for attendance in AttendanceModel.objects.filter(department=department, year=year, section=section, semester=sem,
                                                             username=student.username):

                if attendance.isattended == "yes":
                    if attendance.username in attendancedict:
                        attendancedict[attendance.username] = attendancedict[attendance.username] + 1
                    else:
                        attendancedict[attendance.username] = 1
                else:
                    if attendance.username in attendancedict:
                        attendancedict[attendance.username] = attendancedict[attendance.username]
                    else:
                        attendancedict[attendance.username] = 0

            for key, val in attendancedict.items():
                percentagedict.update({key: (val / count) * 100})

    return render(request, "viewattendance.html", {"percentage":percentagedict})

#=================================================================================================

def handle_uploaded_file(f):
    with open(PROJECT_PATH+"/uploads/"+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def savemarks(filename):

    with open(PROJECT_PATH+"\\uploads\\"+filename,mode="r") as f:

        reader=csv.reader(f)

        for line in reader:

            marks = MarksModel()

            marks.halticket_number = line[0]
            marks.Subject_Code = line[1]
            marks.Subject_Name = line[2]
            marks.Internal_Marks = line[3]
            marks.ExterNal_Marks = line[4]
            marks.Total = line[5]
            marks.Credits = line[6]
            marks.year_sem = line[7]
            marks.actualmarks = line[8]

            marks.save()

def addmarks(request):

    marksForm = MarksForm(request.POST, request.FILES)

    if marksForm.is_valid():
        print("in if")
        file = marksForm.cleaned_data['file']
        handle_uploaded_file(file)
        savemarks(file.name)
    else:
        print("in else")

    return render(request, "addmarks.html", {"message":"uploaded successfully"})

def viewpercentage(request):

    print("in fun")
    if request.session['role']=="faculty":

        print("in faculty")

        department = request.GET["department"]
        year = request.GET["year"]
        section = request.GET["section"]
        regulation = request.GET["regulation"]

        percentagedict = dict()

        print(department,year,section,regulation)

        for student in StudentModel.objects.filter(department=department, year=year, section=section,
                                                   regulation=regulation):
            total_marks=0
            actual_marks=0

            print("in for")

            for marks in MarksModel.objects.filter(halticket_number=student.username):

                print("in marks")

                total_marks = total_marks + int(marks.Total)
                actual_marks = actual_marks + int(marks.actualmarks)

            percentagedict.update({student.username:(total_marks/actual_marks)*100})

        return render(request, "viewpercentage.html", {"percentage": percentagedict})
    else:
        print("in not faculty")

def viewstudentpercentage(request):
    return render(request, "viewstudentwisepercentage.html")

def viewstudentpercentageaction(request):

    print("in fun")

    if request.session['role']=="faculty":

        print("in faculty")
        username = request.GET["username"]

        percentagedict = dict()

        total_marks = 0
        actual_marks = 0

        for marks in MarksModel.objects.filter(halticket_number=username):
            total_marks = total_marks + int(marks.Total)
            actual_marks = actual_marks + int(marks.actualmarks)

        print()
        if actual_marks!=0:
            percentagedict.update({username: (total_marks / actual_marks) * 100})

        return render(request, "viewstudentwisepercentage.html", {"percentage": percentagedict})

    elif request.session['role']=="student":

        print("in else")

        username = request.session["username"]

        percentagedict = dict()

        total_marks = 0
        actual_marks = 0

        for marks in MarksModel.objects.filter(halticket_number=username):
            total_marks = total_marks + int(marks.Total)
            actual_marks = actual_marks + int(marks.actualmarks)

        if actual_marks != 0:
            percentagedict.update({username: (total_marks / actual_marks) * 100})

        return render(request, "viewstudentpercentage.html", {"percentage": percentagedict})

#===============================================================================================

def addinternship(request):

    InternshipModel(halticket_number=request.GET['username'],Company_Name=request.GET['company']).save()
    return render(request, "addinternship.html", {"message":"Added Successfully"})

def viewstudentinternship(request):
    return render(request, "viewinternship.html")

def viewstudentinternshipaction(request):

    print("in fun")
    if request.session['role']=="faculty":
        print("in if")
        username = request.GET["username"]
        print(username)
        for internship in InternshipModel.objects.filter(halticket_number=username):
            print(internship.halticket_number)
            print(internship.Company_Name)
        return render(request, "viewstudentwiseinternship.html", {"internships": InternshipModel.objects.filter(halticket_number=username)})

    elif request.session['role']=="student":

        username = request.session["username"]

        return render(request, "viewstudentwiseinternship.html", {"internships": InternshipModel.objects.filter(halticket_number=username)})


def get_bot_response(request):

    try:
        userText = request.GET['msg']
        print("in bot response", userText)

        if request.session['role'] in "faculty" or request.session['role'] in "admin":

            print("in bot response faculty ")

            if "marks" in userText:

                tokens = userText.split(" ")
                rno = tokens[1]
                sem = tokens[2]

                return render(request, "chat.html", {"academic_marks": getstudentsemmarks(rno, sem), "type": "marks"})

            elif "sempercentage" in userText:

                tokens = userText.split(" ")
                rno = tokens[1]
                sem = tokens[2]

                return render(request, "chat.html",
                              {"percentage": getstudentsempercentage(rno, sem), "type": "percentage"})

            elif "overallpercentage" in userText:

                tokens = userText.split(" ")
                rno = tokens[1]

                return render(request, "chat.html", {"percentage": getstudentpercentage(rno), "type": "percentage"})

            elif "internships" in userText:

                tokens = userText.split(" ")
                rno = tokens[1]

                return render(request, "chat.html", {"internships": getstudentinternships(rno), "type": "internship"})

            elif "attendance" in userText:

                tokens = userText.split(" ")
                rno = tokens[1]
                sem = tokens[2]

                return render(request, "chat.html",
                              {"percentage": getstudentsemattendance(rno, sem), "type": "percentage"})

            elif "hello" in userText:
                return render(request, "chat.html", {"message": "Hi How are You?"})

            else:
                return render(request, "chat.html", {"message": "sorry i didn't understand please try again"})
        elif request.session['role'] in 'student':

            print("in bot response student ")
            if "marks" in userText:

                tokens = userText.split(" ")
                sem = tokens[1]

                return render(request, "chat.html",
                              {"academic_marks": getstudentsemmarks(request.session['username'], sem), "type": "marks"})

            elif "sempercentage" in userText:

                tokens = userText.split(" ")
                sem = tokens[1]

                return render(request, "chat.html",
                              {"percentage": getstudentsempercentage(request.session['username'], sem),
                               "type": "percentage"})

            elif "overallpercentage" in userText:
                print("in student overal", getstudentpercentage(request.session['username']))
                return render(request, "chat.html",
                              {"percentage": getstudentpercentage(request.session['username']), "type": "percentage"})

            elif "internships" in userText:
                return render(request, "chat.html",
                              {"internships": getstudentinternships(request.session['username']), "type": "internship"})

            elif "attendance" in userText:

                tokens = userText.split(" ")
                sem = tokens[1]
                print("final", getstudentsemattendance(request.session['username'], sem))
                return render(request, "chat.html",
                              {"percentage": getstudentsemattendance(request.session['username'], sem),
                               "type": "percentage"})

            elif "hello" in userText:
                return render(request, "chat.html", {"message": "Hi How are You?"})

            else:
                return render(request, "chat.html", {"message": "sorry i didn't understand please try again"})
        else:
            return render(request, "chat.html", {"message": "sorry i didn't understand please try again"})
    except:
        return render(request, "chat.html", {"message": "sorry i didn't understand please try again"})
