from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class WorkingYearModel(models.Model):
    id=models.AutoField(primary_key=True)
    working_start_year=models.DateField()
    working_end_year=models.DateField()
    object=models.Manager()

class CustomUser(AbstractUser):
    user_type_data=((1,"HOD"),(2,"Staff"),(3,"Gstaff"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)


class AdminHOD(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Departments(models.Model):
    id=models.AutoField(primary_key=True)
    department_name=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    isTrue = models.BooleanField(default=True)

class Staffs(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address=models.TextField()
    department_id = models.ForeignKey(Departments, on_delete=models.DO_NOTHING, default=1)
    working_year_id = models.ForeignKey(WorkingYearModel, on_delete=models.CASCADE,default=1)
    gender = models.CharField(max_length=255,default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    fcm_token=models.TextField(default="")
    objects=models.Manager()
    isTrue = models.BooleanField(default=True)


class Projects(models.Model):
    id=models.AutoField(primary_key=True)
    project_name=models.CharField(max_length=255)
    department_id=models.ForeignKey(Departments, on_delete=models.CASCADE, default=1)
    staff_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    isTrue = models.BooleanField(default=True)


class Gstaff(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    gender=models.CharField(max_length=255, default="Male")
    profile_pic=models.FileField()
    address=models.TextField()
    department_id=models.ForeignKey(Departments,on_delete=models.DO_NOTHING, default=1)
    working_year_id=models.ForeignKey(WorkingYearModel,on_delete=models.CASCADE, default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    fcm_token=models.TextField(default="")
    objects = models.Manager()
    isTrue=models.BooleanField(default=True)

class Contribution(models.Model):
    id=models.AutoField(primary_key=True)
    project_id=models.ForeignKey(Projects,on_delete=models.DO_NOTHING)
    contribution_date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    working_year_id=models.ForeignKey(WorkingYearModel,on_delete=models.CASCADE)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class ContributionReport(models.Model):
    id=models.AutoField(primary_key=True)
    gstaff_id=models.ForeignKey(Gstaff,on_delete=models.DO_NOTHING)
    contribution_id=models.ForeignKey(Contribution,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class LeaveReportGstaff(models.Model):
    id=models.AutoField(primary_key=True)
    gstaff_id=models.ForeignKey(Gstaff,on_delete=models.CASCADE)
    leave_date=models.CharField(max_length=255)
    leave_message=models.TextField()
    leave_status=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class FeedBackGstaff(models.Model):
    id = models.AutoField(primary_key=True)
    gstaff_id = models.ForeignKey(Gstaff, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class FeedBackStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class NotificationGstaff(models.Model):
    id = models.AutoField(primary_key=True)
    gstaff_id = models.ForeignKey(Gstaff, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class NotificationStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type==2:
            Staffs.objects.create(admin=instance,department_id=Departments.objects.get(id=1), working_year_id=WorkingYearModel.object.get(id=1), address="", gender="")
        if instance.user_type==3:
            Gstaff.objects.create(admin=instance, department_id=Departments.objects.get(id=1), working_year_id=WorkingYearModel.object.get(id=1), address="", profile_pic="", gender="")

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.adminhod.save()
    if instance.user_type==2:
        instance.staffs.save()
    if instance.user_type==3:
        instance.gstaff.save()



