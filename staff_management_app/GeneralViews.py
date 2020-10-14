import datetime

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from staff_management_app.models import Gstaff, Departments, Projects, CustomUser, Contribution, ContributionReport, \
    LeaveReportGstaff, FeedBackGstaff, NotificationGstaff


def gstaff_home(request):
    gstaff_obj=Gstaff.objects.get(admin=request.user.id)
    contribution_total=ContributionReport.objects.filter(gstaff_id=gstaff_obj).count()
    contribution_present=ContributionReport.objects.filter(gstaff_id=gstaff_obj,status=True).count()
    contribution_absent=LeaveReportGstaff.objects.filter(gstaff_id=gstaff_obj,leave_status=1).count()

    department=Departments.objects.get(id=gstaff_obj.department_id.id, isTrue=True)
    projects=Projects.objects.filter(department_id=department, isTrue=True).count()
    project1=Projects.objects.filter(department_id=department, isTrue=True)

    project_name=[]
    data_present=[]
    data_absent=[]
    project_data=Projects.objects.filter(department_id=gstaff_obj.department_id, isTrue=True)
    for project in project_data:
        contribution=Contribution.objects.filter(project_id=project.id)
        contribution_present_count=ContributionReport.objects.filter(contribution_id__in=contribution,status=True,gstaff_id=gstaff_obj.id).count()
        contribution_absent_count=ContributionReport.objects.filter(contribution_id__in=contribution,status=False,gstaff_id=gstaff_obj.id).count()
        project_name.append(project.project_name)
        data_present.append(contribution_present_count)
        data_absent.append(contribution_absent_count)

    return render(request,"general_template/gstaff_home_template.html",{"total_contribution":contribution_total,"contribution_absent":contribution_absent,"contribution_present":contribution_present,"projects":projects,"data_name":project_name,"data1":data_present,"data2":data_absent, "project_name":project1,})

def gstaff_view_contribution(request):
    gstaff=Gstaff.objects.get(admin=request.user.id)
    department=gstaff.department_id
    projects=Projects.objects.filter(department_id=department, isTrue=True)
    return render(request,"general_template/gstaff_view_contribution.html",{"projects":projects})

def gstaff_view_contribution_post(request):
    project_id=request.POST.get("project")
    start_date=request.POST.get("start_date")
    end_date=request.POST.get("end_date")

    start_data_parse=datetime.datetime.strptime(start_date,"%Y-%m-%d").date()
    end_data_parse=datetime.datetime.strptime(end_date,"%Y-%m-%d").date()
    project_obj=Projects.objects.get(id=project_id)
    user_object=CustomUser.objects.get(id=request.user.id)
    stud_obj=Gstaff.objects.get(admin=user_object)

    contribution=Contribution.objects.filter(contribution_date__range=(start_data_parse,end_data_parse),project_id=project_obj)
    contribution_reports=ContributionReport.objects.filter(contribution_id__in=contribution,gstaff_id=stud_obj)
    return render(request,"general_template/gstaff_contribution_data.html",{"contribution_reports":contribution_reports})

def general_staff_leave(request):
    gstaff_id = Gstaff.objects.get(admin=request.user.id)
    leave_data=LeaveReportGstaff.objects.filter(gstaff_id=gstaff_id)
    return render(request,"general_template/gstaff_apply_leave.html",{"leave_data":leave_data})

def gstaff_apply_leave_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("gstaff_apply_leave"))
    else:
        leave_date=request.POST.get("leave_date")
        leave_msg=request.POST.get("leave_msg")

        gstaff_obj=Gstaff.objects.get(admin=request.user.id)
        try:
            leave_report=LeaveReportGstaff(gstaff_id=gstaff_obj,leave_date=leave_date,leave_message=leave_msg,leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("gstaff_apply_leave"))
        except:
            messages.error(request, "Failed To Apply for Leave")
            return HttpResponseRedirect(reverse("gstaff_apply_leave"))


def gstaff_feedback(request):
    staff_id=Gstaff.objects.get(admin=request.user.id)
    feedback_data=FeedBackGstaff.objects.filter(gstaff_id=staff_id)
    return render(request,"general_template/gstaff_feedback.html",{"feedback_data":feedback_data})

def gstaff_feedback_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("gstaff_feedback"))
    else:
        feedback_msg=request.POST.get("feedback_msg")

        gstaff_obj=Gstaff.objects.get(admin=request.user.id)
        try:
            feedback=FeedBackGstaff(gstaff_id=gstaff_obj,feedback=feedback_msg,feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("gstaff_feedback"))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse("gstaff_feedback"))

def gstaff_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    gstaff=Gstaff.objects.get(admin=user)
    return render(request,"general_template/gstaff_profile.html",{"user":user,"gstaff":gstaff})

def gstaff_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("gstaff_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        address=request.POST.get("address")
        username = request.POST.get("username")
        email = request.POST.get("email")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            customuser.email = email
            customuser.username = username
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()

            gstaff=Gstaff.objects.get(admin=customuser)
            gstaff.address=address
            gstaff.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("gstaff_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("gstaff_profile"))

@csrf_exempt
def gstaff_fcmtoken_save(request):
    token=request.POST.get("token")
    try:
        gstaff=Gstaff.objects.get(admin=request.user.id)
        gstaff.fcm_token=token
        gstaff.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def gstaff_all_notification(request):
    gstaff=Gstaff.objects.get(admin=request.user.id)
    notifications=NotificationGstaff.objects.filter(gstaff_id=gstaff.id)
    return render(request,"general_template/all_notification.html",{"notifications":notifications})