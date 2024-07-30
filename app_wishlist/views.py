from django.shortcuts import render,redirect,get_object_or_404
from .models import WishlistItem,Wishlist
from app_store.models import Product
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


# Create your views here.

def _wishlist_id(request):
    wishlist = request.session.session_key
    if not wishlist:
        wishlist = request.session.create()
    return wishlist


# I add this because in the store.views i make a query in wishlist weher I want to show in store page that the item alerady exist or not in the wishlist

# def product_in_wishlist(request,product_slug):
#     try:
        
#         single_product = get_object_or_404(Product, slug = product_slug)
#     except Exception as e:
#         raise e
#     return single_product


def add_wishlist(request, product_id):
    current_user = request.user
    product = Product.objects.get(id = product_id)
    #if user is logged in
    if current_user.is_authenticated:
        wishlist_item = []
        if request.method == 'POST':
            if WishlistItem.objects.filter(product = product, user = current_user):
                messages.info(request, "Item already added in wishlist")
                return redirect("wishlist")
            else:
                wishlist_item = WishlistItem.objects.create(
                    product = product,
                    user = current_user
                )
            wishlist_item.save()
            messages.success(request, "Item added in Wishlist")
        return redirect("wishlist")
    #if user is not authenticated
    else:
        wishlist_item = []
        if request.method=='POST':
            try:
                wishlist = Wishlist.objects.get(wishlist_id = _wishlist_id(request))
            except Wishlist.DoesNotExist:
                wishlist =  Wishlist.objects.create(
                    wishlist_id = _wishlist_id(request)
                )
            wishlist.save()

            if WishlistItem.objects.filter(wishlist = wishlist, product = product).exists():
                messages.info(request, "Item already added in wishlist")
                return redirect("wishlist")
            else:
                wishlist_item = WishlistItem.objects.create(
                    product = product,
                    wishlist = wishlist
                )
            wishlist_item.save()
            messages.success(request, "Item added in Wishlist")
        return redirect("wishlist")


def delete_wishlist(request, product_id):
    product = get_object_or_404(Product, id = product_id)
    if request.user.is_authenticated:
        wishlist_item = WishlistItem.objects.get(product = product, user = request.user)
    else:
        wishlist = Wishlist.objects.get(wishlist_id = _wishlist_id(request))
        wishlist_item = WishlistItem.objects.get(product = product, wishlist=wishlist)
    wishlist_item.delete()
    return redirect("wishlist")




def wishlist(request):
    try:
        if request.user.is_authenticated:
                wishlist_item=WishlistItem.objects.filter(user=request.user,is_active=True)
        else:
            wishlist = Wishlist.objects.get(wishlist_id = _wishlist_id(request))
            wishlist_item = WishlistItem.objects.filter(wishlist = wishlist, is_active = True)
    except ObjectDoesNotExist:
        pass
    return render(request,"app_wishlist/wishlist.html",{
        "wishlist_item" : wishlist_item

    })
