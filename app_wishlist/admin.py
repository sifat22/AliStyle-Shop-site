from django.contrib import admin
from .models import Wishlist,WishlistItem

# Register your models here.


class WishlistAdmin(admin.ModelAdmin):
    list_display = ('wishlist_id',)

class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('product','wishlist',)

admin.site.register(Wishlist,WishlistAdmin)
admin.site.register(WishlistItem,WishlistItemAdmin)
