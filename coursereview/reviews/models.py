from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

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
