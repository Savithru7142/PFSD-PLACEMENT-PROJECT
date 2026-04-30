from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="student"),
    path("jobs/", views.browse_jobs, name="student_browse_jobs"),
    path("jobs/<int:pk>/apply/", views.apply_job, name="student_apply_job"),
    path("applications/", views.my_applications, name="student_applications"),
    path("profile/", views.my_profile, name="student_profile"),
]
