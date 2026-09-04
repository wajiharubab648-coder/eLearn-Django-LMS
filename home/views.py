from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Course, Lesson, Enrollment, Category, News, ContactMessage


def index(request):
    query = request.GET.get('search_query', '').strip()

    courses_list = Course.objects.all()

    # Agar Home Page se koi search kare
    if query:
        words = query.split()
        q_objects = Q()
        for word in words:
            q_objects |= Q(title__icontains=word) | \
                         Q(description__icontains=word) | \
                         Q(instructor__username__icontains=word) | \
                         Q(instructor__first_name__icontains=word) | \
                         Q(instructor__last_name__icontains=word)

        courses_list = courses_list.filter(q_objects).distinct()

    categories = Category.objects.all()[:5]

    context = {
        'courses': courses_list[:6],  # Home page par top 6 courses dikhane ke liye
        'search_query': query,
        'categories': categories,
    }
    return render(request, 'home/index.html', context)


def about(request):
    return render(request, 'home/about.html')


def contact(request):
    return render(request, 'home/contact.html')


def news(request):
    return render(request, 'home/news.html')


def elements(request):
    return render(request, 'home/elements.html')


def courses(request):
    search_query = request.GET.get('search_query', '').strip()
    category_id = request.GET.get('category', '').strip()

    courses_list = Course.objects.all().order_by('-id')

    if search_query:
        words = search_query.split()
        q_objects = Q()
        for word in words:
            q_objects |= Q(title__icontains=word) | \
                         Q(description__icontains=word) | \
                         Q(instructor__username__icontains=word) | \
                         Q(instructor__first_name__icontains=word)
        courses_list = courses_list.filter(q_objects).distinct()

    if category_id:
        courses_list = courses_list.filter(category_id=category_id)

    # 1 Page par sirf 6 courses show honge
    paginator = Paginator(courses_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    context = {
        'courses': page_obj,  # paginated courses
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
    }
    return render(request, 'home/courses.html', context)


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'home/course_detail.html', {'course': course})


def course_player(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # 1. Check if user is logged in
    if not request.user.is_authenticated:
        messages.warning(request, "You must log in and enroll in this course to access the lessons.")
        return redirect('course_detail', course_id=course.id)

    # 2. Check if the user is enrolled
    is_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()

    if not is_enrolled:
        messages.warning(request, "You must enroll in this course to access the lessons.")
        return redirect('course_detail', course_id=course.id)

    lessons = course.lessons.all().order_by('order')
    lesson_id = request.GET.get('lesson')

    if lesson_id:
        active_lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    else:
        active_lesson = lessons.first()

    return render(request, 'home/course_player.html', {
        'course': course,
        'lessons': lessons,
        'active_lesson': active_lesson,
    })

def news(request):
    news_list = News.objects.all().order_by('-created_at')
    return render(request, 'home/news.html', {'news_list': news_list})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')

    return render(request, 'home/contact.html')