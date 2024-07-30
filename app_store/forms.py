from django import forms
from .models import Review
from django.forms import fields



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'subject',
            'review',
            'rating'
        ]

