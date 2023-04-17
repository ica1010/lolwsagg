
from carts.models import Cart, Cartitems
from carts.views import _cart_id


def counter(request):
    cart_count=0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart= Cart.objects.filter(Cart_id=_cart_id(request))
            if request.user.is_authenticated:
                cart_items=Cartitems.objects.all().filter(user=request.user)
            else:
                cart_items=Cartitems.objects.all().filter(Cart=cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist :
            cart_count=0
    return dict(cart_count = cart_count)
               