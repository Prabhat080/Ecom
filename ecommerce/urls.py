from django.urls import path
from ecommerce import views

urlpatterns = [
    path('home',views.home,name="Home"),
    path('register',views.register,name="Register"),
    path('login',views.login,name="Login"),
    path('logout',views.logout,name="Logout"),
    path('productList',views.ListProduct,name="normal"),
    path('product/<int:pk>',views.product,name="test"),
    path('product/<str:category>',views.categoryView,name="CategoryView"),
    path('update_item',views.updItem),
    path('cart',views.cart,name='Cart'),
    path('upd_quantity',views.updQuantity),
    path('checkout',views.checkout,name='checkout'),
    path('online',views.online,name="Online"),
    path('fake-payment-api',views.fake_payment,name="fake-payment-api"),
    path('adminReg',views.registerAdmin),
    path('inventory',views.inventory,name='inventory'),
    path('adminView',views.adminView),
    path('updateCart',views.updateCart),
    path('orderHistory',views.orderHistory),
    path('updOrderHistory',views.updOrderHistory)
]