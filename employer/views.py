from django.shortcuts import render, redirect, get_object_or_404
from accounts.decorators import role_required
from .models import Company, Job
from student.models import Application
from django.contrib import messages

@role_required("employer")
def dashboard(request):
    company = getattr(request.user, 'company_profile', None)
    if not company:
        messages.error(request, "Company profile not found.")
        return redirect('home')
    
    jobs = company.jobs.all()
    job_count = jobs.count()
    applications = Application.objects.filter(job__company=company)
    app_count = applications.count()
    
    context = {
        'company': company,
        'job_count': job_count,
        'app_count': app_count,
        'recent_jobs': jobs.order_by('-posted_at')[:5],
    }
    return render(request, "employer/dashboard.html", context)

@role_required("employer")
def my_jobs(request):
    company = request.user.company_profile
    jobs = company.jobs.all()
    return render(request, "employer/my_jobs.html", {'jobs': jobs})

@role_required("employer")
def post_job(request):
    if request.method == "POST":
        title = request.POST.get('title')
        location = request.POST.get('location')
        salary = request.POST.get('salary')
        description = request.POST.get('description')
        
        Job.objects.create(
            company=request.user.company_profile,
            title=title,
            location=location,
            salary=salary,
            description=description
        )
        messages.success(request, "Job posted successfully!")
        return redirect('employer_jobs')
    return render(request, "employer/post_job.html")

@role_required("employer")
def view_applications(request):
    company = request.user.company_profile
    applications = Application.objects.filter(job__company=company)
    return render(request, "employer/applications.html", {'applications': applications})

@role_required("employer")
def update_app_status(request, pk):
    application = get_object_or_404(Application, pk=pk, job__company=request.user.company_profile)
    if request.method == "POST":
        status = request.POST.get('status')
        application.status = status
        application.save()
        messages.success(request, f"Application status updated to {status}")
    return redirect('employer_applications')
