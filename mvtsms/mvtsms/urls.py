"""mvtsms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from mvtapp import views, adminviews, staffviews, studentviews, accountantviews, parentviews


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.showlogin, name="loginpage"),
    path('dologin', views.dologin, name="dologin"),
    path('getuserdetails', views.getuserdetails, name="getuserdetails"),
    path('logoutuser', views.logoutuser, name="logoutuser"),
    path('dash/', views.showdash, name="dashboard"),
    path('home', adminviews.home, name="admin_home"),
    path('add_staff', adminviews.addstaff, name="addstaff"),
    path('savestaff', adminviews.savestaff, name="savestaff"),
    path('manage_staff', adminviews.managestaff, name="managestaff"),
    path('add_student', adminviews.addstudent, name="addstudent"),
    path('savestudent', adminviews.savestudent, name="savestudent"),
    path('manage_student', adminviews.managestudent, name="managestudent"),
    path('add_classes', adminviews.addclasses, name="addclasses"),
    path('saveclasses', adminviews.saveclasses, name="saveclasses"),
    path('manage_classes', adminviews.manageclasses, name="manageclasses"),
    path('add_parent', adminviews.addparent, name="addparent"),
    path('saveparent', adminviews.saveparent, name="saveparent"),
    path('manage_parent', adminviews.manageparent, name="manageparent"),
    path('add_accountant', adminviews.addaccountant, name="addaccountant"),
    path('saveaccountant', adminviews.saveaccountant, name="saveaccountant"),
    path('manage_accountant', adminviews.manageaccountant, name="manageaccountant"),
    path('add_subject', adminviews.addsubject, name="addsubject"),
    path('savesubject', adminviews.savesubject, name="savesubject"),
    path('manage_subject', adminviews.managesubject, name="managesubject"),


    path('edit_staff/<str:staff_id>', adminviews.edit_staff, name="editstaff "),
    path('edit_staff_save', adminviews.edit_staff_save, name="edit_staff_save"),

    path('edit_student/<str:student_id>', adminviews.edit_student, name="editstudent"),
    path('edit_student_save', adminviews.edit_student_save, name="edit_student_save"),

    path('edit_accountant/<str:accountant_id>', adminviews.edit_accountant, name="editaccountant"),
    path('edit_accountant_save', adminviews.edit_accountant_save, name="edit_accountant_save"),

    path('edit_parent/<str:parent_id>', adminviews.edit_parent, name="editparent "),
    path('edit_parent_save', adminviews.edit_parent_save, name="edit_parent_save"),

    path('edit_subject/<str:subject_id>', adminviews.edit_subject, name="editsubject"),
    path('edit_subject_save', adminviews.edit_subject_save, name="edit_subject_save"),

    path('edit_classes/<str:classes_id>', adminviews.edit_classes, name="editclasses"),
    path('delete_classes/<str:classes_id>', adminviews.delete_classes, name="delete_classes"),

    path('edit_classes_save', adminviews.edit_classes_save, name="edit_classes_save"),
    path('edit_classes_delete', adminviews.edit_classes_delete, name="edit_classes_delete"),

    path('attend', adminviews.attend, name="attend"),

    path('manage_session', adminviews.managesession, name="managesession"),
    path('savesession', adminviews.savesession, name="savesession"),

    path('view_leave', adminviews.view_leave, name="view_leave"),
    path('approve_leave/<str:id>', adminviews.approve_leave, name="approve_leave"),
    path('disapprove_leave/<str:id>', adminviews.disapprove_leave, name="disapprove_leave"),
    path('admin_viewresults/<str:term_id>', adminviews.admin_viewresults, name="admin_viewresults"),
    path('admin_broadsheet/<str:term_id>', adminviews.admin_broadsheet, name="admin_broadsheet"),
    path('broadsheet', adminviews.broadsheet, name="broadsheet"),

    path('fetchresults', adminviews.fetchresults, name="fetchresults"),
    path('termdetails', adminviews.termdetails, name="termdetails"),
    path('save_termdetails', adminviews.save_termdetails, name="save_termdetails"),
    path('del_termdetails/<str:term_id>', adminviews.del_termdetails, name="del_termdetails"),
    path('delete_termdetails', adminviews.delete_termdetails, name="delete_termdetails"),
    path('edit_termdetails/<str:term_id>', adminviews.edit_termdetails, name="edit_termdetails"),
    path('edit_termdetails_save', adminviews.edit_termdetails_save, name="edit_termdetails_save"),
    path('delete_session/<str:ses_id>', adminviews.delete_session, name="delete_session"),
    path('delete_a_session', adminviews.delete_a_session, name="delete_a_session"),

    path('calendar', adminviews.calendar, name="calendar"),
    path('admin_inv_print/<str:term_id><str:s_id>', adminviews.admin_inv_print, name="admin_inv_print"),
    path('broadsheet_print/<str:term_id><str:c_id><str:sub_id>', adminviews.broadsheet_print, name="broadsheet_print"),
    path('admin_remarks/<str:term_id>', adminviews.admin_remarks, name="admin_remarks"),
    path('admin_save_remarks', adminviews.admin_save_remarks, name="admin_save_remarks"),
                  # staff url path
    path('staffhome', staffviews.staffhome, name="staffhome"),
    path('takeattendance/<str:term_id>', staffviews.takeattendance, name="takeattendance"),
    path('view_attendance/<str:id>', staffviews.view_attendance, name="view_attendance"),
    path('saveattendance', staffviews.saveattendance, name="saveattendance"),
    path('staffleave', staffviews.staffleave, name="staffleave"),
    path('staffleave_save', staffviews.staffleave_save, name="staffleave_save"),
    path('leavehistory', staffviews.leavehistory, name="leavehistory"),
    path('addresult', staffviews.addresult, name="addresult"),
    path('saveresult_term1', staffviews.saveresult_term1, name="saveresult_term1"),
    path('viewresults', staffviews.viewresults, name="viewresults"),

    path('invoice-print', staffviews.invoice, name="invoice-print"),
    path('traits/<str:term_id>', staffviews.traits, name="traits"),
    path('savetraits', staffviews.savetraits, name="savetraits"),
    path('staff_remarks', staffviews.staff_remarks, name="staff_remarks"),
    path('staff_save_remarks', staffviews.staff_save_remarks, name="staff_save_remarks"),
                  #path('getstudent/', staffviews.get_student, name="getstudent"),


                # student url path
    path('studenthome/', studentviews.studenthome, name="studenthome"),
    path('student_view_results/<str:id>', studentviews.student_view_results, name="student_view_results"),
    path('student_invoice_print/<str:t_id>', studentviews.student_invoice_print, name="student_invoice_print"),
    path('confirm_result_details/<str:term_id>', studentviews.confirm_result_details, name="confirm_result_details"),

                  #parents views....
    path('parenthome/', parentviews.parenthome, name="parenthome"),
    path('email_details/<str:term_id>', parentviews.email_details, name="email_details"),
    path('checkresults', parentviews.checkresults, name="checkresults"),
    path('parents_invoice_print/<str:s_id>/<str:term_id>', parentviews.parents_invoice_print, name="parents_invoice_print"),


    # accountant VIEWS
    path('accountanthome/', accountantviews.accountanthome, name="accountanthome"),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
