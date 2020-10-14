import json

import requests
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from staff_management_app.forms import AddGstaffForm, EditGstaffForm
from staff_management_app.models import CustomUser, Staffs, Departments, Projects, Gstaff, WorkingYearModel, \
    FeedBackGstaff, FeedBackStaffs, LeaveReportGstaff, LeaveReportStaff, Contribution, ContributionReport, \
    NotificationGstaff, NotificationStaffs


def admin_home(request):
    num = 0
    gstaff_count1 = Gstaff.objects.filter(isTrue=True).count()
    staff_count = Staffs.objects.filter(isTrue=True).count()
    project_count = Projects.objects.filter(isTrue=True).count()
    department_count = Departments.objects.filter(isTrue=True).count()

    department_all = Departments.objects.filter(isTrue=True)
    department_name_list = []
    project_count_list = []
    gstaff_count_list_in_department = []
    for department in department_all:
        projects = Projects.objects.filter(department_id=department.id, isTrue=True).count()
        gstaff = Gstaff.objects.filter(department_id=department.id, isTrue=True).count()
        department_name_list.append(department.department_name)
        project_count_list.append(projects)
        gstaff_count_list_in_department.append(gstaff)

    projects_all = Projects.objects.filter(isTrue=True)
    project_list = []
    gstaff_count_list_in_project = []
    for project in projects_all:
        department = Departments.objects.get(id=project.department_id.id, isTrue=True)
        gstaff_count = Gstaff.objects.filter(department_id=department.id, isTrue=True).count()
        project_list.append(project.project_name)
        gstaff_count_list_in_project.append(gstaff_count)

    staffs = Staffs.objects.filter(isTrue=True)
    contribution_present_list_staff = []
    contribution_absent_list_staff = []
    staff_name_list = []
    for staff in staffs:
        # For Fetch All General staff Under Staff
        projects = Projects.objects.filter(staff_id=staff.admin.id, isTrue=True)
        department_id_list = []
        for project in projects:
            department = Departments.objects.get(id=project.department_id.id, isTrue=True)
            department_id_list.append(department.id)

        final_department = []
        # removing Duplicate department ID
        for department_id in department_id_list:
            if department_id not in final_department:
                final_department.append(department_id)
        gstaffs1 = Gstaff.objects.filter(department_id__in=final_department, isTrue=True)
        project_ids = Projects.objects.filter(staff_id=staff.admin.id, isTrue=True)
        contribute = Contribution.objects.filter(project_id__in=project_ids)
        contribution = ContributionReport.objects.filter(contribution_id__in=contribute, status=True, gstaff_id__in=gstaffs1).count()
        leaves = LeaveReportStaff.objects.filter(staff_id=staff.id, leave_status=1).count()
        contribution_present_list_staff.append(contribution)
        contribution_absent_list_staff.append(leaves)
        staff_name_list.append(staff.admin.username)

    gstaff_all = Gstaff.objects.filter(isTrue=True)
    contribution_present_list_gstaff = []
    contribution_absent_list_gstaff = []
    gstaff_name_list = []
    for gstaff in gstaff_all:
        contribution = ContributionReport.objects.filter(gstaff_id=gstaff.id, status=True).count()
        abs = ContributionReport.objects.filter(gstaff_id=gstaff.id, status=False).count()
        leaves = LeaveReportGstaff.objects.filter(gstaff_id=gstaff.id, leave_status=1).count()
        contribution_present_list_gstaff.append(contribution)
        contribution_absent_list_gstaff.append(leaves)
        gstaff_name_list.append(gstaff.admin.username)

    return render(request, "hod_template/home_content.html",
                  {"gstaff_count": gstaff_count1, "staff_count": staff_count, "project_count": project_count,
                   "department_count": department_count, "department_name_list": department_name_list,
                   "project_count_list": project_count_list,
                   "gstaff_count_list_in_department": gstaff_count_list_in_department,
                   "gstaff_count_list_in_project": gstaff_count_list_in_project, "project_list": project_list,
                   "staff_name_list": staff_name_list, "contribution_present_list_staff": contribution_present_list_staff,
                   "contribution_absent_list_staff": contribution_absent_list_staff, "gstaff_name_list": gstaff_name_list,
                   "contribution_present_list_gstaff": contribution_present_list_gstaff,
                   "contribution_absent_list_gstaff": contribution_absent_list_gstaff, "num" : num})


def add_staff(request):
    departments = Departments.objects.filter(isTrue=True)
    working = WorkingYearModel.object.all()
    return render(request, "hod_template/add_staff_template.html", {"working": working, "departments": departments})


def add_staff_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        department_id = request.POST.get("department")
        year_id = request.POST.get("working")
        # try:
        user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                  last_name=last_name, first_name=first_name, user_type=2)
        user.staffs.address = address
        user.staffs.gender = gender
        department_obj = Departments.objects.get(id=department_id)
        user.staffs.department_id = department_obj
        working_year = WorkingYearModel.object.get(id=1)
        user.staffs.working_year_id = working_year
        user.save()



        messages.success(request, "Successfully Added Mangement Staff")
        return HttpResponseRedirect(reverse("add_staff"))
        # except:
        #     messages.error(request, "Failed to Add Mangement Staff")
        #     return HttpResponseRedirect(reverse("add_staff"))


def add_department(request):
    return render(request, "hod_template/add_department_template.html")


def add_department_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        department = request.POST.get("department")
        try:
            department_model = Departments(department_name=department)
            department_model.save()
            messages.success(request, "Successfully Added Department")
            return HttpResponseRedirect(reverse("add_department"))
        except:
            messages.error(request, "Failed To Add Department")
            return HttpResponseRedirect(reverse("add_department"))


def add_gstaff(request):
    form = AddGstaffForm()
    return render(request, "hod_template/add_gstaff_template.html", {"form": form})


def add_gstaff_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        form = AddGstaffForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            address = form.cleaned_data["address"]
            working_year_id = form.cleaned_data["working_year_id"]
            department_id = form.cleaned_data["department"]
            sex = form.cleaned_data["sex"]

            try:
                user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                          last_name=last_name, first_name=first_name, user_type=3)
                user.gstaff.address = address
                department_obj = Departments.objects.get(id=department_id)
                user.gstaff.department_id = department_obj
                working_year = WorkingYearModel.object.get(id=working_year_id)
                user.gstaff.working_year_id = working_year
                user.gstaff.gender = sex
                user.save()

                messages.success(request, "Successfully Added General Staff")
                return HttpResponseRedirect(reverse("add_gstaff"))
            except:
                messages.error(request, "Failed to Add General Staff")
                return HttpResponseRedirect(reverse("add_gstaff"))
        else:
            form = AddGstaffForm(request.POST)
            return render(request, "hod_template/add_gstaff_template.html", {"form": form})


def add_project(request):
    departments = Departments.objects.filter(isTrue=True)
    staffs = CustomUser.objects.filter(user_type=2, is_active=True)
    return render(request, "hod_template/add_project_template.html", {"staffs": staffs, "departments": departments})


def add_project_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        project_name = request.POST.get("project_name")
        department_id = request.POST.get("department")
        department = Departments.objects.get(id=department_id)
        staff_id = request.POST.get("staff")
        staff = CustomUser.objects.get(id=staff_id)

        try:
            project = Projects(project_name=project_name, department_id=department, staff_id=staff)
            project.save()
            messages.success(request, "Successfully Added Project")
            return HttpResponseRedirect(reverse("add_project"))
        except:
            messages.error(request, "Failed to Add Project")
            return HttpResponseRedirect(reverse("add_project"))


def manage_staff(request):
    staffs = Staffs.objects.filter(isTrue=True)
    return render(request, "hod_template/manage_staff_template.html", {"staffs": staffs})


def manage_gstaff(request):
    gstaff = Gstaff.objects.filter(isTrue=True)
    return render(request, "hod_template/manage_gstaff_template.html", {"gstaffs": gstaff})


def manage_department(request):
    departments = Departments.objects.filter(isTrue=True)
    return render(request, "hod_template/manage_department_template.html", {"departments": departments})


def manage_project(request):
    projects = Projects.objects.filter(isTrue=True)
    return render(request, "hod_template/manage_project_template.html", {"projects": projects})


def edit_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    departments = Departments.objects.filter(isTrue=True)
    working = WorkingYearModel.object.all()
    return render(request, "hod_template/edit_staff_template.html",
                  {"staff": staff, "id": staff_id, "working": working, "departments": departments})


def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id = request.POST.get("staff_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        department_id = request.POST.get("department")
        year_id = request.POST.get("working")

        try:
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username

            user.save()

            staff_model = Staffs.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.gender = gender
            working_year = WorkingYearModel.object.get(id=year_id)
            staff_model.working_year_id = working_year
            dep_obj = Departments.objects.get(id=department_id)
            staff_model.department_id = dep_obj
            staff_model.save()
            messages.success(request, "Successfully Edited Management Staff")
            return HttpResponseRedirect(reverse("edit_staff", kwargs={"staff_id": staff_id}))
        except:
            messages.error(request, "Failed to Edit Staff")
            return HttpResponseRedirect(reverse("edit_staff", kwargs={"staff_id": staff_id}))


def edit_gstaff(request, gstaff_id):
    request.session['gstaff_id'] = gstaff_id
    gstaff = Gstaff.objects.get(admin=gstaff_id)
    form = EditGstaffForm()
    form.fields['email'].initial = gstaff.admin.email
    form.fields['first_name'].initial = gstaff.admin.first_name
    form.fields['last_name'].initial = gstaff.admin.last_name
    form.fields['username'].initial = gstaff.admin.username
    form.fields['address'].initial = gstaff.address
    form.fields['department'].initial = gstaff.department_id.id
    form.fields['sex'].initial = gstaff.gender
    form.fields['working_year_id'].initial = gstaff.working_year_id.id
    return render(request, "hod_template/edit_gstaff_template.html",
                  {"form": form, "id": gstaff_id, "username": gstaff.admin.username})


def edit_gstaff_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        gstaff_id = request.session.get("gstaff_id")
        if gstaff_id == None:
            return HttpResponseRedirect(reverse("manage_gstaff"))

        form = EditGstaffForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]
            working_year_id = form.cleaned_data["working_year_id"]
            department_id = form.cleaned_data["department"]
            sex = form.cleaned_data["sex"]

            if request.FILES.get('profile_pic', False):
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                user = CustomUser.objects.get(id=gstaff_id)
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.save()

                gstaff = Gstaff.objects.get(admin=gstaff_id)
                gstaff.address = address
                working_year = WorkingYearModel.object.get(id=working_year_id)
                gstaff.working_year_id = working_year
                gstaff.gender = sex
                department = Departments.objects.get(id=department_id)
                gstaff.department_id = department
                if profile_pic_url != None:
                    gstaff.profile_pic = profile_pic_url
                gstaff.save()
                del request.session['gstaff_id']
                messages.success(request, "Successfully Edited General Staff")
                return HttpResponseRedirect(reverse("edit_gstaff", kwargs={"gstaff_id": gstaff_id}))
            except:
                messages.error(request, "Failed to Edit General Staff")
                return HttpResponseRedirect(reverse("edit_gstaff", kwargs={"gstaff_id": gstaff_id}))
        else:
            form = EditGstaffForm(request.POST)
            gstaff = Gstaff.objects.get(admin=gstaff_id)
            return render(request, "hod_template/edit_gstaff_template.html",
                          {"form": form, "id": gstaff_id, "username": gstaff.admin.username})


def edit_project(request, project_id):
    project = Projects.objects.get(id=project_id)
    departments = Departments.objects.filter(isTrue=True)
    staffs = CustomUser.objects.filter(user_type=2, is_active=1)
    return render(request, "hod_template/edit_project_template.html",
                  {"project": project, "staffs": staffs, "departments": departments, "id": project_id})


def edit_project_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        project_id = request.POST.get("project_id")
        project_name = request.POST.get("project_name")
        staff_id = request.POST.get("staff")
        department_id = request.POST.get("department")

        try:
            project = Projects.objects.get(id=project_id)
            project.project_name = project_name
            staff = CustomUser.objects.get(id=staff_id)
            project.staff_id = staff
            department = Departments.objects.get(id=department_id)
            project.department_id = department
            project.save()

            messages.success(request, "Successfully Edited Project")
            return HttpResponseRedirect(reverse("edit_project", kwargs={"project_id": project_id}))
        except:
            messages.error(request, "Failed to Edit Project")
            return HttpResponseRedirect(reverse("edit_project", kwargs={"project_id": project_id}))


def edit_department(request, department_id):
    department = Departments.objects.get(id=department_id)
    return render(request, "hod_template/edit_department_template.html", {"department": department, "id": department_id})


def edit_department_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        department_id = request.POST.get("department_id")
        department_name = request.POST.get("department")

        try:
            department = Departments.objects.get(id=department_id)
            department.department_name = department_name
            department.save()
            messages.success(request, "Successfully Edited Department")
            return HttpResponseRedirect(reverse("edit_department", kwargs={"department_id": department_id}))
        except:
            messages.error(request, "Failed to Edit Department")
            return HttpResponseRedirect(reverse("edit_department", kwargs={"department_id": department_id}))


def delete_staff(request, staff_id):
    try:
        user = CustomUser.objects.get(id=staff_id)
        user.is_active = 0
        user.save()

        staff_model = Staffs.objects.get(admin=staff_id)
        staff_model.isTrue = False
        staff_model.save()

        staffs = Staffs.objects.filter(isTrue=True)
        return render(request, "hod_template/manage_staff_template.html", {"staffs": staffs})
    except:

        return render(request, "hod_template/manage_staff_template.html", {"staffs": staffs})


def delete_general_staff(request, staff_id):
    try:
        user = CustomUser.objects.get(id=staff_id)
        user.is_active = 0
        user.save()

        gstaff = Gstaff.objects.get(admin=staff_id)
        gstaff.isTrue = False
        gstaff.save()

        gstaffs = Gstaff.objects.filter(isTrue=True)
        return render(request, "hod_template/manage_gstaff_template.html", {"gstaffs": gstaffs})
    except:

        return render(request, "hod_template/manage_gstaff_template.html", {"gstaffs": gstaffs})


def delete_department(request, dep_id):
    try:
        departments = Departments.objects.get(id=dep_id)
        departments.isTrue = False
        departments.save()

        departments = Departments.objects.filter(isTrue=True)
        return render(request, "hod_template/manage_department_template.html", {"departments": departments})
    except:
        return render(request, "hod_template/manage_department_template.html", {"departments": departments})


def delete_project(request, project_id):
    try:
        project = Projects.objects.get(id=project_id)
        project.isTrue = False
        project.save()

        projects = Projects.objects.filter(isTrue=True)
        return render(request, "hod_template/manage_project_template.html", {"projects": projects})
    except:
        return render(request, "hod_template/manage_project_template.html", {"projects": projects})


def manage_working(request):
    return render(request, "hod_template/manage_working_template.html")


def add_working_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("manage_working"))
    else:
        working_start_year = request.POST.get("working_start")
        working_end_year = request.POST.get("working_end")

        try:
            workingyear = WorkingYearModel(working_start_year=working_start_year, working_end_year=working_end_year)
            workingyear.save()
            messages.success(request, "Successfully Added Working Year")
            return HttpResponseRedirect(reverse("manage_working"))
        except:
            messages.error(request, "Failed to add Working Year")
            return HttpResponseRedirect(reverse("manage_working"))


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def staff_feedback_message(request):
    feedbacks = FeedBackStaffs.objects.all()
    return render(request, "hod_template/staff_feedback_template.html", {"feedbacks": feedbacks})


def gstaff_feedback_message(request):
    feedbacks = FeedBackGstaff.objects.all()
    return render(request, "hod_template/gstaff_feedback_template.html", {"feedbacks": feedbacks})


@csrf_exempt
def gstaff_feedback_message_replied(request):
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")

    try:
        feedback = FeedBackGstaff.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


@csrf_exempt
def staff_feedback_message_replied(request):
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")

    try:
        feedback = FeedBackStaffs.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


def staff_leave_view(request):
    leaves = LeaveReportStaff.objects.all()
    return render(request, "hod_template/staff_leave_view.html", {"leaves": leaves})


def gstaff_leave_view(request):
    leaves = LeaveReportGstaff.objects.all()
    return render(request, "hod_template/gstaff_leave_view.html", {"leaves": leaves})


def gstaff_approve_leave(request, leave_id):
    leave = LeaveReportGstaff.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("gstaff_leave_view"))


def gstaff_disapprove_leave(request, leave_id):
    leave = LeaveReportGstaff.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("gstaff_leave_view"))


def staff_approve_leave(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))


def staff_disapprove_leave(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))


def admin_view_contribution(request):
    projects = Projects.objects.all()
    working_year_id = WorkingYearModel.object.all()
    return render(request, "hod_template/admin_view_contribution.html",
                  {"projects": projects, "working_year_id": working_year_id})


@csrf_exempt
def admin_get_contribution_dates(request):
    project = request.POST.get("project")
    working_year_id = request.POST.get("working_year_id")
    project_obj = Projects.objects.get(id=project)
    working_year_obj = WorkingYearModel.object.get(id=working_year_id)
    contribution = Contribution.objects.filter(department_id=project_obj, working_year_id=working_year_obj)
    contribution_obj = []
    for contribution_single in contribution:
        data = {"id": contribution_single.id, "contribution_date": str(contribution_single.contribution_date),
                "working_year_id": contribution_single.working_year_id.id}
        contribution_obj.append(data)

    return JsonResponse(json.dumps(contribution_obj), safe=False)


@csrf_exempt
def admin_get_contribution_gstaff(request):
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


def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, "hod_template/admin_profile.html", {"user": user})


def admin_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
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
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("admin_profile"))


def admin_send_notification_gstaff(request):
    gstaffs = Gstaff.objects.filter(isTrue=True)
    return render(request, "hod_template/gstaff_notification.html", {"gstaffs": gstaffs})


def admin_send_notification_staff(request):
    staffs = Staffs.objects.filter(isTrue=True)
    return render(request, "hod_template/staff_notification.html", {"staffs": staffs})


@csrf_exempt
def send_gstaff_notification(request):
    id = request.POST.get("id")
    message = request.POST.get("message")
    gstaff = Gstaff.objects.get(admin=id)
    token = gstaff.fcm_token
    url = "https://fcm.googleapis.com/fcm/send"
    body = {
        "notification": {
            "title": "Staff Management System",
            "body": message,
            "click_action": "https://studentmanagementsystem22.herokuapp.com/student_all_notification",
            "icon": "http://studentmanagementsystem22.herokuapp.com/static/dist/img/user2-160x160.jpg"
        },
        "to": token
    }
    headers = {"Content-Type": "application/json", "Authorization": "key=SERVER_KEY_HERE"}
    data = requests.post(url, data=json.dumps(body), headers=headers)
    notification = NotificationGstaff(gstaff_id=gstaff, message=message)
    notification.save()
    print(data.text)
    return HttpResponse("True")


@csrf_exempt
def send_staff_notification(request):
    id = request.POST.get("id")
    message = request.POST.get("message")
    staff = Staffs.objects.get(admin=id)
    token = staff.fcm_token
    url = "https://fcm.googleapis.com/fcm/send"
    body = {
        "notification": {
            "title": "Staff Management System",
            "body": message,
            "click_action": "https://studentmanagementsystem22.herokuapp.com/staff_all_notification",
            "icon": "http://studentmanagementsystem22.herokuapp.com/static/dist/img/user2-160x160.jpg"
        },
        "to": token
    }
    headers = {"Content-Type": "application/json", "Authorization": "key=SERVER_KEY_HERE"}
    data = requests.post(url, data=json.dumps(body), headers=headers)
    notification = NotificationStaffs(staff_id=staff, message=message)
    notification.save()
    print(data.text)
    return HttpResponse("True")
