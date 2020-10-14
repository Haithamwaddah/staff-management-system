from django import forms
from django.forms import ChoiceField

from staff_management_app.models import Departments, WorkingYearModel, Projects, Gstaff
class ChoiceNoValidation(ChoiceField):
    def validate(self, value):
        pass

class DateInput(forms.DateInput):
    input_type = "date"

class AddGstaffForm(forms.Form):
    email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control","autocomplete":"off"}))
    password=forms.CharField(label="Password",max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username=forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control","autocomplete":"off"}))
    address=forms.CharField(label="Address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    department_list=[]
    working_list = []
    try:
        departments=Departments.objects.filter(isTrue=True)
        for department in departments:
            small_department=(department.id, department.department_name)
            department_list.append(small_department)
    except:
        department_list=[]



    try:
        workings = WorkingYearModel.object.all()

        for work in workings:
            small_work = (work.id, str(work.working_start_year) + "   TO  " + str(work.working_end_year))
            working_list.append(small_work)
    except:
        working_list=[]

    gender_choice=(
        ("Male","Male"),
        ("Female","Female")
    )

    department=forms.ChoiceField(label="Department", choices=department_list, widget=forms.Select(attrs={"class": "form-control"}))
    sex=forms.ChoiceField(label="Sex",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    working_year_id=forms.ChoiceField(label="Working Year", choices=working_list, widget=forms.Select(attrs={"class": "form-control"}))


class EditGstaffForm(forms.Form):
    email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username=forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    address=forms.CharField(label="Address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))


    department_list=[]
    try:
        departments = Departments.objects.filter(isTrue=True)
        for department in departments:
            small_department=(department.id, department.department_name)
            department_list.append(small_department)
    except:
        department_list=[]

    working_list = []
    try:
        workings = WorkingYearModel.object.all()

        for work in workings:
            small_work = (work.id, str(work.working_start_year) + "   TO  " + str(work.working_end_year))
            working_list.append(small_work)
    except:
        pass
        #working_list = []

    gender_choice=(
        ("Male","Male"),
        ("Female","Female")
    )

    department=forms.ChoiceField(label="Department", choices=department_list, widget=forms.Select(attrs={"class": "form-control"}))
    sex=forms.ChoiceField(label="Sex",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    working_year_id=forms.ChoiceField(label="Working Year", choices=working_list, widget=forms.Select(attrs={"class": "form-control"}))
