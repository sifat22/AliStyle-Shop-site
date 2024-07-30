from django.urls import path
from . import views

urlpatterns = [
    path("",views.wishlist,name="wishlist"),
    path("add_wishlist/<int:product_id>/",views.add_wishlist,name="add_wishlist"),
    #for in_cart
    #path("add_wishlist/<slug:product_slug>/dgvfgehvf",views.product_in_wishlist,name="in_wishlist"),
    path("delete_wishlist/<int:product_id>/",views.delete_wishlist,name="delete_wishlist"),
]

