from django import forms
from .models import CourseReview

class CourseReviewForm(forms.ModelForm):
    class Meta:
        model = CourseReview
        fields = ['rating', 'comment', 'certificate_image']
        widgets = {
            'rating': forms.Select(attrs={
                'class': 'form-control'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Поделитесь своим опытом обучения на курсе...'
            }),
            'certificate_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            })
        }