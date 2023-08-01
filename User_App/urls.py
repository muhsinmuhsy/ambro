from django.urls import path
from User_App.views import *

urlpatterns = [
    path('', home, name='home'),
    path('product_view/<int:pk>/', product_view, name='product_view'),
    path('add_to_cart_one/<int:product_id>/', add_to_cart_one, name='add_to_cart_one'),
    path('add_to_cart_two/<int:product_id>/', add_to_cart_two, name='add_to_cart_two'),
    path('cart_items/', cart_items_view, name='cart_items_view'),
    # path('update_cart_item/<int:cart_item_id>/', update_cart_item, name='update_cart_item'),

    path('cart_item/increase/<int:item_id>/', increase_quantity, name='increase_quantity'),
    path('cart_item/decrease/<int:item_id>/', decrease_quantity, name='decrease_quantity'),

    path('checkout/', checkout, name='checkout'),
    path('order_confirmation/<int:order_id>/', order_confirmation, name='order_confirmation'),

    path('cart_item/delete/<int:item_id>/', delete_cart_item, name='delete_cart_item'),
    path('cart_items/delete_all/', delete_all_cart_items, name='delete_all_cart_items'),
]