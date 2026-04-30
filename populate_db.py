import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PLACEMENT_TRACKING_SYS.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile
from student.models import Student, Application
from employer.models import Company, Job

def populate():
    # Ensure admin exists
    admin_user, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@test.com', 'is_staff': True, 'is_superuser': True})
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
    
    UserProfile.objects.get_or_create(user=admin_user, defaults={'role': 'admin'})

    # Ensure Placement Officer exists
    officer_user, created = User.objects.get_or_create(username='officer', defaults={'email': 'officer@test.com'})
    if created:
        officer_user.set_password('officer123')
        officer_user.save()
    UserProfile.objects.get_or_create(user=officer_user, defaults={'role': 'placement_officer'})

    # Create Companies
    companies_data = [
        {'name': 'Infosys', 'location': 'Bangalore', 'industry': 'IT Services', 'email': 'hr@infosys.com'},
        {'name': 'TCS', 'location': 'Mumbai', 'industry': 'IT Consulting', 'email': 'careers@tcs.com'},
        {'name': 'Wipro', 'location': 'Pune', 'industry': 'Software', 'email': 'jobs@wipro.com'},
        {'name': 'HCL', 'location': 'Noida', 'industry': 'Technology', 'email': 'recruitment@hcl.com'},
        {'name': 'Tech Mahindra', 'location': 'Chennai', 'industry': 'IT Services', 'email': 'careers@techmahindra.com'},
    ]
    
    companies = []
    for cdata in companies_data:
        company, _ = Company.objects.get_or_create(name=cdata['name'], defaults={
            'location': cdata['location'],
            'industry': cdata['industry'],
            'contact_email': cdata['email']
        })
        companies.append(company)

    # Create Jobs
    jobs_data = [
        {'title': 'Software Developer', 'company': companies[0], 'location': 'Bangalore', 'salary': '₹5-7 LPA', 'status': 'Open'},
        {'title': 'Data Analyst', 'company': companies[1], 'location': 'Mumbai', 'salary': '₹4-6 LPA', 'status': 'Open'},
        {'title': 'Web Developer', 'company': companies[2], 'location': 'Pune', 'salary': '₹4.5-6.5 LPA', 'status': 'Open'},
        {'title': 'System Engineer', 'company': companies[3], 'location': 'Noida', 'salary': '₹3.5-5 LPA', 'status': 'Open'},
    ]
    
    jobs = []
    for jdata in jobs_data:
        job, _ = Job.objects.get_or_create(title=jdata['title'], company=jdata['company'], defaults={
            'location': jdata['location'],
            'salary': jdata['salary'],
            'status': jdata['status'],
            'description': f"Exciting role as {jdata['title']} at {jdata['company'].name}"
        })
        jobs.append(job)

    # Create Students
    students_data = [
        {'username': 'priya', 'name': 'Priya Sharma', 'dept': 'Computer Science', 'email': 'priya@student.com', 'phone': '9876543210'},
        {'username': 'rajesh', 'name': 'Rajesh Kumar', 'dept': 'Information Technology', 'email': 'rajesh@student.com', 'phone': '9876543211'},
        {'username': 'anjali', 'name': 'Anjali Patel', 'dept': 'Computer Science', 'email': 'anjali@student.com', 'phone': '9876543212'},
        {'username': 'vikram', 'name': 'Vikram Singh', 'dept': 'Electronics', 'email': 'vikram@student.com', 'phone': '9876543213'},
        {'username': 'deepika', 'name': 'Deepika Reddy', 'dept': 'Computer Science', 'email': 'deepika@student.com', 'phone': '9876543214'},
        {'username': 'arjun', 'name': 'Arjun Gupta', 'dept': 'Information Technology', 'email': 'arjun@student.com', 'phone': '9876543215'},
    ]
    
    students = []
    for sdata in students_data:
        user, _ = User.objects.get_or_create(username=sdata['username'], defaults={
            'email': sdata['email'],
            'first_name': sdata['name'].split()[0],
            'last_name': sdata['name'].split()[1] if len(sdata['name'].split()) > 1 else ''
        })
        UserProfile.objects.get_or_create(user=user, defaults={'role': 'student'})
        student, _ = Student.objects.get_or_create(user=user, defaults={
            'department': sdata['dept'],
            'phone': sdata['phone']
        })
        students.append(student)

    # Create Applications
    for i in range(4):
        Application.objects.get_or_create(student=students[i], job=jobs[i], defaults={'status': 'Processing'})

    print("Database populated successfully!")

if __name__ == '__main__':
    populate()
