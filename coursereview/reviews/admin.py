from django.contrib import admin
from .models import Course, Category, CourseReview
from django.utils import timezone

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_at", "updated_at", "is_published")
    readonly_fields = ("created_at", "updated_at")
    list_filter = ("category", "created_at", "updated_at")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("is_published",)
    fields = (
        "title",
        "slug",
        "description",
        "image",
        "category",
        "price",
        "is_published",
    )
    save_on_top = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'course', 'rating', 'status',
        'created_at', 'reviewed_at', 'reviewed_by'
    )
    list_filter = ('status', 'rating', 'created_at', 'reviewed_at')
    search_fields = ('user__username', 'course__title', 'comment')
    list_editable = ('status',)
    readonly_fields = ('created_at', 'reviewed_at', 'reviewed_by')
    
    def save_model(self, request, obj, form, change):
        if 'status' in form.changed_data: # Проверяет, было ли изменено поле 'status'
            obj.reviewed_by = request.user
            obj.reviewed_at = timezone.now()
        super().save_model(request, obj, form, change)