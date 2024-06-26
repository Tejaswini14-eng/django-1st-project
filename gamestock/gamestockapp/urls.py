from django.contrib import admin
from django.urls import path
from gamestockapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('products',views.createproduct),
    path('products/view',views.readproduct),
    path('products/details/<rid>',views.productDetails),
    path('products/view/update/<rid>',views.updateproduct),
    path('products/view/delete/<rid>',views.deleteproduct),
    path('register',views.userRegister),
    path('login',views.userLogin),
    path('logout',views.userLogout),
    path('users/view',views.readuser),
    path('users/view/update/<rid>',views.updateuser),
    path('add_to_cart/<rid>',views.add_to_cart),
    path('showcart',views.showcart),
    path('removecart/<rid>',views.removecart),
    path('cart/update/<cid>/<rid>',views.updatecart),
    path('add_to_order',views.add_to_order),
    path('orders',views.show_orders),
    path('add_review/<rid>',views.add_review),
    path('forgot_password',views.forgot_password),
    path('verify_otp' , views.verify_otp),
    path('change_password',views.change_password),
]

urlpatterns += static(settings.MEDIA_URL ,document_root = settings.MEDIA_ROOT)
