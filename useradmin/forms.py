
from core.models import Product
from django import forms 

class AddProductForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Tên sản phẩm", "class": "form-control"}))
    description = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Mô tả", "class": "form-control"}))
    price = forms.CharField(widget=forms.NumberInput(attrs={"placeholder": "Giá...", "class": "form-control"}))
    old_price = forms.CharField(widget=forms.NumberInput(attrs={"placeholder": "Giá cũ..", "class": "form-control"}))
    stock_count = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Số lượng sản phẩm hiện có", "class": "form-control"}))
    updated= forms.DateTimeField(widget=forms.DateTimeInput(attrs={"placeholder": "Ngày cập nhật...", "class": "form-control"}))
    tags = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Gán nhãn hashtag ví dụ: #cream", "class": "form-control"}))
    image = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control"}))

    
    
    class Meta:
        model = Product
        
        fields = [
            "title",
            "sku",
            "description",
            "vendor",
            "price",
            "old_price",
            "specifications",
            "tags",
            "image",
            "product_status",
            "in_stock",
            "digital",
            "stock_count",
            "updated",
            "pid",
            "status",
            "featured",
            "category",
        ]