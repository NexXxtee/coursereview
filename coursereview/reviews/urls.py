from django.urls import path
from . import views
from django.views.decorators.cache import cache_page


app_name = 'reviews'

urlpatterns = [
    path('', cache_page(10)(views.CourseListView.as_view()), name='course_list'),
    path('about/', views.about_view, name='about'),
    path('course/<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('course/<slug:slug>/review/', views.CourseReviewCreateView.as_view(), name='create_review'),
]

