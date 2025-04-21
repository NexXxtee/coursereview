from django.contrib import admin
from .models import Course, Category, ReviewVerification, Review


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


@admin.register(ReviewVerification)
class ReviewVerificationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "course",
        "certificate_image",
        "status",
        "submitted_at",
        "reviewed_at",
    )
    readonly_fields = ("submitted_at",)
    search_fields = ("user", "course")
    list_filter = ("user", "course", "submitted_at", 'reviewed_at')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('rating', 'comment', 'created_at', 'is_published')
    readonly_fields = ('created_at',)
    list_filter = ('rating', 'created_at', 'is_published')
    