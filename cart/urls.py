from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_cart, name='add-cart'),
    # path('category/',views.store, name='store'),
    # path('category/<slug:category_slug>/',views.store, name='products_by_category'),
    # path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    # path('cart/', include('cart.urls'))
]
