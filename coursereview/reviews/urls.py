from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('about/', views.about_view, name='about'),
    path('', views.CourseListView.as_view(), name='course_list'),
]