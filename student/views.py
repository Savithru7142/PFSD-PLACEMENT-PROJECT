from django.shortcuts import render, redirect, get_object_or_404
from accounts.decorators import role_required
from .models import Student, Application
from employer.models import Job
from django.contrib import messages

@role_required("student")
def dashboard(request):
    student = getattr(request.user, 'student_profile', None)
    if not student:
        messages.error(request, "Student profile not found.")
        return redirect('home')
    
    applications = student.applications.all()
    app_count = applications.count()
    accepted_count = applications.filter(status='Accepted').count()
    
    context = {
        'student': student,
        'app_count': app_count,
        'accepted_count': accepted_count,
        'recent_applications': applications.order_by('-applied_at')[:5],
    }
    return render(request, "student/dashboard.html", context)

@role_required("student")
def browse_jobs(request):
    jobs = Job.objects.filter(status='Open')
    return render(request, "student/browse_jobs.html", {'jobs': jobs})

@role_required("student")
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk, status='Open')
    student = request.user.student_profile
    
    if Application.objects.filter(student=student, job=job).exists():
        messages.warning(request, "You have already applied for this job.")
    else:
        Application.objects.create(student=student, job=job)
        messages.success(request, f"Successfully applied for {job.title}")
    
    return redirect('student_browse_jobs')

@role_required("student")
def my_applications(request):
    applications = request.user.student_profile.applications.all()
    return render(request, "student/applications.html", {'applications': applications})

@role_required("student")
def my_profile(request):
    return render(request, "student/profile.html")
