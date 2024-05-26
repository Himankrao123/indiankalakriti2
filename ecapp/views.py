from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from ecapp.models import UserProfile,Contact_us,Product,Wishlist,Cart,PurchasedProduct,OrderDetails,PaymentDetails, Product_history, Rating
from django.db import transaction
import datetime
import random
import string

from django.conf import settings
from django.core.mail import send_mail

# Create your views here.

def index(request):
    trending_products = list(Product.objects.filter(outofstock=False).order_by("-trend_score","-soldcount")[:10].values("name","image","price","discount","productID"))
    for item in trending_products:
        item["discountedprice"] = int(item["price"]-item["price"]*item["discount"]/100)
    featured_products = list(Product.objects.filter(outofstock=False,featured=True).order_by("-soldcount")[:10].values("name","image","price","discount","productID"))
    for item in featured_products:
        item["discountedprice"] = int(item["price"]-item["price"]*item["discount"]/100)
    if request.user.is_anonymous:
        return render(request, 'index.html',{"template":"base.html","trending_products":trending_products,"featured_products":featured_products})
    recent_products = list(Product_history.objects.filter(user=request.user).order_by("-datetime"))
    recent_products = list(map(lambda x:x.product, recent_products))
    recent_products = recent_products[:10]
    recent_products = list(map(lambda x:{"name":x.name,"image":x.image,"price":x.price,"discount":x.discount,"productID":x.productID},recent_products))
    for item in recent_products:
        item["discountedprice"] = int(item["price"]-item["price"]*item["discount"]/100)
    return render(request,'userindex.html',{"template":"base2.html","trending_products":trending_products,"featured_products":featured_products,"recent_products":recent_products})

def contactus(request):
    if request.method == "POST":
        conname = request.POST.get('name')
        conemail = request.POST.get('email')
        connumber = request.POST.get('number')
        desc = request.POST.get('desc')
        dateofcon = datetime.datetime.today()
        subject = request.POST.get('subject')
        contactus = Contact_us(name = conname, emailid = conemail, desc = desc, dateofcontact = dateofcon,contactnumber = connumber,subjecttocontact = subject)
        contactus.save()
    if request.user.is_anonymous:
        return render(request, 'contact_us.html',{"template":"base.html"})
    return render(request,'contact_us.html',{"template":"base2.html"})

def loginacc(request):
    if request.method == "POST":
        ausername = request.POST.get("username")
        apassword = request.POST.get("password")
        if "@" and "." in ausername:
            if User.objects.filter(email=ausername).exists():
                ausername = User.objects.get(email=ausername).username
            else:
                message = {'what':'User does not exist'}
                return render(request, 'login.html',message)
        else:
            if User.objects.filter(username=ausername).exists():
                pass
            else:
                message = {'what':'User does not exist'}
                return render(request, 'login.html',message)
        if User.objects.get(username=ausername).is_active == False and UserProfile.objects.get(userz=User.objects.get(username=ausername)).verified == False:
            message = {'what':'Please check your email to verify your account'}
            return render(request, 'login.html',message)
        try:
            userserv = authenticate(request, username=ausername, password=apassword)
        except:
            message = {'what':'Invalid password!'}
            return render(request, 'login.html',message)
        if userserv is not None:
            login(request,userserv)
            return redirect('/')
        else:
            message = {"what":"Invalid password!"}
            return render(request, 'login.html', message)
    message = {"what":""}
    return render(request, 'login.html',message)

def signup(request):
    if request.method == "POST":
        try:
            print(request.POST)
            pphoto = request.FILES.get("pphoto")
            fname = request.POST.get("fname")
            lname = request.POST.get("lname")
            username = request.POST.get("username")
            password = request.POST.get("password")
            password2 = request.POST.get("password2")
            email = request.POST.get("email")
            contact = request.POST.get("contact")
            dob = request.POST.get("dob")
            gender = request.POST.get("gender")
            address = request.POST.get("address")
            char  = string.ascii_lowercase + string.digits
            a = ''.join(random.choice(char) for _ in range(20)) 
            while UserProfile.objects.filter(verifycode=a).exists():
                a = ''.join(random.choice(char) for _ in range(20))
            with transaction.atomic():
                if password == password2:
                    if User.objects.filter(username=username).exists():
                        message = {'what':'Username already exists. Please use another'}
                        return render(request, 'signup.html',message)
                    elif User.objects.filter(email=email).exists():
                        message = {'what':'Email already exists. Please use another'}
                        return render(request, 'signup.html',message)
                    else:
                        user = User.objects.create_user(username=username, password=password, email=email, first_name=fname, last_name=lname, is_active=True)
                        user.save()
                        userprofile = UserProfile(userz=user,contactnumber=contact, dateofbirth=dob,gender = gender,profilePhoto = pphoto, address = address,verifycode = a,verified = True)
                        userprofile.save()
                        return redirect("/login")
        except:
            message = {'what':'Something went wrong'}
            return render(request, 'signup.html',message)

        
    return render(request, 'signup.html')


def logoutacc(request):
    if request.user.is_anonymous:
        return redirect("/")
    logout(request)
    return redirect("/")

def profile(request):
    if request.user.is_anonymous:
        redirect("/login")
    u = User.objects.get(username = request.user)
    up = UserProfile.objects.get(userz=request.user)
    user = {'fname':u.first_name,'lname':u.last_name,'email':u.email,'username':u.username,'contactnumber':up.contactnumber,'gender':up.gender,'dob':up.dateofbirth,'profilephoto':up.profilePhoto,'address':up.address}
    return render(request,'profile.html',user)

def editprofile(request):
    if request.user.is_anonymous:
        return redirect("/login")
    if request.method == "POST":
        try:
            pphoto = request.FILES.get("pphoto")
            fname = request.POST.get("fname")
            lname = request.POST.get("lname")
            username = request.POST.get("username")
            email = request.POST.get("email")
            contact = request.POST.get("contact")
            dob = request.POST.get("dob")
            address = request.POST.get("address")
            u = User.objects.get(username = request.user)
            up = UserProfile.objects.get(userz=request.user)
            with transaction.atomic():
                if User.objects.filter(username=username).exists() and username != u.username:
                    message = {'what':'Username already exists. Please use another'}
                    return render(request, 'editprofile.html',message)
                elif User.objects.filter(email=email).exists() and email != u.email:
                    message = {'what':'Email already exists. Please use another'}
                    return render(request, 'editprofile.html',message)
                else:
                    u.username = username
                    u.email = email
                    u.first_name = fname
                    u.last_name = lname
                    u.save()
                    up.contactnumber = contact
                    up.dateofbirth = dob
                    up.address = address
                    if pphoto != None:
                        up.profilePhoto = pphoto
                    up.save()
                    return redirect("/profile")
        except:
            message = {'what':'Something went wrong'}
            return render(request, 'editprofile.html',message)

    u = User.objects.get(username = request.user)
    up = UserProfile.objects.get(userz=request.user)
    user = {'fname':u.first_name,'lname':u.last_name,'email':u.email,'username':u.username,'contactnumber':up.contactnumber,'gender':up.gender,'dob':up.dateofbirth.strftime("%Y-%m-%d"),'profilephoto':up.profilePhoto,'address':up.address,'genderlist':['male','female','other']}
    return render(request,'editprofile.html',user)

def store(request,slug):
    if slug=="bottle_art":
        product_list = list(Product.objects.filter(category = "Bottle art").order_by("outofstock","-soldcount").values("name","image","price","discount","productID","outofstock"))
    elif slug=="madhubani_painting":
        product_list = list(Product.objects.filter(category = "Madhubani painting").order_by("outofstock","-soldcount").values("name","image","price","discount","productID","outofstock"))
    elif slug=="name_plates":
        product_list = list(Product.objects.filter(category = "Name plate").order_by("outofstock","-soldcount").values("name","image","price","discount","productID","outofstock"))
    elif slug=="wall_plates":
        product_list = list(Product.objects.filter(category = "Wall plate").order_by("outofstock","-soldcount").values("name","image","price","discount","productID","outofstock"))
    else:
        product_list = []
    product_list = {"products":product_list}
    for item in product_list["products"]:
        item["discountedprice"] = int(item["price"]-item["price"]*item["discount"]/100)
    if request.user.is_authenticated:
        userwishlist = list(Wishlist.objects.filter(user=request.user).values("product"))
        userwlproducts = list(map(lambda x:x["product"],userwishlist))
        # print(userwlproducts)
        for item in product_list["products"]:
            if item["productID"] in userwlproducts:
                item["wcolor"] = "red"
            else:
                item["wcolor"] = "white"
        product_list["template"] = "base2.html"
        return render(request,'store.html',product_list)

    product_list["template"] = "base.html"
    return render(request, 'store.html',product_list)

def product(request,slug):
    if Product.objects.filter(productID=slug).exists():
        product = Product.objects.get(pk=slug)
        product.trend_score+=1
        if request.user.is_authenticated:
            if Product_history.objects.filter(user=request.user,product=product).exists():
                ph = Product_history.objects.get(user=request.user,product=product)
                ph.datetime = datetime.datetime.now()
                ph.save()
            else:
                phlist = Product_history.objects.filter(user=request.user).order_by("datetime")
                if len(phlist)>=10:
                    phlist[0].delete()
                ph = Product_history(user=request.user,product=product)
                ph.save()
        product.save()
        pass
    else:
        return HttpResponse("Product not found!")
    p = list(Product.objects.filter(productID=slug).values())[0]
    finaldict = {}
    p["discountedprice"] = int(p["price"]-p["price"]*p["discount"]/100)
    if request.user.is_authenticated:
        finaldict["template"] = "base2.html"
        if Wishlist.objects.filter(user=request.user,product=p["productID"]).exists():
            p["wcolor"] = "red"
        else:
            p["wcolor"] = "white"
        if Cart.objects.filter(user=request.user,product=p["productID"]).exists():
            p["cart"] = True
        else:
            p["cart"] = False
    else:
        finaldict["template"] = "base.html"
    
    finaldict["product"] = p
    if Rating.objects.filter(product=slug).exists():
        finaldict["reviews"] = list(Rating.objects.filter(product=slug).values("rating","review")[0:5])
    else:
        finaldict["reviews"] = []
    return render(request,'product.html',finaldict)

def wishlist(request):
    if request.user.is_anonymous:   
        return redirect("/login")
    uwishlist = Wishlist.objects.filter(user = request.user)
    wishlistdet=[]
    for item in uwishlist:
        wish = {"name":item.product.name,"image":item.product.image,"price":item.product.price,"discount":item.product.discount,"productID":item.product.productID,"outofstock":item.product.outofstock}
        wishlistdet.append(wish)
    wishlistdet.sort(key=lambda x:x["outofstock"])
    userwishlist = {"products":wishlistdet,"template":"base2.html"}
    for item in userwishlist["products"]:
            item["wcolor"] = "red"
            item["discountedprice"] = int(item["price"]-item["price"]*item["discount"]/100)
    return render(request,'wishlist.html',userwishlist)

def mycart(request):
    if request.user.is_anonymous:
        return redirect("/login")
    cartlist = Cart.objects.filter(user = request.user)
    cartdet=[]
    for item in cartlist:
        wish = {"name":item.product.name,"image":item.product.image,"price":item.product.price,"discount":item.product.discount,"productID":item.product.productID,"outofstock":item.product.outofstock,"quantity":item.quantity}
        cartdet.append(wish)
    cartdet.sort(key=lambda x:x["outofstock"])
    usercart = {"products":cartdet,"template":"base2.html"}
    totalamount = 0
    for item in usercart["products"]:
            item["discountedprice"] = int(item["price"]-item["price"]*item["discount"]/100)
            item["totalamount"] = int(item["discountedprice"]*item["quantity"])
            totalamount+=item["totalamount"]
    usercart["totalamount"] = totalamount
    return render(request,'cart.html',usercart)
    
def buyproduct(request,slug):
    if request.user.is_anonymous:
        return redirect("/login")
    if Product.objects.filter(productID=slug).exists():
        pass
    else:
        return redirect("/")
    
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        pincode = request.POST.get("pincode")
        modeofpayment = request.POST.get("modeofpayment")
        qty = request.POST.get("quantity")
        print(name,phone,address,pincode,modeofpayment,qty)
        if len(phone)!=10 or len(pincode)!=6:
            return redirect("/buyproduct/"+slug)
        if int(qty)<=0:
            return redirect("/buyproduct/"+slug)
        with transaction.atomic():
            if modeofpayment == "cod" or modeofpayment == "netbanking" or modeofpayment == "upi" or modeofpayment == "card":
                pass
            else:
                return redirect("/buyproduct/"+slug)
            p = Product.objects.get(pk=slug)
            if p.outofstock==True:
                return redirect("/")
            if p.quantity<int(qty):
                return redirect("/buyproduct/"+slug)
            up = UserProfile.objects.get(userz=request.user)
            char  = string.ascii_lowercase + string.digits
            oid = ''.join(random.choice(char) for _ in range(10)) 
            while PurchasedProduct.objects.filter(orderid=oid).exists():
                oid = ''.join(random.choice(char) for _ in range(10))
            ppid = ''.join(random.choice(char) for _ in range(10))
            while PurchasedProduct.objects.filter(purchasedprodid=ppid).exists():
                ppid = ''.join(random.choice(char) for _ in range(10))
            payid = ''.join(random.choice(char) for _ in range(10))
            while PaymentDetails.objects.filter(paymentid=payid).exists():
                payid = ''.join(random.choice(char) for _ in range(10))
            payment = PaymentDetails(paymentid = payid,modeofpayment = modeofpayment,paymentstatus = True,transactionid = "NA")
            order = OrderDetails(orderid = oid,purchaser = request.user,nameonpurchase = name,paymentid = payment,dateofpurchase=datetime.datetime.today(),address=address,pincode=pincode,phone=phone,amount=int(p.price*int(qty)-p.discount*int(qty)))
            purchasedprod = PurchasedProduct(purchasedprodid = ppid,product = p,quantity = qty,orderid = order,price = p.price,discount = p.discount)
            payment.save()
            order.save()
            purchasedprod.save()
            p.quantity = p.quantity-int(qty)
            p.soldcount = p.soldcount+int(qty)
            if p.quantity==0:
                p.outofstock = True
            p.save()
        return render(request,'orderplaced.html',{"template":"base2.html","orderid":oid})
    p = Product.objects.get(pk=slug)
    p.trend_score+=3
    up = UserProfile.objects.get(userz=request.user)
    u = request.user
    if p.outofstock==True:
        return redirect("/")
    product = {'pid':p.productID,'name':p.name,'price':p.price,'image':p.image,'discount':p.discount,'description':p.description,'discountedprice':int(p.price-p.price*p.discount/100),'name':u.first_name+' '+u.last_name,'address':up.address,'phone':up.contactnumber}

    return render(request,'buyproduct.html',product)

def buycart(request):
    if request.user.is_anonymous:
        return redirect("/login")
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        pincode = request.POST.get("pincode")
        modeofpayment = request.POST.get("modeofpayment")
        # print(name,phone,address,pincode,modeofpayment)
        if len(phone)!=10 or len(pincode)!=6:
            return redirect("/buycart")
        cartlist = Cart.objects.filter(user = request.user)
        if len(cartlist)==0:
            return redirect("/cart")
        totalamount = 0
        for item in cartlist:
            if item.product.outofstock==True:
                message= {"status":"Failed","message":f"{item.product.name} is out of stock. Please remove it from your cart to proceed.","template":"base2.html","nextsteplink":"/cart","nextstep":"My Cart"}
                return render(request,'message.html',message)
            if item.product.quantity<item.quantity:
                message= {"status":"Failed","message":f"There are only {item.product.quantity} units available for {item.product.name}. Please remove extra from your cart to proceed.","template":"base2.html","nextsteplink":"/cart","nextstep":"My Cart"}
                return render(request,'message.html',message)
            totalamount = totalamount + item.product.price*item.quantity - int((item.product.price*(item.product.discount/100))*item.quantity)
        
        with transaction.atomic():
            if modeofpayment == "cod" or modeofpayment == "netbanking" or modeofpayment == "upi" or modeofpayment == "card":
                pass
            else:
                return redirect("/buycart")
            char  = string.ascii_lowercase + string.digits
            oid = ''.join(random.choice(char) for _ in range(10)) 
            while PurchasedProduct.objects.filter(orderid=oid).exists():
                oid = ''.join(random.choice(char) for _ in range(10))
            payid = ''.join(random.choice(char) for _ in range(10))
            while PaymentDetails.objects.filter(paymentid=payid).exists():
                payid = ''.join(random.choice(char) for _ in range(10))
            payment = PaymentDetails(paymentid = payid,modeofpayment = modeofpayment,paymentstatus = True,transactionid = "NA")
            order = OrderDetails(orderid = oid,purchaser = request.user,nameonpurchase = name,paymentid = payment,dateofpurchase=datetime.datetime.today(),address=address,pincode=pincode,phone=phone,amount=totalamount)
            payment.save()
            order.save()
            cartlist = Cart.objects.filter(user = request.user)
            for item in cartlist:
                ppid = ''.join(random.choice(char) for _ in range(10))
                while PurchasedProduct.objects.filter(purchasedprodid=ppid).exists():
                    ppid = ''.join(random.choice(char) for _ in range(10))
                purchasedprod = PurchasedProduct(purchasedprodid = ppid,product = item.product,quantity = item.quantity,orderid = order,price = item.product.price,discount = item.product.discount)
                purchasedprod.save()
                item.product.quantity = item.product.quantity-item.quantity
                item.product.soldcount = item.product.soldcount+item.quantity
                item.product.trend_score+=3
                if item.product.quantity==0:
                    item.product.outofstock = True
                item.product.save()
                item.delete()
        return render(request,'orderplaced.html',{"template":"base2.html","oid":oid})
    user = request.user
    userp = UserProfile.objects.get(userz=user)
    return render(request,'buycart.html',{"template":"base2.html","name":user.first_name+" "+user.last_name,"address":userp.address,"phone":userp.contactnumber})



def myorders(request):
    if request.user.is_anonymous:
        return redirect("/login")
    orders = OrderDetails.objects.filter(purchaser=request.user)
    orderlist=[]
    for order in orders:
        orderdet = {"orderid":order.orderid,"dateofpurchase":order.dateofpurchase,"nameonpurchase":order.nameonpurchase,"items":[],"amount":order.amount}
        products = PurchasedProduct.objects.filter(orderid=order)
        for product in products:
            orderdet["items"].append({"name":product.product.name,"quantity":product.quantity})
        orderlist.append(orderdet)
    orderlist.sort(key=lambda x:x["dateofpurchase"],reverse=True)
    userorders = {"orders":orderlist}
    return render(request,'myorders.html',userorders)

def order(request,slug):
    if request.user.is_anonymous:
        return redirect("/login")
    if OrderDetails.objects.filter(orderid=slug).exists():
        pass
    else:
        return redirect("/")
    order = OrderDetails.objects.get(orderid=slug)
    if order.purchaser != request.user:
        return redirect("/")
    orderdet = {"orderid":order.orderid,"dateofpurchase":order.dateofpurchase,"nameonpurchase":order.nameonpurchase,"modeofpayment":order.paymentid.modeofpayment,"paymentstatus":order.paymentid.paymentstatus,"address":order.address,"pincode":order.pincode,"phone":order.phone,"amount":order.amount,"status":order.status,"items":[]}
    products = PurchasedProduct.objects.filter(orderid=order)
    for product in products:
        orderdet["items"].append({"productid":product.product.productID,"name":product.product.name,"quantity":product.quantity,"price":product.product.price,"discount":product.product.discount,"discountedprice":int(product.product.price-product.product.price*product.product.discount/100),"image":product.product.image})
    return render(request,'order.html',orderdet)

def apicalls(request,slug):
    
    if request.method == "GET":
        if slug=="addtowishlist":
            if request.user.is_anonymous:
                return redirect("/login")
            productID = request.GET.get("productID")[2:]
            p = Product.objects.get(productID=productID)
            p.trend_score+=2
            p.save()
            user = request.user
            if Wishlist.objects.filter(product=productID,user=user).exists():
                return JsonResponse({"error":"Already exist in wishlist"},status=400)
            with transaction.atomic():
                try:
                    newwishlist = Wishlist(user=user,product=Product.objects.get(productID=productID))
                    newwishlist.save()
                    return JsonResponse({"pid":productID,"color":"red","message":"Successfully added to wishlist!"},status=200)
                except:
                    return JsonResponse({"Error":"something went wrong"},status=400)

        if slug=="removefromwishlist":
            if request.user.is_anonymous:
                return redirect("/login")
            productID = request.GET.get("productID")[2:]
            p = Product.objects.get(productID=productID)
            p.trend_score-=2
            p.save()
            user = request.user
            with transaction.atomic():
                try:
                    Wishlist.objects.filter(product=productID,user=user)[0].delete()
                    return JsonResponse({"pid":productID,"color":"white","message":"Successfully removed from wishlist!"},status=200)
                except:
                    return JsonResponse({"Error":"something went wrong"},status=400)


        if slug=="addtocart":
            if request.user.is_anonymous:
                return redirect("/login")
            productID = request.GET.get("productID")
            user = request.user
            totalamount = 0
            cartlist = Cart.objects.filter(user = request.user)
            for item in cartlist:
                totalamount+=item.product.price*item.quantity
            if Cart.objects.filter(product=productID,user=user).exists():
                with transaction.atomic():
                    try:
                        cartobj = Cart.objects.filter(product=productID,user=user)[0]
                        cartobj.quantity+=1
                        cartobj.save()
                        totalamount = totalamount+cartobj.product.price
                        return JsonResponse({"pid":productID,"button":"added","totalamount":totalamount,"message":"Successfully added to Cart!"},status=200)
                    except:
                        return JsonResponse({"Error":"something went wrong"},status=400)

            with transaction.atomic():
                try:
                    newcart = Cart(user=user,product=Product.objects.get(productID=productID),quantity=1)
                    p = Product.objects.get(productID=productID)
                    p.trend_score+=2
                    p.save()
                    newcart.save()
                    totalamount = totalamount+newcart.product.price
                    return JsonResponse({"pid":productID,"button":"added","totalamount":totalamount,"message":"Successfully added to Cart!"},status=200)
                except:
                    return JsonResponse({"Error":"something went wrong"},status=400)

        if slug=="removefromcart":
            if request.user.is_anonymous:
                return redirect("/login")
            productID = request.GET.get("productID")
            user = request.user
            totalamount = 0
            cartlist = Cart.objects.filter(user = request.user)
            for item in cartlist:
                totalamount+=item.product.price*item.quantity
            with transaction.atomic():
                try:
                    cartobj = Cart.objects.filter(product=productID,user=user)[0]
                    if cartobj.quantity==1:
                        p = Product.objects.get(productID=productID)
                        p.trend_score-=2
                        p.save()
                        cartobj.delete()
                    elif cartobj.quantity>1:
                        cartobj.quantity-=1
                        cartobj.save()
                    totalamount = totalamount-cartobj.product.price
                    return JsonResponse({"pid":productID,"button":"add","totalamount":totalamount,"message":"Successfully removed from Cart!"},status=200)
                except:
                    return JsonResponse({"error":"Something went wrong"},status=400)
        
        if slug=="getrating":
            productID = request.GET.get("productID")
            rating_count = Rating.objects.filter(product=productID).count()
            delivered_rating = int(request.GET.get("lastrating"))
            if rating_count==0 or rating_count<=delivered_rating:
                return JsonResponse({"error":"End of rating"},status=400)
            if Rating.objects.filter(product=productID).exists():
                ratinglist = list(Rating.objects.filter(product=productID).values("rating","review"))
                return JsonResponse({'rating':ratinglist},status=200)
            return JsonResponse({"error":"Something went Wrong!"},status=400)
                
        if slug=="addreview":
            if request.user.is_anonymous:
                return redirect("/login")
            productID = request.GET.get("productID")
            rating = request.GET.get("rating")
            review = request.GET.get("review")
            if Rating.objects.filter(product=productID,user=request.user).exists():
                return JsonResponse({"error":"Already rated this product"},status=400)
            with transaction.atomic():
                try:
                    newrating = Rating(user=request.user,product=Product.objects.get(productID=productID),rating=rating,review=review)
                    newrating.save()
                    return JsonResponse({"message":"Successfully rated the product!"},status=200)
                except Exception as e:
                    print(e)
                    return JsonResponse({"error":"Something went wrong"},status=400)
                
        