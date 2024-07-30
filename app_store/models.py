from django.db import models
from app_brand.models import Brand
from app_category.models import Category
from django.urls import reverse
from django.contrib.auth.models import User
from app_admin_account.models import Account
from django.db.models.aggregates import Avg, Count

# Create your models here.


class Product(models.Model):
    product_name = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="photos/app_product",blank=True)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    stock = models.IntegerField()
    import_from = models.CharField(max_length=200)
    price = models.IntegerField()
    manufacture = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True)
    offers = models.BooleanField(default=False)
    warrenty = models.IntegerField(blank=True,null=True)
    offer_precentage = models.IntegerField(blank=True,null=True)
    delivery_time = models.CharField(max_length=200,blank=True)
    img1 = models.ImageField(upload_to="photos/app_product",blank=True)
    img2 = models.ImageField(upload_to="photos/app_product",blank=True)
    img3 = models.ImageField(upload_to="photos/app_product",blank=True)
    img4 = models.ImageField(upload_to="photos/app_product",blank=True)
    desc = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    def get_url(self):
        return reverse('product_details', args=[self.brand.slug, self.category.slug, self.slug])
    


    def __str__(self):
        return self.product_name
    
    def staff_permission(self,user_id):
        user = User.objects.get(id= user_id)
        if user.is_staff==True and user.is_superadmin==True:
            return user
    
        #get average review
    def averagereview(self):
        review=Review.objects.filter(product=self,status=True).aggregate(average=Avg('rating'))
        avg=0
        if review['average'] is not None:
            avg=float(review['average'])
        return avg

    


 #variation manager will help us to diplay the color and size differently
class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category = "color" ,is_active = True)
    def sizes(self):
        return super(VariationManager, self).filter(variation_category = "size" ,is_active = True)



#Drop down the variation choices
variation_category_choices = (
    ('color', 'color'),
    ('size', 'size'),
    
)


#For Variation add

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=255, choices= variation_category_choices)
    variation_value = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = VariationManager()


    def __str__(self):
        return self.variation_value
    

class Review(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    subject=models.CharField(max_length=100,blank=True)
    review=models.TextField(max_length=500,blank=True)
    rating=models.FloatField()
    admin_reply = models.TextField(max_length=500,blank=True)
    ip=models.CharField(max_length=20,null=True)
    status=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
    

    

    
