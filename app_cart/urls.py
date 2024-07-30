from django.urls import path
from . import views



urlpatterns = [
    path("",views.all_cart,name="cart"),
    path("add_cart/<int:product_id>/",views.add_cart,name="add_cart"),
    path("increase_cart/<int:product_id>/<int:cart_item_id>/",views.increase_cart,name="increase_cart"),
    path("decrease_cart/<int:product_id>/<int:cart_item_id>/",views.remove_cart,name="decrease_cart"),
    path("delete_cart/<int:product_id>/<int:cart_item_id>/",views.delete_cart,name="delete_cart"),

    #Checkout
    path("checkout/", views.checkout,name="checkout")
]

