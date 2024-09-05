from django.shortcuts import render, redirect
from core.models import CartOrder, Product, Category, Vendor
from django.db.models import Sum
from userauths.models import User
import datetime
from useradmin.forms import AddProductForm
from django.contrib import messages
# Create your views here.

def dashboard(request):
    revenue = CartOrder.objects.aggregate(price=Sum("price"))
    total_orders_count = CartOrder.objects.all()
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    new_customers = User.objects.all().order_by("-id")
    latest_orders = CartOrder.objects.all()
    
    this_month = datetime.datetime.now().month
    monthly_revenue = CartOrder.objects.filter(order_date__month=this_month).aggregate(price=Sum("price"))
    
    context = {
        "revenue": revenue,
        "total_orders_count": total_orders_count,
        "all_products": all_products,
        "all_categories": all_categories,
        "new_customers": new_customers,
        "latest_orders": latest_orders,
        "monthly_revenue": monthly_revenue,
        "this_month": this_month
    }
    
    return render(request, "useradmin/dashboard.html", context)


def product(request):
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    
    context = {
        "all_products": all_products,
        "all_categories": all_categories,
    }
    
    return render(request, "useradmin/product.html", context)


def add_product(request):
    form = AddProductForm()
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)
        print("sau hon")
        if form.is_valid():
           new_form = form.save(commit=False)
           
           new_form.user = request.user
           new_form.save()
           form.save_m2m()
           print("sau hon nua")
           return redirect("useradmin:dashboard")
        else:
           print(form.errors)
    else: 
        print("form k co gi ngoai cung")
        
    context = {
        "form" : form,
    }
    
    return render(request, "useradmin/add-product.html", context)


def edit_product(request, pid):
    product = Product.objects.get(pid=pid)
    form = AddProductForm()
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES, instance=product)
        print("sau hon")
        if form.is_valid():
           new_form = form.save(commit=False)
           
           new_form.user = request.user
           new_form.save()
           form.save_m2m()
           messages.success(request, "Sản phẩm cập nhật thành công! Vui lòng xem lại thông tin đã cập nhật")
           return redirect("useradmin:edit-product", product.pid)
        else:
           print(form.errors)
    else: 
        form = AddProductForm(instance=product)
        
    context = {
        "form" : form,
        "product": product
    }
    
    return render(request, "useradmin/edit-product.html", context)


def delete_product(request, pid):
    product = Product.objects.get(pid=pid)
    
    product.delete()
    
    return redirect("useradmin:products")