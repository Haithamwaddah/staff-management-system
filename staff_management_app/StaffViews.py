import json

from django.contrib import messages
from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from staff_management_app.models import Projects, WorkingYearModel, Gstaff, Contribution, ContributionReport, \
    LeaveReportStaff, Staffs, FeedBackStaffs, CustomUser, Departments, NotificationStaffs, LeaveReportGstaff


def staff_home(request):
    # For Fetch All General staff Under Staff
    projects = Projects.objects.filter(staff_id=request.user.id, isTrue=True)
    department_id_list = []
    for project in projects:
        department = Departments.objects.get(id=project.department_id.id, isTrue=True)
        department_id_list.append(department.id)

    final_department = []
    # removing Duplicate department ID
    for department_id in department_id_list:
        if department_id not in final_department:
            final_department.append(department_id)

    gstaffs_count = Gstaff.objects.filter(department_id__in=final_department, isTrue=True).count()


    # Fetch All general staff leave
    gstaffs = Gstaff.objects.filter(department_id__in=final_department, isTrue=True)
    general_leave_count = 0
    for gstaff in gstaffs:
        temp = LeaveReportGstaff.objects.filter(leave_status=1, gstaff_id=gstaff.id).count()
        general_leave_count = general_leave_count + temp

    # Fetch All Approve Leave
    staff = Staffs.objects.get(admin=request.user.id)
    leave_count = LeaveReportStaff.objects.filter(staff_id=staff.id, leave_status=1).count()
    project_count = projects.count()

    # Fetch Contribution Data by Project
    project_list = []
    contribution_list = []
    for project in projects:
        contribute_id = Contribution.objects.filter(project_id=project.id)
        contribution_count1 = ContributionReport.objects.filter(contribution_id__in=contribute_id, status=True, gstaff_id__in=gstaffs).count()
        project_list.append(project.project_name)
        contribution_list.append(contribution_count1)

    gstaff_contribution = Gstaff.objects.filter(department_id__in=final_department, isTrue=True)
    gstaff_list = []
    gstaff_list_contribution_present = []
    gstaff_list_contribution_absent = []
    for gstaff in gstaff_contribution:
        contribution_present_count = ContributionReport.objects.filter(status=True, gstaff_id=gstaff.id).count()
        leaves = LeaveReportGstaff.objects.filter(gstaff_id=gstaff.id, leave_status=1).count()
        gstaff_list.append(gstaff.admin.username)
        gstaff_list_contribution_present.append(contribution_present_count)
        gstaff_list_contribution_absent.append(leaves)

    project2 = Projects.objects.filter(department_id=department, isTrue=True)

    # Fetch All contribution Count
    contribute_count = 0
    contribution_count = 0
    for gstaff in gstaff_contribution:
        contribution_count = contribute_count + ContributionReport.objects.filter(status=True, gstaff_id=gstaff.id).count()

    return render(request, "staff_template/staff_home_template.html",
                  {"gstaffs_count": gstaffs_count, "contribution_count": contribution_count, "leave_count": leave_count,
                   "general_leave_count": general_leave_count, "project_count": project_count,
                   "project_list": project_list, "contribution_list": contribution_list, "gstaffs_list": gstaff_list,
                   "present_list": gstaff_list_contribution_present, "absent_list": gstaff_list_contribution_absent,
                   "project_name": project2})


def staff_take_contribution(request):
    projects = Projects.objects.filter(staff_id=request.user.id, isTrue=True)
    working_years = WorkingYearModel.object.all()
    return render(request, "staff_template/staff_take_contribution.html",
                  {"projects": projects, "working_years": working_years})


@csrf_exempt
def get_gstaff(request):
    project_id = request.POST.get("project")
    working_year = request.POST.get("working_year")

    project = Projects.objects.get(id=project_id, isTrue=True)
    working_model = WorkingYearModel.object.get(id=working_year)
    gstaffs = Gstaff.objects.filter(department_id=project.department_id, working_year_id=working_model, isTrue=True)
    list_data = []

    for gstaff in gstaffs:
        data_small = {"id": gstaff.admin.id, "name": gstaff.admin.first_name + " " + gstaff.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def save_contribution_data(request):
    gstaff_ids = request.POST.get("gstaff_ids")
    project_id = request.POST.get("project_id")
    contribution_date = request.POST.get("contribution_date")
    working_year_id = request.POST.get("working_year_id")

    project_model = Projects.objects.get(id=project_id)
    working_model = WorkingYearModel.object.get(id=working_year_id)
    json_sgstaff = json.loads(gstaff_ids)
    # print(data[0]['id'])

    try:
        contribution = Contribution(project_id=project_model, contribution_date=contribution_date,
                                working_year_id=working_model)
        contribution.save()

        for gstaffs in json_sgstaff:
            gstaff = Gstaff.objects.get(admin=gstaffs['id'])
            contribution_report = ContributionReport(gstaff_id=gstaff, contribution_id=contribution, status=gstaffs['status'])
            contribution_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")


def staff_update_contribution(request):
    projects = Projects.objects.filter(staff_id=request.user.id)
    working_year_id = WorkingYearModel.object.all()
    return render(request, "staff_template/staff_update_contribution.html",
                  {"projects": projects, "working_year_id": working_year_id})


@csrf_exempt
def get_contribution_dates(request):
    project = request.POST.get("project")
    working_year_id = request.POST.get("working_year_id")
    project_obj = Projects.objects.get(id=project)
    working_year_obj = WorkingYearModel.object.get(id=working_year_id)
    contribution = Contribution.objects.filter(project_id=project_obj, working_year_id=working_year_obj)
    contribution_obj = []
    for contribution_single in contribution:
        data = {"id": contribution_single.id, "contribution_date": str(contribution_single.contribution_date),
                "working_year_id": contribution_single.working_year_id.id}
        contribution_obj.append(data)

    return JsonResponse(json.dumps(contribution_obj), safe=False)


@csrf_exempt
def get_contribution_gstaff(request):
    contribution_date = request.POST.get("contribution_date")
    contribution = Contribution.objects.get(id=contribution_date)

    contribution_data = ContributionReport.objects.filter(contribution_id=contribution)
    list_data = []

    for gstaff in contribution_data:
        data_small = {"id": gstaff.gstaff_id.admin.id,
                      "name": gstaff.gstaff_id.admin.first_name + " " + gstaff.gstaff_id.admin.last_name,
                      "status": gstaff.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def save_updatecontribution_data(request):
    gstaff_ids = request.POST.get("gstaff_ids")
    contribution_date = request.POST.get("contribution_date")
    contribution = Contribution.objects.get(id=contribution_date)

    json_sgstaff = json.loads(gstaff_ids)

    try:
        for gstaff in json_sgstaff:
            gstaff = Gstaff.objects.get(admin=gstaff['id'])
            contribution_report = ContributionReport.objects.get(gstaff_id=gstaff, contribution_id=contribution)
            contribution_report.status = gstaff['status']
            contribution_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")


def staff_apply_leave(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    leave_data = LeaveReportStaff.objects.filter(staff_id=staff_obj)
    return render(request, "staff_template/staff_apply_leave.html", {"leave_data": leave_data})


def staff_apply_leave_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_apply_leave"))
    else:
        leave_date = request.POST.get("leave_date")
        leave_msg = request.POST.get("leave_msg")

        staff_obj = Staffs.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStaff(staff_id=staff_obj, leave_date=leave_date, leave_message=leave_msg,
                                            leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("staff_apply_leave"))
        except:
            messages.error(request, "Failed To Apply for Leave")
            return HttpResponseRedirect(reverse("staff_apply_leave"))


def staff_feedback(request):
    staff_id = Staffs.objects.get(admin=request.user.id)
    feedback_data = FeedBackStaffs.objects.filter(staff_id=staff_id)
    return render(request, "staff_template/staff_feedback.html", {"feedback_data": feedback_data})


def staff_feedback_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_feedback_save"))
    else:
        feedback_msg = request.POST.get("feedback_msg")

        staff_obj = Staffs.objects.get(admin=request.user.id)
        try:
            feedback = FeedBackStaffs(staff_id=staff_obj, feedback=feedback_msg, feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))


def staff_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    staff = Staffs.objects.get(admin=user)
    return render(request, "staff_template/staff_profile.html", {"user": user, "staff": staff})


def staff_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_profile"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        password = request.POST.get("password")
        username = request.POST.get("username")
        email = request.POST.get("email")
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            customuser.email = email
            customuser.username = username
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            staff = Staffs.objects.get(admin=customuser.id)
            staff.address = address
            staff.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("staff_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("staff_profile"))


@csrf_exempt
def staff_fcmtoken_save(request):
    token = request.POST.get("token")
    try:
        staff = Staffs.objects.get(admin=request.user.id)
        staff.fcm_token = token
        staff.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


def staff_all_notification(request):
    staff = Staffs.objects.get(admin=request.user.id)
    notifications = NotificationStaffs.objects.filter(staff_id=staff.id)
    return render(request, "staff_template/all_notification.html", {"notifications": notifications})
