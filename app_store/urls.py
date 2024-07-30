from django.urls import path
from . import views


urlpatterns = [
    path("",views.store,name="store"),
    path("<slug:brand_slug>/",views.store,name="products_by_brand"),
    path("<slug:category_slug>/",views.store,name="products_by_category"),
    path("<slug:brand_slug>/<slug:category_slug>/",views.store,name="products_by_b_c"),
    #path("<slug:brand_slug>/<slug:category_slug>/<slug:product_slug>",views.store,name="in_wishlist"),
    path("<slug:brand_slug>/<slug:category_slug>/<slug:product_slug>/",views.product_details,name="product_details"),
    #path("<slug:brand_slug>/<slug:category_slug>/<slug:product_slug>/",views.store,name="products_by_b_c_p"),
    # path("<slug:brand_slug>/<slug:category_slug>/<slug:product_slug>/",context_processor.product_links,name="product_details"),

    #for review
    path("submit_review/<int:brand_id>/<int:category_id>/<int:product_id>/",views.submit_review, name="submit_review"),
    #path("update_review/<int:brand_id>/<int:category_id>/<int:product_id>/",views.update_review, name="update_review")



    #review
    #path("review/<int:category_id>/<int:product_id>/",views.review,name="review")
    
]
