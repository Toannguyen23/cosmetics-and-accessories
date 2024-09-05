
from core.models import Category, Vendor, Product, WishList
from django.db.models import Min, Max
from django.contrib import messages

def default(request):
    
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))
    
    try:
        wishlist = WishList.objects.filter(user=request.user)
    except:
        messages.warning(request, "Không có sản phẩm yêu thích trong danh sách")
        wishlist = 0
    return {
        'categories' : categories,
        'wishlist' : wishlist,
        'vendors': vendors,
        'min_max_price': min_max_price,
    }