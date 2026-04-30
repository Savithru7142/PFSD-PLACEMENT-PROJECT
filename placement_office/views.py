from django.shortcuts import render, get_object_or_404, redirect
from accounts.decorators import role_required
from student.models import Student, Application
from employer.models import Company, Job
from django.contrib import messages

@role_required("placement_officer")
def dashboard(request):
    total_students = Student.objects.count()
    companies_registered = Company.objects.count()
    placements_done = Application.objects.filter(status='Accepted').count()
    
    recent_students = Student.objects.all()[:5]
    
    context = {
        'total_students': total_students,
        'companies_registered': companies_registered,
        'placements_done': placements_done,
        'recent_students': recent_students,
    }
    return render(request, "officer/dashboard.html", context)

@role_required("placement_officer")
def students_list(request):
    students = Student.objects.all()
    return render(request, "officer/students.html", {'students': students})

@role_required("placement_officer")
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, "officer/student_detail.html", {'student': student})

@role_required("placement_officer")
def companies_list(request):
    companies = Company.objects.all()
    return render(request, "officer/companies.html", {'companies': companies})

@role_required("placement_officer")
def applications_list(request):
    applications = Application.objects.all()
    return render(request, "officer/applications.html", {'applications': applications})

@role_required("placement_officer")
def my_profile(request):
    return render(request, "officer/profile.html")
