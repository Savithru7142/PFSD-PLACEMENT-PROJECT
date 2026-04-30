from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import redirect, render

from .models import UserProfile


def home(request):
    role_display = None
    auth_tab = request.GET.get("auth")
    if request.user.is_authenticated:
        profile = getattr(request.user, "profile", None)
        role_display = profile.get_role_display() if profile else "No Role"
    if auth_tab not in {"login", "signup"}:
        auth_tab = None
    return render(request, "home.html", {"role_display": role_display, "auth_tab": auth_tab})


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        selected_role = request.POST.get("role", "").strip()

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, "Invalid username or password.")
            return redirect(f"{reverse('home')}?auth=login")

        profile = getattr(user, "profile", None)
        if profile is None or selected_role != profile.role:
            messages.error(request, "Role does not match this account.")
            return redirect(f"{reverse('home')}?auth=login")

        login(request, user)
        return redirect("role-dashboard")
    return render(request, "login.html")


def signup_page(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        role = request.POST.get("role", UserProfile.ROLE_STUDENT)

        if not all([full_name, username, email, password]):
            messages.error(request, "Please fill all signup fields.")
            return redirect(f"{reverse('home')}?auth=signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect(f"{reverse('home')}?auth=signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect(f"{reverse('home')}?auth=signup")

        first_name = full_name.split()[0]
        last_name = " ".join(full_name.split()[1:]) if len(full_name.split()) > 1 else ""
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user_profile = UserProfile.objects.create(user=user, role=role)
        
        # Create corresponding profile based on role
        if role == UserProfile.ROLE_STUDENT:
            from student.models import Student
            Student.objects.create(user=user)
        elif role == UserProfile.ROLE_EMPLOYER:
            from employer.models import Company
            Company.objects.create(user=user, name=full_name, contact_email=email)
            
        messages.success(request, "Account created. Please login to continue.")
        return redirect(f"{reverse('home')}?auth=login")
    return render(request, "signup.html")


def role_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("home")

    user_role = getattr(getattr(request.user, "profile", None), "role", None)

    if user_role == UserProfile.ROLE_STUDENT:
        return redirect("student")
    if user_role == UserProfile.ROLE_ADMIN:
        return redirect("admin_role")
    if user_role == UserProfile.ROLE_PLACEMENT_OFFICER:
        return redirect("placement_office")
    if user_role == UserProfile.ROLE_EMPLOYER:
        return redirect("employer")

    messages.error(request, "Your account does not have an assigned role.")
    return redirect("home")


def logout_page(request):
    logout(request)
    return redirect("home")
