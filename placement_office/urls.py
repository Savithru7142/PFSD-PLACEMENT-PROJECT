from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="placement_office"),
    path("students/", views.students_list, name="officer_students"),
    path("students/<int:pk>/", views.student_detail, name="officer_student_detail"),
    path("companies/", views.companies_list, name="officer_companies"),
    path("applications/", views.applications_list, name="officer_applications"),
    path("profile/", views.my_profile, name="officer_profile"),
]

