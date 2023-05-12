from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, PROTECT
from django.core.validators import MinLengthValidator,MaxLengthValidator

# Create your models here.
def product_directory_path(instance, filename):
    return f"products/product_{instance.productID}/{filename}"
    
class Product(models.Model):
    # categories=[
    #     ('Gifting',(
    #         ('Hand painted bookmark','Hand painted bookmark'),
    #         ('Hand painted bottle lamp with cork light','Hand painted bottle lamp with cork light'),
    #         ('Hand painted teracota diya','Hand painted teracota diya'),
    #         ('Hand painted jwellary box','Hand painted jwellary box'),
    #         ('Hand painted decorative trunk','Hand painted decorative trunk')
    #     )),
    #     ('Home utility',(
    #         ('Handpainted name plated','Handpainted name plated'),
    #         ('Handpainted key holder','Handpainted key holder'),
    #         ('Handpainted wooden tray','Handpainted wooden tray'),
    #         ('Handpainted cups','Handpainted cups'),
    #         ('Handpainted glass bottles','Handpainted glass bottles'),
    #         ('Handpainted furnitures','Handpainted furnitures'),
    #         ('Hand painted jwellary box','Hand painted jwellary box'),
    #     )),
    #     ('Home decor',(
    #         ('Handpainted magnets','Handpainted magnets'),
    #         ('Handpainted traditional painting','Handpainted traditional painting'),
    #         ('Handpainted teracota diya','Handpainted teracota diya'),
    #         ('Handpainted decorative trunk','Handpainted decorative trunk'),
    #     ))
    # ]
    categories=[("Madhubani painting","Madhubani painting"),("Bottle arts","Bottle arts"),("Name plates","Name plates"),("Wall plates","Wall plates")]
    # featuredin = models.CharField(max_length=30,choices=[('none','none'),('featured','featured'),('traditional art','traditional art'),('madhubani art','madhubani art'),('pichwai art','pichwai art')],default='none')
    productID = models.CharField(max_length=10,unique=True,primary_key=True)
    name =models.CharField(max_length=100)
    description = models.TextField()
    image = models.FileField(upload_to=product_directory_path)
    price = models.IntegerField()
    discount = models.IntegerField()
    category = models.CharField(
        max_length=100,
        choices=categories,
        default='Hand painted bookmark'
    )
    size=models.CharField(max_length=40)
    materials=models.CharField(max_length=100)
    soldcount = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)
    outofstock = models.BooleanField(default=False)


    def __str__(self) -> str:
        return self.name

def user_directory_path(instance, filename):
    return f"users/user_{instance.userz.username}/{filename}"



class UserProfile(models.Model):
    userz = models.OneToOneField(User, on_delete=CASCADE)
    contactnumber = models.IntegerField()
    dateofbirth = models.DateField(auto_now=False, auto_now_add=False)
    address = models.CharField(max_length=100,default="nowhere")
    gender = models.CharField(max_length=20,choices=[('male','male'),('female','female'),('other','other')],default='male')
    profilePhoto = models.FileField(upload_to=user_directory_path)
    verified = models.BooleanField(default=False)
    verifycode = models.CharField(max_length=20,default="none")

    def __str__(self):
        return str(self.userz.username)
    
class PaymentDetails(models.Model):
    paymentid = models.CharField(max_length=20,default="none",unique=True,primary_key=True)
    transactionid = models.CharField(max_length=20,default="none")
    paymentstatus = models.BooleanField(default=False)
    modeofpayment = models.CharField(max_length=20,choices=[('card','debit/creditcard'),('net','net banking'),('upi','upi'),('cod','cash on delivery')],default='cod')

    
class OrderDetails(models.Model):
    orderid = models.CharField(max_length=20,unique=True,primary_key=True)
    purchaser = models.ForeignKey(User,on_delete=PROTECT)
    nameonpurchase = models.CharField(max_length=40,default="none")
    paymentid = models.ForeignKey(PaymentDetails,on_delete=PROTECT)
    dateofpurchase = models.DateField(auto_now=False, auto_now_add=False)
    address = models.CharField(max_length=200,default="nowhere")
    pincode = models.IntegerField(default=000000)
    status = models.CharField(max_length=20,choices=[('placed','placed'),('shipped','shipped'),('delivered','delivered')],default='placed')
    phone = models.IntegerField()
    amount = models.IntegerField(default=0)


class PurchasedProduct(models.Model):
    purchasedprodid = models.CharField(max_length=20,primary_key=True,default="none")
    orderid = models.ForeignKey(OrderDetails,on_delete=PROTECT)
    product = models.ForeignKey(Product,on_delete=PROTECT)
    quantity = models.IntegerField()
    price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.product.productID
    

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=PROTECT)
    product = models.ForeignKey(Product,on_delete=PROTECT)
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return self.product.name

class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=PROTECT)
    product = models.ForeignKey(Product,on_delete=PROTECT)

    def __str__(self) -> str:
        return self.product.name


class Contact_us(models.Model):
    name = models.CharField(max_length=20)
    emailid = models.EmailField()
    contactnumber = models.IntegerField()
    subjecttocontact = models.TextField()
    desc = models.TextField()
    dateofcontact = models.DateTimeField()

    def __str__(self):
        return self.subjecttocontact