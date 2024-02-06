from django.contrib import admin

# Register your models here.
from chatbot.models import FacultyModel, StudentModel, AttendanceModel, MarksModel, InternshipModel

admin.site.register(FacultyModel)
admin.site.register(StudentModel)
admin.site.register(AttendanceModel)
admin.site.register(MarksModel)
admin.site.register(InternshipModel)