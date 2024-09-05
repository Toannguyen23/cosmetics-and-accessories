from django import forms
from core.models import ProductReview

class ProductReviewFrom(forms.ModelForm):
    
    review = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Vui lòng đánh giá..."}))
    
    class Meta:
        model = ProductReview
        fields = ['review', 'rating']
        