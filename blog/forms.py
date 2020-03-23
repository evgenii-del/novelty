from django import forms
from blog.models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('text',)
