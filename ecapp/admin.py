from django.contrib import admin
from ecapp.models import Product,UserProfile,Wishlist,Cart,PurchasedProduct,Contact_us,OrderDetails,PaymentDetails
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Product)
admin.site.register(Wishlist)
admin.site.register(Cart)
admin.site.register(PurchasedProduct)
admin.site.register(Contact_us)
admin.site.register(OrderDetails)
admin.site.register(PaymentDetails)