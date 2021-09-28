from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_cart_item, name='add-cart-item'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_cart_item, name='remove-cart-item'),
    path('remove-cart-product/<int:cart_item_id>/', views.remove_cart_product, name='remove-cart-product'),
    # path('category/',views.store, name='store'),
    # path('category/<slug:category_slug>/',views.store, name='products_by_category'),
    # path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    # path('cart/', include('cart.urls'))
]
