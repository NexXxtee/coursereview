from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView
from .models import Course, Category


def about_view(request):
    return render(request, 'reviews/about.html')


class CourseListView(ListView):
    model = Course
    template_name = 'reviews/course_list.html'
    context_object_name = 'courses'
    ordering = ['-created_at']  # Newest first
    paginate_by = 10

class CourseDetailView(DetailView):
    model = Course
    template_name = 'reviews/course_detail.html'
    context_object_name = 'course'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'