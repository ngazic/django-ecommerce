from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from my_store.models import Product, Variation
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
        
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            print(item, request.POST[item])
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=item, variation_value__iexact=request.POST[item])
                product_variation.append(variation)
            except:
                pass
    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
    
    if is_cart_item_exists:
        cart_items = CartItem.objects.filter(product=product, cart=cart)
        
        existing_variation_list = []
        items_id = []
        for item in cart_items:
            existing_variation = item.variations.all()
            existing_variation_list.append(list(existing_variation))
            items_id.append(item.id)
        # if variation for product already exists, increase it, else create new
        if (product_variation in existing_variation_list) or (product_variation[: :-1] in existing_variation_list):
            index = existing_variation_list.index(product_variation) if product_variation in existing_variation_list else existing_variation_list.index(product_variation[::-1])
            item_id = items_id[index]
            item = CartItem.objects.get(product=product, id = item_id)
            item.quantity += 1
            item.save()
        else:
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:
                item.variations.add(*product_variation)
            item.save()
            
    else:
        cart_item =CartItem.objects.create(
            cart=cart,
            quantity=1,
            product=product
        )
        if len(product_variation) > 0:
            cart_item.variations.clear()
            for item in product_variation:
                cart_item.variations.add(item)
                
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
        