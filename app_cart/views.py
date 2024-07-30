from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from app_store.models import Product,Variation
from .models import Cart,CartItem
from app_admin_account.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
#get the session id for cart
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id= product_id)
    #if the user is logged in
    if current_user.is_authenticated:
        product_variation = []
        if request.method=='POST':
            #get the quantity from product details
            quantity = int(request.POST['quantity'])
            for item in request.POST:
                key = item
                value = request.POST[key]
                #get the selected product variation and append it into empty product_variation array
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key,variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
        #adding cart item
        #is the cart item already into the cart
        is_cart_item_exists = CartItem.objects.filter(product= product, user= current_user).exists()
        # if the cart_item already existy in cart
        if is_cart_item_exists:
            cart_item=CartItem.objects.filter(product=product,user= current_user)
            #existing variation
            #current variation
            #item_id
            ex_var_list = []
            id = []
            #if the cart_item variation doesnot exist in cart just added the variation in ex_var_list
            for item in cart_item:
                existing_variation  = item.variation.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            #if the cart item variation already exist in the cart
            if product_variation in ex_var_list:
                #increase cart quantity
                index=ex_var_list.index(product_variation)
                item_id=id[index]
                item=CartItem.objects.get(product=product,id=item_id)
                item.quantity += quantity
                item.save()

            #if the cart item variation doesn't exist in the cart
            else:
                item = CartItem.objects.create(product=product, quantity=quantity, user= current_user)
                #add variation
                if len(product_variation) >0: #add variation
                    item.variation.clear() #add variation
                    #add variation
                    item.variation.add(*product_variation) #add variation
                
                #cart_item.quantity +=1#add cart
                item.save()#add cart
        #is the cart item isnot into the cart
        else:
            cart_item= CartItem.objects.create(
                product= product,
                quantity= quantity,
                user= current_user
            )
            #add variation
            if len(product_variation) >0: 
                cart_item.variation.clear()
            
                cart_item.variation.add(*product_variation) #add variation
            cart_item.save()
            messages.success(request, "Product added into the Cart")
        return redirect('cart')
    
    #if the user is not authenticated
    else:
        product_variation = []
        if request.method == 'POST':
            quantity = int(request.POST['quantity'])
            for item in request.POST:   #get the item and its value
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product = product, variation_category__iexact=key, variation_value__iexact= value)# iexact means value or key can be capital or small letter
                    product_variation.append(variation)
                except:
                    pass                        
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request) )  # get the cart using the cart id present in session

        except Cart.DoesNotExist:
            cart =  Cart.objects.create(
                cart_id =_cart_id(request)
            )
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product= product, cart= cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product = product,cart=cart)
            #existing variation->database
            #current variation ->product_variation
            #item_id->database
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variation.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            print(ex_var_list)
            
            if product_variation in ex_var_list:
                #increase quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product= product, id = item_id)
                item.quantity += quantity
                item.save()

            else:
                # create new cart item
                item = CartItem.objects.create(product = product, quantity= quantity, cart= cart)
                if len(product_variation) > 0:
                    item.variation.clear()
                    item.variation.add(*product_variation)
            #cart_item.quantity +=1 #cart_item.quantity = cart_item.quantity +1
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = quantity,
                cart = cart,
            )
            if len(product_variation) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
            cart_item.save()
        return redirect("cart")

#increase the cart

def increase_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id = product_id)
    try:
        if request.user.is_authenticated:
            cart_item=CartItem.objects.get(product=product,user= request.user,id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_item = CartItem.objects.get(product = product, cart=cart, id = cart_item_id)
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.info(request,"item is not available")
    except:
        pass

    return redirect("cart")


# decrement the cartr
def remove_cart(request,product_id, cart_item_id):
    product = get_object_or_404(Product, id = product_id)
    try:
        if request.user.is_authenticated:
            cart_item=CartItem.objects.get(product=product,user=request.user,id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_item = CartItem.objects.get(product = product, cart=cart, id = cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

#delete the cart
def delete_cart(request,product_id, cart_item_id):
    product=get_object_or_404(Product,id=product_id)
    if request.user.is_authenticated:
            cart_item=CartItem.objects.get(product=product,user=request.user,id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_item = CartItem.objects.get(product = product, cart=cart, id = cart_item_id)
    cart_item.delete()
    return redirect('cart')


def all_cart(request, total=0, quantity=0, cart_items = None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,is_active=True)
            
        else:
            cart = Cart.objects.get(cart_id =_cart_id(request))
            cart_items = CartItem.objects.filter(cart = cart , is_active=True)
        for cart_item in cart_items:
            total += (cart_item.discout_prices() * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore
    return render(request,"app_cart/cart.html",{
        "total" :round(total,2),
        "quantity" : quantity,
        "cart_items" :cart_items ,
        "tax" :round(tax,2),
        "grand_total" : round(grand_total, 2),
    })

#Checkout
@login_required(login_url='login')
def checkout(request, total= 0, quantity= 0, cart_items= None):
    current_user = request.user
    #userprofile = get_object_or_404(UserProfile, user = current_user)
    try:
        tax= 0
        grand_total= 0
        if current_user.is_authenticated:
            cart_items = CartItem.objects.filter(user= current_user, is_active= True)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.discout_prices() * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore
    return render(request,"app_cart/checkout.html",{
        "total" :round(total,2),
        "quantity" : quantity,
        "cart_items" :cart_items ,
        "tax" :round(tax,2),
        "grand_total" : round(grand_total, 2),
        #"userprofile" : userprofile
    })


