from . models import CartItem
from .views import _session_id

def cart_counter(request):
    item_number = 0
    if 'admin' in request.path:
        return {}
    else:
        cart_items = CartItem.objects.filter(cart__cart_id=_session_id(request))
        for item in cart_items:
            item_number += item.quantity
            
    return {'cart_count': item_number}
