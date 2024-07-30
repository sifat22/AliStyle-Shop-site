from django.db import models
from app_store.models import Product
from app_admin_account.models import Account

# Create your models here.


class Wishlist(models.Model):
    wishlist_id = models.CharField(max_length=255,blank=True)
    Date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.wishlist_id
    

class WishlistItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    wishlist = models.ForeignKey(Wishlist,on_delete=models.CASCADE,null=True)
    is_active = models.BooleanField(default=True)


    def __unicode__(self):
        return self.product
