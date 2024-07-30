import datetime
from app_store.models import Product
from app_admin_account.models import Account,UserProfile
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Order,Payment,OrderProduct
from django.shortcuts import get_object_or_404, redirect, render
from app_cart.models import CartItem
from .forms import OrderForm
from django.contrib import messages
import uuid
# Varification email
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

import json
# Create your views here.



def palce_order(request,total=0):
    cart_items = CartItem.objects.filter(user= request.user)
    cart_count = cart_items.count()
    if cart_count <=0:
        return redirect("store")
    grand_total = 0
    tax = 0

    for item in  cart_items:
        total += item.discout_prices() * item.quantity
    tax = (2 * total)/100
    grand_total = total + tax
    if request.method=='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            print('valid')
            data = Order()
            data.user = request.user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone_number = form.cleaned_data['phone_number']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            ## generate_order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            order=Order.objects.get(user=request.user,is_ordered=False,order_number=order_number)
           
            return render(request,'app_order/order.html',{
                'order':order,
                'cart_items':cart_items,
                'total':round(total, 2),
                'tax':tax,
                'grand_total':round(grand_total, 2),
                
            })
    else:
        return redirect('checkout')
    
    #COD payment

def payment(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        payment_method = request.POST.get('payment_method')

        order = Order.objects.get(user=request.user, is_ordered=False, order_number=order_id)

        if payment_method == 'COD':
            # Generate a unique transaction ID
            transaction_id = 'COD-' + str(uuid.uuid4())
            payment = Payment(
                user=request.user,
                payment_id=transaction_id,
                payment_method='COD',
                amount_to_pay=order.order_total,
                status='pending'
            )
            payment.save()
            order.cash_payment = payment
            order.is_ordered = True
            order.save()

            # Move the cart items to order products
            cart_items = CartItem.objects.filter(user=request.user)
            for item in cart_items:
                order_product = OrderProduct()
                order_product.order_id = order.id
                order_product.payment = payment
                order_product.user_id = request.user.id
                order_product.product_id = item.product_id
                order_product.quantity = item.quantity
                order_product.product_price = item.discout_prices()
                order_product.ordered = True
                order_product.save()

                # Add variations to the order product
                product_variations = item.variation.all()
                order_product.variations.set(product_variations)
                order_product.save()

                # Reduce the stock
                product = Product.objects.get(id=item.product_id)
                product.stock -= item.quantity
                product.save()

            # Clear the cart
            CartItem.objects.filter(user=request.user).delete()

            #send order  recieved email to customer
            mail_subject = 'Thank You for Your Order!'
            message = render_to_string('app_order/order_recieved_email.html', {
                'user': request.user,
                'order':order
                
                })
            to_email = request.user.email
            send_mail = EmailMessage(mail_subject, message, to=[to_email])
            send_mail.send()

            # Redirect to order_complete with order_number and transaction_id
            return HttpResponseRedirect(reverse('order_complete') + f'?order_number={order.order_number}&payment_id={payment.payment_id}')

    return JsonResponse({'error': 'Invalid request'}, status=400)





def paypal_payment(request):
    body=json.loads(request.body)
    order=Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])
    #store all details which is collect from payment.html in script
    payment=Payment(
            user=request.user,
            payment_id=body['transId'],
            payment_method=body['payment_method'],
            amount_paid=order.order_total,
            status=body['status']

    )
    payment.save()
    order.payment=payment
    order.is_ordered =True
    order.save()

    # move the cart items in order product
    cart_items=CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct=OrderProduct()
        orderproduct.order_id=order.id
        orderproduct.payment=payment
        orderproduct.user_id=request.user.id
        orderproduct.product_id=item.product_id
        orderproduct.quantity=item.quantity
        orderproduct.product_price=item.product.price
        orderproduct.ordered=True
        orderproduct.save()

        #add variation or store variation

        cart_item=CartItem.objects.get(id=item.id)
        product_variation=cart_item.variations.all()
        orderproduct=OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()
        

        # Reduce he quantity of the stock products
        product=Product.objects.get(id=item.product_id)
        product.stock-=item.quantity
        product.save()


    #Clear cart
    CartItem.objects.filter(user=request.user).delete()


    #send order  recieved email to customer
    mail_subject = 'Thank You for Your Order!'
    message = render_to_string('app_order/order_recieved_email.html', {
        'user': request.user,
        'order':order
        
        })
    to_email = request.user.email
    send_mail = EmailMessage(mail_subject, message, to=[to_email])
    send_mail.send()


    #send order number and transection id backto send data via json response
        #send order number and transection id backto send data via json response
    data ={
        'order_number':order.order_number,
        'transId':payment.payment_id,
    }
    return JsonResponse(data)


def order_complete(request):
    #get order number transection if from js by json
    order_number=request.GET.get('order_number')
    transId=request.GET.get('payment_id')

    try:
        order=Order.objects.get(order_number=order_number,is_ordered=True)
        order_product=OrderProduct.objects.filter(order_id=order.id)
        

        sub_total=0
        grand_total = 0
        for i in order_product:
            sub_total +=(i.product_price * i.quantity)
        grand_total = order.tax + sub_total
            

        payment=Payment.objects.get(payment_id=transId)

        context ={
            'order':order,
            'order_product':order_product,
            'order_number':order.order_number,
            'transId':payment.payment_id,
            'payment':payment,
            'sub_total':sub_total,
            'grand_total':grand_total
        }

        return render(request,'app_order/order_complete.html' , context)
    except (Payment.DoesNotExist,Order.DoesNotExist):
        return redirect('home')

    return render(request,"app_order/order_complete.html")
    
    

    



