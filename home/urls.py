from django.urls import path
from .  import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('courses/', views.courses, name='courses'),
    path('news/', views.news, name='news'),
    path('elements/', views.elements, name='elements'),
path('course/<int:course_id>/', views.course_detail, name='course_detail'),
path('course/<int:course_id>/play/', views.course_player, name='course_player'),

]