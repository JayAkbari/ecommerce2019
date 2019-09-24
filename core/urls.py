from django.urls import path
from .views import item_list, checkout, product, HomeView, ItemDetailView, OrderSummaryView, add_to_cart,remove_from_cart,remove_single_from_cart

app_name = 'core'
urlpatterns = [
    path('', HomeView.as_view(), name='item-list'),
    path('checkout/', checkout, name='checkoutpage'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='productpage'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-single-from-cart/<slug>/', remove_single_from_cart, name='remove-single-from-cart'),
    


]
