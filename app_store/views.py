from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from.models import Product,Review
from app_brand.models import Brand
from app_category.models import Category
from django.db.models import Sum
from app_wishlist.views import _wishlist_id
from .forms import ReviewForm
from app_wishlist.models import WishlistItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.


def store(request, brand_slug=None, category_slug=None):
    products = None
    categories = None
    brands = None
    # in_wishlist = None
    
    if category_slug:
        categories = get_object_or_404(Category, slug = category_slug)
        brands = get_object_or_404(Brand, slug = brand_slug)
        products = Product.objects.filter(category = categories, is_available= True)
        cat_by_brand = Category.objects.filter(brand = brands)

        product_count = products.count()

    elif brand_slug:
        brands = get_object_or_404(Brand, slug = brand_slug)
        products = Product.objects.filter(brand = brands, is_available= True)
        cat_by_brand = Category.objects.filter(brand = brands)
        product_count = products.count()

    # elif brand_slug and brand_slug:
    #     brands = get_object_or_404(Brand, slug = brand_slug)
    #     categories = get_object_or_404(Category, slug = category_slug)
    #     products = Product.objects.filter(brand = brands, category = categories, is_available= True)
    #     product_count = products.count()

    else:
        products = Product.objects.all().filter(is_available=True).order_by("-modified_date")
        cat_by_brand = Category.objects.all()[:0]
        product_count = products.count()

    # try:
    #     #single_product = Product.objects.all().filter(is_available=True).order_by("-modified_date")
    #     product = request.product_slug
    #     in_wishlist = WishlistItem.objects.filter(wishlist__wishlist_id = _wishlist_id(request), product =product).exists()
    # except:
    #     pass
    
        



    return render(request,"app_store/store.html",{
        "products" : products,
        "product_count" : product_count,
        "cat_by_brand" : cat_by_brand,
        #"in_wishlist" : in_wishlist,
        # "product_slug" : product_slug
       

    })




def product_details(request, brand_slug, category_slug, product_slug):
    total_stock = 0
    try:
        product_detail = get_object_or_404(Product, brand__slug = brand_slug, category__slug = category_slug, slug = product_slug)
        total_stock = product_detail.stock

    except Exception as e:
        raise e
    #get the reveiws product
    reviews=Review.objects.filter(product_id=product_detail.id,status=True)
    review_count = reviews.count()
    return render(request,"app_store/product_details.html",{
        "product_detail" : product_detail,
        "total_stock" : total_stock,
        #"is_reviewd" : is_reviewd
        "review_count" : review_count,
        "reviews" : reviews


        
    })



#submit Review
def submit_review(request, brand_id, category_id, product_id):
    #is_reviewd = Review.objects.filter(user__id=request.user.id).exists()
    url=request.META.get('HTTP_REFERER')
    if request.method=='POST':
        try:
            reviews=Review.objects.get(user__id=request.user.id,product__id=product_id)
            form=ReviewForm(request.POST,instance=reviews) # for instance it will update the review if we dont use it it will create a new one
            form.save()
            messages.success(request,'Thank You ! your review has been updated !')
            return redirect(url)
        except Review.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                print('valid')
                data= Review()
                data.subject= form.cleaned_data['subject']
                data.rating= form.cleaned_data['rating']
                data.review= form.cleaned_data['review']
                data.ip= request.META.get('REMOTE_ADDR') 
                data.product_id= product_id
                data.user_id=request.user.id
                data.save()
                messages.success(request,'Thank You ! your review has been submitted !')
                return redirect(url)
        


        

    



    
    



    


    
    