from django.urls import path, include
from core import views

app_name ="core"

urlpatterns = [
   path('', views.index, name='index'),
   path('products/', views.product_list_view, name='product-list'),
   path('categories/', views.category_list_view, name='category-list'),
   path('category_product/<cid>/', views.category_product_list, name='category-product-list'),
   path('vendor_list/', views.vendor_list_view, name="vendor-list"),
   path('product_detail/<pid>/', views.product_detail_view, name='product-detail'),
   path('product/tags/<slug:tag_slug>/', views.tag_list, name='tags'),
   path('ajax-add-review/<int:pid>/', views.ajax_add_review, name="ajax-add-review"),
   path('search/', views.search_view, name='search'),
   path('filter-products/', views.filter_product, name="filter-products"),
   path('add-to-cart/', views.add_to_cart, name="add-to-cart"),
   path('cart/', views.cart_view, name="cart"),
   path('delete-from-cart/', views.delete_item_from_cart, name="delete-from-cart"),
   path('update-from-cart/', views.update_item_from_cart, name="update-from-cart"),
   path('checkout/<oid>/', views.checkout, name="checkout"),
   
   path('save-checkout-info/', views.save_checkout_infor, name="save-checkout-infor"),
   #paypal integration
   path('paypal/', include('paypal.standard.ipn.urls')),
   
   #thanh toan
   path('payment-completed/<oid>/', views.payment_completed_view, name="payment-completed"),
   path('payment-failed/', views.payment_failed_view, name="payment-failed"),
   path('dashboard/', views.dashboard_view, name="dashboard"),
   path('dashboard/order/<int:id>/', views.order_detail, name="order-detail"),
   path('make-default-address/', views.make_address_default, name="make-default-address"),
   path('wishlist/', views.wishlist_view, name="wishlist"),
   path('add-to-wishlist/', views.add_to_wishlist, name="add-to-wishlist"),
   path('remove-from-wishlist/', views.remove_wishlist, name="remove-from-wishlist"),
   path('contact/', views.contact, name="contact"),
   path('ajax-contact-form/', views.ajax_contact, name="contact-form")
   
]
