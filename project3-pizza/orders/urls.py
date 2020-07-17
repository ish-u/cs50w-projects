from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/",views.register, name="register"),
    path("pizza_order/",views.pizza_order, name="pizza_order"),
    path("sub_order/",views.sub_order, name="sub_order"),
    path("pasta_order/",views.pasta_order, name="pasta_order"),
    path("salad_order/",views.salad_order, name="salad_order"),
    path("platter_order/",views.platter_order, name="platter_order"),
    path("cart/",views.cart, name="cart"),
    path("special/",views.special, name="special"),
    path("order/",views.Order, name="order"),
    path("cart/delete_pizza/",views.delete_pizza, name="delete_pizza"),
    path("cart/delete_sub/",views.delete_sub, name="delete_sub"),
    path("cart/delete_pasta/",views.delete_pasta, name="delete_pasta"),
    path("cart/delete_salad/",views.delete_salad, name="delete_salad"),
    path("cart/delete_platter/",views.delete_platter, name="delete_platter"),
    path("order_complete/",views.order_complete, name="order_complete"),
]
