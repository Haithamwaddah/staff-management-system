"""Staff_Management_System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from staff_management_app import views, HodViews, StaffViews, GeneralViews
from Staff_Management_System import settings

urlpatterns = [
    path('demo',views.showDemoPage),
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls')),
    path('show_login',views.ShowLoginPage,name="show_login"),
    path('',views.ShowStartPage,name="start_page"),
    path('get_user_details', views.GetUserDetails),
    path('logout_user', views.logout_user,name="logout"),
    path('doLogin',views.doLogin,name="do_login"),
    path('admin_home',HodViews.admin_home,name="admin_home"),
    path('add_management_staff',HodViews.add_staff,name="add_staff"),
    path('add_staff_save',HodViews.add_staff_save,name="add_staff_save"),
    path('add_department', HodViews.add_department,name="add_department"),
    path('add_department_save', HodViews.add_department_save,name="add_department_save"),
    path('add_general_staff', HodViews.add_gstaff,name="add_gstaff"),
    path('add_gstaff_save', HodViews.add_gstaff_save,name="add_gstaff_save"),
    path('add_project', HodViews.add_project,name="add_project"),
    path('add_project_save', HodViews.add_project_save,name="add_project_save"),
    path('manage_management_staff', HodViews.manage_staff,name="manage_staff"),
    path('manage_general_staff', HodViews.manage_gstaff,name="manage_gstaff"),
    path('manage_department', HodViews.manage_department,name="manage_department"),
    path('manage_project', HodViews.manage_project,name="manage_project"),
    path('edit_management_staff/<str:staff_id>', HodViews.edit_staff,name="edit_staff"),
    path('edit_staff_save', HodViews.edit_staff_save,name="edit_staff_save"),
    path('edit_general_staff/<str:gstaff_id>', HodViews.edit_gstaff,name="edit_gstaff"),
    path('edit_gstaff_save', HodViews.edit_gstaff_save,name="edit_gstaff_save"),
    path('edit_project/<str:project_id>', HodViews.edit_project,name="edit_project"),
    path('edit_project_save', HodViews.edit_project_save,name="edit_project_save"),
    path('edit_department/<str:department_id>', HodViews.edit_department,name="edit_department"),
    path('edit_department_save', HodViews.edit_department_save,name="edit_department_save"),
    path('manage_working_year', HodViews.manage_working,name="manage_working"),
    path('add_working_save', HodViews.add_working_save,name="add_working_save"),
    path('check_email_exist', HodViews.check_email_exist,name="check_email_exist"),
    path('check_username_exist', HodViews.check_username_exist,name="check_username_exist"),
    path('general_staff_feedback_message', HodViews.gstaff_feedback_message, name="gstaff_feedback_message"),
    path('gstaff_feedback_message_replied', HodViews.gstaff_feedback_message_replied,name="gstaff_feedback_message_replied"),
    path('management_staff_feedback_message', HodViews.staff_feedback_message,name="staff_feedback_message"),
    path('staff_feedback_message_replied', HodViews.staff_feedback_message_replied,name="staff_feedback_message_replied"),
    path('general_staff_leave', HodViews.gstaff_leave_view,name="gstaff_leave_view"),
    path('management_staff_leave', HodViews.staff_leave_view,name="staff_leave_view"),
    path('gstaff_approve_leave/<str:leave_id>', HodViews.gstaff_approve_leave,name="gstaff_approve_leave"),
    path('gstaff_disapprove_leave/<str:leave_id>', HodViews.gstaff_disapprove_leave,name="gstaff_disapprove_leave"),
    path('staff_disapprove_leave/<str:leave_id>', HodViews.staff_disapprove_leave,name="staff_disapprove_leave"),
    path('staff_approve_leave/<str:leave_id>', HodViews.staff_approve_leave,name="staff_approve_leave"),
    path('view_contribution', HodViews.admin_view_contribution,name="admin_view_contribution"),
    path('admin_get_contribution_dates', HodViews.admin_get_contribution_dates,name="admin_get_contribution_dates"),
    path('admin_get_contribution_gstaff', HodViews.admin_get_contribution_gstaff,name="admin_get_contribution_gstaff"),
    path('admin_profile', HodViews.admin_profile,name="admin_profile"),
    path('admin_profile_save', HodViews.admin_profile_save,name="admin_profile_save"),
    path('send_notification_management_staff', HodViews.admin_send_notification_staff,name="admin_send_notification_staff"),
    path('send_notification_general_staff', HodViews.admin_send_notification_gstaff,name="admin_send_notification_gstaff"),
    path('send_gstaff_notification', HodViews.send_gstaff_notification,name="send_gstaff_notification"),
    path('send_staff_notification', HodViews.send_staff_notification,name="send_staff_notification"),
    path('delete_manager/<str:staff_id>', HodViews.delete_staff,name="delete_manager"),
    path('delete_general_staff/<str:staff_id>', HodViews.delete_general_staff,name="delete_general_staff"),
    path('delete_department/<str:dep_id>', HodViews.delete_department,name="delete_department"),
    path('delete_project/<str:project_id>', HodViews.delete_project,name="delete_project"),

                  #     Staff URL Path
    path('management_staff_home', StaffViews.staff_home, name="staff_home"),
    path('management_staff_view_contribution', StaffViews.staff_take_contribution, name="staff_take_contribution"),
    path('management_staff_update_contribution', StaffViews.staff_update_contribution, name="staff_update_contribution"),
    path('get_gstaff', StaffViews.get_gstaff, name="get_gstaff"),
    path('get_contribution_dates', StaffViews.get_contribution_dates, name="get_contribution_dates"),
    path('get_contribution_gstaff', StaffViews.get_contribution_gstaff, name="get_contribution_gstaff"),
    path('save_contribution_data', StaffViews.save_contribution_data, name="save_contribution_data"),
    path('save_updatecontribution_data', StaffViews.save_updatecontribution_data, name="save_updatecontribution_data"),
    path('management_staff_apply_leave', StaffViews.staff_apply_leave, name="staff_apply_leave"),
    path('staff_apply_leave_save', StaffViews.staff_apply_leave_save, name="staff_apply_leave_save"),
    path('management_staff_feedback', StaffViews.staff_feedback, name="staff_feedback"),
    path('staff_feedback_save', StaffViews.staff_feedback_save, name="staff_feedback_save"),
    path('management_staff_profile', StaffViews.staff_profile, name="staff_profile"),
    path('staff_profile_save', StaffViews.staff_profile_save, name="staff_profile_save"),
    path('staff_fcmtoken_save', StaffViews.staff_fcmtoken_save, name="staff_fcmtoken_save"),
    path('management_staff_notification', StaffViews.staff_all_notification, name="staff_all_notification"),

#     general Staff URL Path
    path('general_staff_home', GeneralViews.gstaff_home, name="gstaff_home"),
    path('general_staff_view_contribution', GeneralViews.gstaff_view_contribution, name="gstaff_view_contribution"),
    path('staff_view_contribution_post', GeneralViews.gstaff_view_contribution_post, name="gstaff_view_contribution_post"),
    path('apply_leave', GeneralViews.general_staff_leave, name="gstaff_apply_leave"),
    path('gstaff_apply_leave_save', GeneralViews.gstaff_apply_leave_save, name="gstaff_apply_leave_save"),
    path('general_staff_feedback', GeneralViews.gstaff_feedback, name="gstaff_feedback"),
    path('gstaff_feedback_save', GeneralViews.gstaff_feedback_save, name="gstaff_feedback_save"),
    path('general_staff_profile', GeneralViews.gstaff_profile, name="gstaff_profile"),
    path('gstaff_profile_save', GeneralViews.gstaff_profile_save, name="gstaff_profile_save"),
    path('gstaff_fcmtoken_save', GeneralViews.gstaff_fcmtoken_save, name="gstaff_fcmtoken_save"),
    path('firebase-messaging-sw.js',views.showFirebaseJS,name="show_firebase_js"),
    path('general_staff_notification',GeneralViews.gstaff_all_notification,name="gstaff_all_notification"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)