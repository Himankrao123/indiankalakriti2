from django.urls import path
from ecapp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.loginacc, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/',views.logoutacc,name="logout"),
    path('profile/',views.profile,name="profile"),
    path('editprofile/',views.editprofile,name="editprofile"),
    path('contact_us/',views.contactus,name="contactus"),
    path('store/<slug:slug>',views.store,name="store"),
    path('product/<slug:slug>',views.product,name="product"),
    path('buyproduct/<slug:slug>',views.buyproduct,name="buyproduct"),
    path('buycart',views.buycart,name="buycart"),
    path('wishlist/', views.wishlist, name="wishlist"),
    path('cart/', views.mycart, name="mycart"),
    path('orders/', views.myorders, name="myorders"),
    path('order/<slug:slug>', views.order, name="order"),
    path('api/<slug:slug>',views.apicalls,name="apicall")
] +static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)