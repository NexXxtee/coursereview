from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView
from .models import Course, Category
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, FormView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Course, Category, CourseReview
from .forms import CourseReviewForm
import logging


logger = logging.getLogger(__name__)


def about_view(request):
    return render(request, 'reviews/about.html')


class CourseListView(ListView):
    model = Course
    template_name = 'reviews/course_list.html'
    context_object_name = 'courses'
    ordering = ['-created_at']  # Newest first
    paginate_by = 3

    def get_queryset(self):
        queryset = Course.objects.filter(is_published=True).prefetch_related('coursereview_set')
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset
    
    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context['categories'] = Category.objects.all()
            context['current_category'] = self.request.GET.get('category')
            for course in context['courses']:
                course.average_rating = course.get_average_rating()
            logger.debug(f'Загружено {len(context["courses"])} курсов')
            return context
        
        except Exception as e:
            logger.error(f'Ошибка при загрузке списка курсов: {str(e)}')
            raise
        
class CourseDetailView(DetailView):
    model = Course
    template_name = 'reviews/course_detail.html'
    context_object_name = 'course'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logger.info(f'Просмотр курса: {self.object.title} (slug: {self.object.slug})')
        # Добавляем в контекст только одобренные отзывы
        try:
            context['approved_reviews'] = self.object.coursereview_set.filter(status='approved')
            context['average_rating'] = self.object.get_average_rating()
            logger.info(f'Средний рейтинг курса {self.object.title}: {context["average_rating"]} - Успех')
        except Exception as e:
            logger.error(f'Ошибка при получении отзывов для курса {self.object.title}: {e}')
            context['approved_reviews'] = []
            context['average_rating'] = 0.0
            
        return context


class CourseReviewCreateView(LoginRequiredMixin, CreateView):
    model = CourseReview
    form_class = CourseReviewForm
    template_name = 'reviews/review_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course, slug=self.kwargs.get('slug'))
        return context
    
    def dispatch(self, request, *args, **kwargs):
        # Проверяем, не оставлял ли пользователь уже отзыв
        self.course = get_object_or_404(Course, slug=self.kwargs.get('slug'))
        if CourseReview.objects.filter(
            user=request.user,
            course=self.course
        ).exists():
            logger.warning(f'Пользователь {request.user} попытался создать повторный отзыв для курса {self.course.title}')
            messages.success(request, 'Вы уже оставили отзыв для этого курса.')
            return redirect('reviews:course_detail', slug=self.course.slug)
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        # Проверяем размер файла (максимум 5MB)
        try:
            if form.cleaned_data.get('certificate_image'):
                file_size = form.cleaned_data['certificate_image'].size
                if file_size > 5 * 1024 * 1024:
                    logger.warning(f'Пользователь {self.request.user} попытался загрузить слишком большой файл ({file_size/1024/1024:.2f} MB)')
                    form.add_error('certificate_image', 'Размер файла не должен превышать 5MB')
                    return self.form_invalid(form)
            
            form.instance.user = self.request.user
            form.instance.course = get_object_or_404(Course, slug=self.kwargs['slug'])
            return super().form_valid(form)
        
        except Exception as e:
            logger.error(f'Ошибка при создании отзыва от пользователя {self.request.user}: {str(e)}')  # Добавлено логирование
            raise 
            
    def get_success_url(self):
        messages.success(
            self.request,
            'Ваш отзыв отправлен на модерацию и будет опубликован после проверки.'
        )
        return reverse_lazy('reviews:course_detail', kwargs={'slug': self.kwargs['slug']})


# class UserReviewsListView(LoginRequiredMixin, ListView):
#     model = CourseReview
#     template_name = 'reviews/user_reviews.html'
#     context_object_name = 'reviews'
    
#     def get_queryset(self):
#         queryset = CourseReview.objects.filter(user=self.request.user)
#         # Фильтр по статусу из GET-параметра
#         status = self.request.GET.get('status')
#         if status in ['pending', 'approved', 'rejected']:
#             queryset = queryset.filter(status=status)
#         return queryset.order_by('-created_at')  # Сортировка по дате создания