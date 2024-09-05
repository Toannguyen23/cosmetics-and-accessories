from django.urls import path
from useradmin import views

app_name="useradmin"


urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("products/", views.product, name="products"),
    path("add-product/", views.add_product, name="add-product"),
    path("edit-product/<pid>/", views.edit_product, name="edit-product"),
    path("delete-product/<pid>/", views.delete_product, name="delete-product"),
    
]
