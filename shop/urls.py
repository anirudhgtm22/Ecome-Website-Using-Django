from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="ShopHome"),
    path('about/',views.about,name="Aboutus"),
    path('contact/',views.contact,name="Contactus"),
    path('tracker',views.tracker,name="Tracker"),
    path('productview',views.productview,name="ProductView"),
    path('search',views.search,name="Search"),
    path('checkout',views.checkout,name="checkout"),
    path('cakes',views.cakes,name="cakes"),
    path('login/',views.login2,name="login"),
    path('signup/',views.signup,name="signup"),
    path('signin/',views.signin,name="signin"),
    path('success/',views.success,name="success"),
    path('logout/', views.logout_view, name='logout'),
    path('go_cart/', views.go_cart, name='Cart2'),
    path('check-out/', views.check_out, name='Check-out'),
    path('orders_placed/', views.orders_placed, name='orders_placed'),
]