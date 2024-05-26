from django.contrib import admin
from ecapp.models import Product,UserProfile,Wishlist,Cart,PurchasedProduct,Contact_us,OrderDetails,PaymentDetails,Product_history,Rating
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Product)
admin.site.register(Wishlist)
admin.site.register(Cart)
admin.site.register(PurchasedProduct)
admin.site.register(Contact_us)
admin.site.register(OrderDetails)
admin.site.register(PaymentDetails)
admin.site.register(Product_history)
admin.site.register(Rating)