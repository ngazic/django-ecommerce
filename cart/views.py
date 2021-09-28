from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import Product
from cart.models import Cart, CartItem

# Create your views here.

# return session by id, 
# or create new one if doesn't exist

def _session_id(request):
    session = request.session.session_key
    if not session:
        session = request.session.create()
    return session


def cart(request, total=0, quantity=0,cart_items=None):
    tax = 0
    try:
        cart = Cart.objects.get(cart_id=_session_id(request))
        cart_items = cart.cart_items.all()
        for cart_item in cart_items:
            total += cart_item.sub_total()
            quantity += cart_item.quantity
        tax = round(0.17 * total)
    except:
        pass #just igore bacause we have default values from kwargs of function
    
    context = {
        'total': total,
        'quantity': quantity,
        'items': cart_items,
        'tax': tax,
        'grand_total': total + tax
    }
    return render(request, 'store/cart.html', context)


def add_cart_item(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except:
        return HttpResponse('No such product')
    
    try:
        cart = Cart.objects.get(cart_id=_session_id(request)) 
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = _session_id(request))
        cart.save()
        
    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
    
    if is_cart_item_exists:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    else:
        cart_item =CartItem.objects.create(
            cart=cart,
            quantity=1,
            product=product
        )
        cart_item.save()

    return redirect('cart')


def remove_cart_item(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id)
    except:
        return HttpResponse('Invalid cart item')
    else:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    
    return redirect('cart')
        

def remove_cart_product(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id)
    except:
        return HttpResponse('Invalid cart item')
    else:
        cart_item.delete()
    
    return redirect('cart')
        