from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
STATUS_CHOICES = (
    ('process', 'Proccssing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
    
)
STATUS = (
    ('draft', 'Draft'),
    ('disable', 'Disable'),
    ('in_review', 'In Review'),
    ('published', 'Published'),
    ('rejected', 'Rejected'),
)
RATING = (
    (1, '⭐ ☆ ☆ ☆ ☆'),
    (2, '⭐⭐ ☆ ☆ ☆'),
    (3, '⭐⭐⭐ ☆ ☆'),
    (4, '⭐⭐⭐⭐ ☆ '),
    (5, '⭐⭐⭐⭐⭐'),
    
)

def user_directory_path(instance, filename):
    return "user_{0}/{1}".format(instance.user.id, filename)


class Tag(models.Model):
    pass    
    
class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=30, prefix="cat", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="category")
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.image.url))
    
    def __str__(self):
        return self.title
    
class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=30, prefix="ven", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, default="CJ co.ltd")
    image = models.ImageField(upload_to=user_directory_path, default='vendor.jpg')
    # description = models.TextField(null=True, blank=True)
    description = RichTextUploadingField(null=True, blank=True, default="JC Vietnam ltd.co")
    address = models.CharField(max_length=100, default="Ho Chi Minh")
    contact = models.CharField(max_length=100, null =True, default="1800 9898")
    chat_response_time = models.CharField(max_length=100, null=True, default="100")
    shipping_on_time = models.CharField(max_length=100, null=True, default="100")
    authentic_rating = models.CharField(max_length=100, null=True, default="100")
    days_return = models.CharField(max_length=100, null=True, default="100")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name_plural = "Vendors"
    
    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.image.url))
    
    def __str__(self):
        return self.title

class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=30, alphabet="abcdefgh12345")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='category')
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name='vendor')
    
    
    title = models.CharField(max_length=100, default="Ao Thun")
    image = models.ImageField(upload_to="category")
    description = RichTextUploadingField(null=True, blank=True, default="Sản phẩm mới thiết kế đa dạng")
    
    price = models.DecimalField(max_digits=12, decimal_places=3, default='100.000')
    old_price = models.DecimalField(max_digits=12, decimal_places=3, default='150.000')
    specifications = RichTextUploadingField(null=True, blank=True)
    tags = TaggableManager(blank=True)
    product_status = models.CharField(choices=STATUS, max_length=10, default='in_review')
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=True)
    digital = models.BooleanField(default=True)
    stock_count = models.CharField(max_length=20, default='18', null=True, blank=True)
    sku = ShortUUIDField(unique=True, length=4, max_length=10,prefix="sku", alphabet="1234567890")
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Products"
    
    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.image.url))
    
    def __str__(self):
        return self.title
    
    def get_percentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price
        
class ProductImage(models.Model):
    images = models.ImageField(upload_to="product-image", default="product.jpg")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='p_images')
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Product-Images"
        
####Phan Order####

class CartOrder(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    fullname = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    state = models.CharField(max_length=150, blank=True, null=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    
    shipping_method = models.CharField(max_length=150, blank=True, null=True)
    tracking_id = models.CharField(max_length=150, blank=True, null=True)
    tracking_website_address = models.CharField(max_length=150, blank=True, null=True)
    
    
    price = models.DecimalField(max_digits=12, decimal_places=3, default='100.000')
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICES, max_length=30, default='processing')
    oid = ShortUUIDField(unique=True, length=4, max_length=10, alphabet="1234567890")

    
    class Meta:
        
        verbose_name_plural = "Cart Order"
        
class CartOrderItem(models.Model):
    
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=250)
    product_status = models.CharField( max_length=30)
    item = models.CharField( max_length=200)
    image = models.CharField( max_length=200)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=3, default='100.000')
    total = models.DecimalField(max_digits=12, decimal_places=3, default='100.000')
    
    class Meta:
        
        verbose_name_plural = "Cart Order Items"
    
    def order_img(self):
        
        return mark_safe('<img src="/media/%s" width="50" height="50"/>' % (self.image))
    
    
class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='reviews')
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Product Reviews"
        
    def __str__(self):
        
        return self.product.title
    
    
    def get_rating(self):
        
        return self.rating
    
class WishList(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Wishlist"
        
    def __str__(self):
        
        return self.product.title
    
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    mobile = models.CharField(max_length=20, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Addresses"
    
    
    
    
    
    
    
    
    
    