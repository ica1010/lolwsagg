from django.contrib import admin
from .models import Cart, Cartitems
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display=('Cart_id', 'date_added')
    
class CartitemAdmin(admin.ModelAdmin):
    list_display=('product', 'Cart', 'quantity', 'is_active')

admin.site.register(Cart,CartAdmin)
admin.site.register(Cartitems,CartitemAdmin)
