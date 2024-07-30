from django.db import models
from app_brand.models import Brand
from django.urls import reverse


# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="photos/app_category")
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,null=True)
    is_trending = models.BooleanField(default=True)
    is_popular = models.BooleanField(default=True)


    class Meta:
        verbose_name ='category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse("products_by_b_c", args =[self.brand.slug, self.slug])



    def __str__(self):
        return self.category_name
