from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import WorkingYearModel, CustomUser, AdminHOD, Departments, Staffs, Projects, Gstaff, LeaveReportGstaff, \
    LeaveReportStaff, FeedBackGstaff, FeedBackStaffs, NotificationGstaff, NotificationStaffs


# Register your models here.
class UserModel(UserAdmin):
    pass

