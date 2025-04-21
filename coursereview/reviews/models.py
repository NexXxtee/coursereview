from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import authenticate, login, logout, get_user_model

class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название курса")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Slug")
    description = models.TextField(verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    image = models.ImageField(
        upload_to="courses/%Y/%m/%d/",   
        blank=True, 
        null=True, 
        verbose_name="Фото"
    )
    category = models.ForeignKey(
        'Category', 
        on_delete=models.PROTECT, 
        verbose_name="Категория",
        related_name='courses'
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators = [MinValueValidator(0)],
        verbose_name="Цена",
    )
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('reviews:course_detail', kwargs={'slug': self.slug})
    
    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ['-created_at']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Slug")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return self.name
    

class ReviewVerification(models.Model):
    # Верификация права на отзыв
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name="Пользователь")
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name="Курс")
    certificate_image = models.ImageField(upload_to='certificates/%Y/%m/%d/', verbose_name="Сертификат/Чек")
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'На рассмотрении'),
            ('approved', 'Одобрено'),
            ('rejected', 'Отклонено')
        ],
        default='pending',
        verbose_name="Статус"
    )
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подачи")
    reviewed_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата рассмотрения")
    reviewed_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='reviews_moderated',
        verbose_name="Проверил"
    )

class Review(models.Model):
    # Отзывы
    verification = models.OneToOneField(
        ReviewVerification,
        on_delete=models.CASCADE,
        verbose_name="Верификация"
    )
    rating = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        verbose_name="Оценка"
    )
    comment = models.TextField(
        max_length=5000,
        verbose_name="Комментарий"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name="Опубликован"
    )