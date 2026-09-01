"""
URL configuration for onlineadmissionsystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from admissionapp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('edit/',views.edit, name='edit'),
    path('add_student/', views.add_student, name='add_student'),
    path('all_student/',views.all_student,name='all_student'),
    path('enquiry/',views.enquiry,name='enquiry'),
    path('all_enquiry/',views.all_enquiry,name='all_enquiry'),
    path('all_enquiry/<int:id>/delete/',views.enquity_delete,name='enquiry_delete'),
    path('student_login/', views.student_login, name='student_login'),
    path('all_student/<int:id>/delete/',views.delete,name='delete'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('add_courses/',views.add_courses,name='add_courses'),
    path('all_courses/',views.all_courses,name='all_courses'),
    path('all_courses/<int:id>/delete/',views.course_delete,name='course_delete'),
    path('courses/',views.courses,name='courses'),
    path('student_logout/', views.student_logout, name='student_logout'),
    path('student_application',views.student_application,name='student_application'),
    path('application/',views.application,name='application'),
    path("all_student/<int:id>/edit/", views.edit_student, name="edit_student"),
    path("all_student/<int:id>/status/",views.update_student_status,name="update_student_status"),

   
    #fees submission
    path("student_fee_submission/",views.student_fee_submission,name="student_fee_submission"),

    #admin fees submission
    path("fees_status/",views.fees_status,name="fees_status"),

    path("verify_payment/<int:id>/",views.verify_payment,name="verify_payment"),
    path("reject_payment/<int:id>/",views.reject_payment,name="reject_payment"),

    #student course
    path("student_course/",views.student_course,name="student_course"),

    #admin course
    path("all_courses/<int:id>/edit/",views.course_edit,name="course_edit"),
    path("all_courses/<int:id>/delete/",views.course_delete,name="course_delete"),

    path(
    "update_profile_photo/",
    views.update_profile_photo,
    name="update_profile_photo"
),
 

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)