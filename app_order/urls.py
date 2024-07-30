from django.urls import path
from .import views

urlpatterns = [
    path("place_order/", views.palce_order, name='place_order'),
    path("process_payment/",views.payment,name="process_payment"),
    path("process_payment/",views.paypal_payment,name="process_payment_paypal"),
    path('order_complete/',views.order_complete,name='order_complete'),

    # path('payment/create/', views.payment, name='payment'),
    # path('payment/execute/', views.execute_payment, name='execute_payment'),
    

]