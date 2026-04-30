from django.shortcuts import render, redirect, get_object_or_404
from accounts.decorators import role_required
from django.contrib.auth.models import User
from accounts.models import UserProfile
from student.models import Student, Application
from employer.models import Company, Job
from django.contrib import messages

@role_required("admin")
def dashboard(request):
    total_users = User.objects.count()
    active_jobs = Job.objects.filter(status='Open').count()
    total_applications = Application.objects.count()
    
    students_count = Student.objects.count()
    employers_count = Company.objects.count()
    job_postings_count = Job.objects.count()
    
    context = {
        'total_users': total_users,
        'active_jobs': active_jobs,
        'total_applications': total_applications,
        'students_count': students_count,
        'employers_count': employers_count,
        'job_postings_count': job_postings_count,
    }
    return render(request, "admin/dashboard.html", context)

# --- Student Management ---
@role_required("admin")
def students_list(request):
    students = Student.objects.all()
    return render(request, "admin/students.html", {'students': students})

@role_required("admin")
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, "admin/student_detail.html", {'student': student})

@role_required("admin")
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    user = student.user
    student.delete()
    user.delete()
    messages.success(request, "Student deleted successfully.")
    return redirect("admin_students")

# --- Company Management ---
@role_required("admin")
def companies_list(request):
    companies = Company.objects.all()
    return render(request, "admin/companies.html", {'companies': companies})

@role_required("admin")
def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk)
    return render(request, "admin/company_detail.html", {'company': company})

@role_required("admin")
def company_delete(request, pk):
    company = get_object_or_404(Company, pk=pk)
    company.delete()
    messages.success(request, "Company deleted successfully.")
    return redirect("admin_companies")

# --- Job Management ---
@role_required("admin")
def jobs_list(request):
    jobs = Job.objects.all()
    return render(request, "admin/jobs.html", {'jobs': jobs})

@role_required("admin")
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, "admin/job_detail.html", {'job': job})

@role_required("admin")
def job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk)
    job.delete()
    messages.success(request, "Job deleted successfully.")
    return redirect("admin_jobs")

# --- Application Management ---
@role_required("admin")
def applications_list(request):
    applications = Application.objects.all()
    return render(request, "admin/applications.html", {'applications': applications})

@role_required("admin")
def application_delete(request, pk):
    app = get_object_or_404(Application, pk=pk)
    app.delete()
    messages.success(request, "Application record deleted.")
    return redirect("admin_applications")

@role_required("admin")
def my_profile(request):
    return render(request, "admin/profile.html")
