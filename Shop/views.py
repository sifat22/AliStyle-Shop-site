from django.http import HttpResponse
from django.shortcuts import render
from app_store.models import Product


def home(request):
    all_product = Product.objects.all().order_by("-modified_date")[:8]
    offer_product = Product.objects.filter(offers = True)[:5]
    product_by_brand = Product.objects.filter(brand__brand_name = "Electronics and Tech")
    return render(request,"home.html",{
        "all_product" : all_product,
        "offer_product" : offer_product,
        "product_by_brand" : product_by_brand,
    })