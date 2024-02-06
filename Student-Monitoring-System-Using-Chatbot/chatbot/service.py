from chatbot.models import InternshipModel, MarksModel, AttendanceModel


def getstudentsemattendance(username,sem):

    attendancedict = dict()
    percentagedict=dict()

    year, sem = sem.split("_")

    print("service",year,sem,username)

    count = AttendanceModel.objects.filter(year=year,semester=sem,username=username).count()

    if count > 0:

        for attendance in AttendanceModel.objects.filter(semester=sem,username=username):

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

    return percentagedict
# =================================================================================================

def getstudentpercentage(username):

    percentagedict = dict()

    total_marks = 0
    actual_marks = 0

    for marks in MarksModel.objects.filter(halticket_number=username):
        total_marks = total_marks + int(marks.Total)
        actual_marks = actual_marks + int(marks.actualmarks)

    if actual_marks != 0:
        percentagedict.update({username: (total_marks / actual_marks) * 100})

    return percentagedict

def getstudentsempercentage(username,sem):

    percentagedict = dict()

    total_marks = 0
    actual_marks = 0

    for marks in MarksModel.objects.filter(halticket_number=username,year_sem=sem):
        total_marks = total_marks + int(marks.Total)
        actual_marks = actual_marks + int(marks.actualmarks)

    if actual_marks != 0:
        percentagedict.update({username: (total_marks / actual_marks) * 100})

    return percentagedict
# ===============================================================================================

def getstudentinternships(username):
    return InternshipModel.objects.filter(halticket_number=username)

#==================================================================================================

def getstudentsemmarks(username,sem):
    return MarksModel.objects.filter(halticket_number=username,year_sem=sem)