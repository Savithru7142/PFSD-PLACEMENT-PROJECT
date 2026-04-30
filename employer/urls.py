from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="employer"),
    path("jobs/", views.my_jobs, name="employer_jobs"),
    path("jobs/post/", views.post_job, name="employer_post_job"),
    path("applications/", views.view_applications, name="employer_applications"),
    path("applications/<int:pk>/status/", views.update_app_status, name="employer_update_status"),
]

