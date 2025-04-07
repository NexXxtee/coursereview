from django.contrib import admin
from .models import Course, Category


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'updated_at', 'is_published')
    list_filter = ('category', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_published',)
    fields = (
        'title',
        'slug',
        'description',
        'image',
        'category',
        'price',
        'is_published'
    )
    save_on_top = True

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    
    
    