from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="admin_role"),
    
    path("students/", views.students_list, name="admin_students"),
    path("students/<int:pk>/", views.student_detail, name="admin_student_detail"),
    path("students/<int:pk>/delete/", views.student_delete, name="admin_student_delete"),
    
    path("companies/", views.companies_list, name="admin_companies"),
    path("companies/<int:pk>/", views.company_detail, name="admin_company_detail"),
    path("companies/<int:pk>/delete/", views.company_delete, name="admin_company_delete"),
    
    path("jobs/", views.jobs_list, name="admin_jobs"),
    path("jobs/<int:pk>/", views.job_detail, name="admin_job_detail"),
    path("jobs/<int:pk>/delete/", views.job_delete, name="admin_job_delete"),
    
    path("applications/", views.applications_list, name="admin_applications"),
    path("applications/<int:pk>/delete/", views.application_delete, name="admin_application_delete"),
    
    path("profile/", views.my_profile, name="admin_profile"),
]

