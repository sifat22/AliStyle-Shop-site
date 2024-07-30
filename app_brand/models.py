from django.db import models
from django.urls import reverse
from app_admin_account.models import Account


# Create your models here.


class Brand(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    brand_name = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(unique=True)


    def get_url(self):
        return reverse("products_by_brand", args =[self.slug])
    
    def has_perm(self, perm, obj=None):
        return self.user.is_admin
    
    def has_module_perms(self, add_label):
        return True




    def __str__(self):
        return self.brand_name
    

