from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProfileUpdateForm

from accounts.forms import CustomUserChangeForm
from home.models import Course, Enrollment

# Custom User Model lookup
User = get_user_model()


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        confirm_password = request.POST.get('confirm_password')

        # Password matching check
        if password == confirm_password:
            # Check existing username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username has been taken, choose another one.')
                return redirect('register')

            # Check existing email
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists, choose another one.')
                return redirect('register')

            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                user.save()
                messages.success(request, 'User registered successfully. Please log in.')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

    return render(request, 'registration/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)

            if remember_me:
                request.session.set_expiry(1209600)
            else:
                request.session.set_expiry(0)

            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    # Path ko 'registration/login.html' kar dein:
    return render(request, 'registration/login.html')


def logout_view(request):
    auth_logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')


def logout_view(request):
    auth_logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')


@login_required
def dashboard(request):
    if request.method == 'POST' and 'create_course' in request.POST:
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title and description:
            Course.objects.create(
                title=title,
                description=description,
                instructor=request.user
            )
            messages.success(request, f"Course '{title}' created successfully!")
        return redirect('dashboard')

    if request.user.is_staff or getattr(request.user, 'user_type', '') == 'instructor':
        created_courses = Course.objects.filter(instructor=request.user)
        enrolled_count = Enrollment.objects.filter(course__in=created_courses).count()
        completed_count = Enrollment.objects.filter(course__in=created_courses, is_completed=True).count()
        enrolled_courses = []
    else:
        created_courses = []
        user_enrollments = Enrollment.objects.filter(user=request.user)
        enrolled_count = user_enrollments.count()
        completed_count = user_enrollments.filter(is_completed=True).count()
        enrolled_courses = user_enrollments

    context = {
        'enrolled_count': enrolled_count,
        'completed_count': completed_count,
        'enrolled_courses': enrolled_courses,
        'created_courses': created_courses,
    }
    return render(request, 'registration/dashboard.html', context)


@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)

    if created:
        messages.success(request, f"Successfully enrolled in '{course.title}'!")
    else:
        messages.info(request, f"You are already enrolled in '{course.title}'.")

    return redirect('dashboard')


@login_required
def delete_course(request, course_id):
    if not request.user.is_staff:
        messages.error(request, "Permission denied!")
        return redirect('dashboard')

    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    course_title = course.title
    course.delete()
    messages.success(request, f"Course '{course_title}' has been deleted successfully.")
    return redirect('dashboard')

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'registration/profile.html', {'form': form})