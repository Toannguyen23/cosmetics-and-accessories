
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from core.models import Category, Product, Vendor, CartOrder, CartOrderItem, WishList, Address, ProductImage, ProductReview
from taggit.models import Tag
from django.db.models import Avg, Count
from core.forms import ProductReviewFrom
from django.template.loader import render_to_string
# import thu vien can thiet cho paypal
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
import datetime
from django.core import serializers
import calendar
from django.db.models.functions import ExtractMonth, ExtractYear
from userauths.models import ContactUs

# Create your views here.
def index(request):
    products = Product.objects.all().order_by('-id')
    context = {
        'products': products,
    }
    return render(request, 'core/index.html', context)

def product_list_view(request):
    products = Product.objects.filter(product_status="published")
    context = {
        'products': products,
    }
    return render(request, 'core/product-list.html', context)


def category_list_view(request):
    categories = Category.objects.all()
    
    context = {
        'categories': categories
    }
    
    return render(request, 'core/category-list.html', context)


def category_product_list(request, cid):
    
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status="published", category=category)
    
    context = {
        'category': category,
        'products': products
    }
    
    return render(request, 'core/category_product_list.html', context)


def vendor_list_view(request):
    vendors = Vendor.objects.all()
    context = {
        'vendors': vendors
    }
    return render(request, 'core/vendor_list.html', context)


def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    p_image = product.p_images.all()
    products = Product.objects.filter(category=product.category).exclude(pid=pid)
    reviews = ProductReview.objects.filter(product=product).order_by('-date')
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    review_form = ProductReviewFrom()
    
    make_review = True
    user_review_count = 0    
    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()
    
    if user_review_count > 0:
        make_review = False
    
    context = {
        "products": product,
        "product" : products,
        'p_image' : p_image,
        'reviews' : reviews,
        'average_rating': average_rating,
        'review_form': review_form,
        'make_review': make_review
    }
    return render(request, 'core/product_detail.html', context)

def tag_list(request, tag_slug=None):
    products = Product.objects.filter(product_status = "published")
    
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
        
    context ={
        'products':products,
        'tag':tag
    }
    
    return render(request, 'core/tag.html', context)


def ajax_add_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user
    
    review = ProductReview.objects.create(
        user = user,
        product = product,
        review = request.POST['review'],
        rating = request.POST['rating'],
    )
    
    context = {
        'user':user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating']
    }
    
    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    
    result =  JsonResponse(
        {
            'bool': True,
            'context': context,
            'average_reviews': average_reviews
        }
    )

    
    return result


def search_view(request):
    
    query = request.GET.get('search')
    products = Product.objects.filter(title__icontains=query).order_by('-date')
    
    context = {
        'products': products,
        'query': query
    }
    
    return render(request, 'core/search.html', context)


def filter_product(request):
    categories = request.GET.getlist('category[]')
    vendors = request.GET.getlist('vendor[]')
    
    products = Product.objects.filter(product_status="published").order_by("-id").distinct()
    
    min_price = request.GET['min_price']
    max_price = request.GET['max_price']
    
    products = products.filter(price__gte = min_price)
    products = products.filter(price__lte = max_price)
    
    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct()
        
    if len(vendors) > 0:
        products = products.filter(vendor__id__in=vendors).distinct()
        
    data = render_to_string("core/async/product-list.html", {'products': products})
    
    return JsonResponse(
        {
            "data" : data,
        }
    )
    
def add_to_cart(request):
    cart_product = {}
        
    cart_product[request.GET['id']] = {
        'title':request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'image':request.GET.getlist('image'),
        'pid': request.GET.getlist('pid'),
    }
    
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            
            request.session['cart_data_obj'] = cart_data
            
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product
        
    return JsonResponse({
        "data": request.session['cart_data_obj'],
        "totalCartItems": len(request.session['cart_data_obj'])
    })
    
    
def cart_view(request):
    
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price']) if item['price'] else 0
            
        return render(request,  "core/cart.html", {"cart_data": request.session['cart_data_obj'], 'totalCartItems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    
    else:
        
        return render(request,  "core/cart.html", {"cart_data":"", 'totalCartItems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
        

def delete_item_from_cart(request):
    
    product_id = str(request.GET.get('id'))
    
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data
            
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price']) if item['price'] else 0
        
    context = render_to_string("core/async/cart-list.html",{"cart_data": request.session['cart_data_obj'], 'totalCartItems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount} )
        
    return JsonResponse({
        "data" : context,
        'totalCartItems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount
    })
    

def update_item_from_cart(request):
    
    product_id = str(request.GET.get('id'))
    product_qty = str(request.GET.get('qty'))
    
    
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET.get('id'))]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data
            
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price']) if item['price'] else 0
        
    context = render_to_string("core/async/cart-list.html",{"cart_data": request.session['cart_data_obj'], 'totalCartItems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount} )
        
    return JsonResponse({
        "data" : context,
        'totalCartItems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount
    })
    
    
def save_checkout_infor(request):
    cart_total_amount = 0
    total_amount = 0
    
    if request.method == "POST":
        full_name = request.POST.get("fullname")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        state = request.POST.get("state")
        zipcode  = request.POST.get("zipcode")
        
        request.session['fullname'] = full_name
        request.session['email'] = email
        request.session['phone'] = phone
        request.session['address'] = address
        request.session['state'] = state
        request.session['zipcode'] = zipcode
        
        if 'cart_data_obj' in request.session:
            for p_id, item in request.session['cart_data_obj'].items():
                total_amount += int(item['qty']) * float(item['price']) if item['price'] else 0

            order = CartOrder.objects.create(
            user = request.user,
            price = total_amount,
            fullname = full_name,
            email = email,
            phone = phone,
            address = address,
            state = state,
            zipcode = zipcode
            )           
            for p_id, item in request.session['cart_data_obj'].items():
                cart_total_amount += int(item['qty']) * float(item['price']) if item['price'] else 0
    
                cart_order_products = CartOrderItem.objects.create(
                    order=order,
                    invoice_no = "HOA DON SO-" + str(order.id),
                    item = item['title'],
                    image=item['image'][0],
                    quantity = item['qty'],
                    price=item['price'],
                    total = float(item['qty']) * float(item['price'])
                        )
            del request.session['fullname']
            del  request.session['email']
            del request.session['phone'] 
            del request.session['address'] 
            del request.session['state'] 
            del request.session['zipcode'] 
            
        return redirect("core:checkout", order.oid)
    return redirect("core:checkout", order.oid)


def payment_completed_view(request, oid):
    
    order = CartOrder.objects.get(oid=oid)
    if order.paid_status == False:
        order.paid_status = True
        order.save()
    context = {
        "order" : order,
        
    }
    
    return render(request, 'core/payment-completed.html', context)


def payment_failed_view(request):
    
    return render(request, 'core/payment-failed.html')


def checkout(request, oid):
    order = CartOrder.objects.get(oid=oid)
    order_items = CartOrderItem.objects.filter(order=order)
    
    
    context ={
        "order": order,
        "order_items": order_items
    }
    
    return render(request, "core/checkout.html", context)
    

def dashboard_view(request):
    orders_list = CartOrder.objects.filter(user=request.user)
    address = Address.objects.filter(user=request.user)
    orders = CartOrder.objects.annotate(month=ExtractMonth("order_date")).values( "month").annotate(count=Count("id")).values("month", "count")
    

    month = []
    total_orders = []
    
    for o in orders: 
        month.append(calendar.month_name[o['month']])
        total_orders.append(o['count'])
    
    if request.method == "POST":
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        
        new_address = Address.objects.create(
            user= request.user,
            address = address,
            mobile = mobile
        )
        
        messages.success(request, "Thêm địa chỉ mới thành công!")
        return redirect("core:dashboard")
    context = {
        "orders_list": orders_list,
        "address": address, 
        "orders" : orders,
        "month": month,
        "total_orders" : total_orders,
       
    }
    
    return render(request, 'core/dashboard.html', context)


def order_detail(request, id):
    order = CartOrder.objects.get(user=request.user, id=id)
    products = CartOrderItem.objects.filter(order=order)
    
    context = {
        'order': order,
        'products': products
    }
    
    return render(request, 'core/order-detail.html', context)


def make_address_default(request):
    
    id = request.GET["id"]
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    
    return JsonResponse({
        "boolean": True,
    })
    
def wishlist_view(request):
    
    w = WishList.objects.all()
    
    context = {
        'wishlist': w,
    }
    
    return render(request, 'core/wishlist.html', context)


def add_to_wishlist(request):
    
    id = request.GET["id"]
    product = Product.objects.get(id=id)
    
    context = {}
    wishlist_count = WishList.objects.filter(product=product, user=request.user).count()
    
    if wishlist_count > 0:
        
        context={
            "bool" : True
        }
    else:
        new_wishlist = WishList.objects.create(
            product = product,
            user=request.user
        )
    context ={
        "bool": True
    }
    
    return JsonResponse(context)
    

def remove_wishlist(request):
    pid = request.GET['id']
    
    wishlist = WishList.objects.filter(user=request.user)
    product = WishList.objects.get(id=pid)
    product.delete()
    
    context ={
        "bool": True,
        "wishlist": wishlist
    }    
    
    data = render_to_string("core/async/wishlist-list.html", context)
    wishlist_json = serializers.serialize("json", wishlist)
    return JsonResponse({
        "data": data,
        "wishlist": wishlist_json
    })
    
    
#Các trang bổ trợ

def contact(request):
    
    return render(request, "core/contact.html")

def ajax_contact(request):
    fullname = request.GET["fullname"]
    email = request.GET["email"]
    phone = request.GET["phone"]
    subject = request.GET["subject"]
    message = request.GET["message"]
    
    contact = ContactUs.objects.create(
        full_name = fullname,
        email = email,
        phone = phone,
        subject = subject,
        message = message
    )
    
    context = {
        "bool" : True,
        "text": "Gửi phản hồi thành công"
    }
    
    return JsonResponse({"data": context})