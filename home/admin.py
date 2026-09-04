from django.contrib import admin
from .models import Course, Enrollment, Lesson, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'instructor', 'created_at')
    list_filter = ('category', 'created_at')
    inlines = [LessonInline]


admin.site.register(Lesson)
admin.site.register(Enrollment)