from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from ecapp.models import UserProfile,Contact_us,Product,Wishlist,Cart,PurchasedProduct,OrderDetails,PaymentDetails
from django.db import transaction
import datetime
import random
import string

from django.conf import settings
from django.core.mail import send_mail

# Create your views here.

def index(request):
    if request.user.is_anonymous:
        return render(request, 'index.html',{"template":"base.html"})
    return render(request,'index.html',{"template":"base2.html"})

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
            message = {"what":"Something went wrong please try again"}
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
                        user = User.objects.create_user(username=username, password=password, email=email, first_name=fname, last_name=lname, is_active=False)
                        user.save()
                        userprofile = UserProfile(userz=user,contactnumber=contact, dateofbirth=dob,gender = gender,profilePhoto = pphoto, address = address,verifycode = a)
                        userprofile.save()
                        subject = 'Verify your email'
                        message = f'Hi {fname} {lname},\n\nPlease verify your email by clicking on the link below:\nhttp://127.0.0.1:8000/verify/{a}\n\nThanks,\nTeam Indian Kalakriti'
                        email_from = settings.EMAIL_HOST_USER
                        recipient_list = [email,]
                        send_mail( subject, message, email_from, recipient_list )
                        return redirect("/login")
        except:
            message = {'what':'Something went wrong'}
            return render(request, 'signup.html',message)

        
    return render(request, 'signup.html')

def verify(request,slug):
    if UserProfile.objects.filter(verifycode=slug).exists:
        with transaction.atomic():
            userprofile = UserProfile.objects.get(verifycode=slug)
            user = userprofile.userz
            user.is_active = True
            userprofile.vefiycode = ""
            userprofile.verified = True
            userprofile.save()
            user.save()
        return redirect("/login")
    return redirect("/")

def forgotpassword(request):
    if request.method == "POST":
        ausername = request.POST.get("username")
        if "@" and "." in ausername:
            if User.objects.filter(email=ausername).exists():
                ausername = User.objects.get(email=ausername)
                print("got user")
            else:
                message = {'what':'User does not exist'}
                return render(request, 'forgotpassword.html',message)
        else:
            if User.objects.filter(username=ausername).exists():
                ausername = User.objects.get(username=ausername)
                print("got user")
            else:
                message = {'what':'User does not exist'}
                return render(request, 'forgotpassword.html',message)
        if ausername.is_active == False and UserProfile.objects.get(userz=User.objects.get(username=ausername.username)).verified == False:
            message = {'what':'Please check your email to verify your account'}
            return render(request, 'forgotpassword.html',message)
        print("user exists")
        char  = string.ascii_lowercase + string.digits
        a = ''.join(random.choice(char) for _ in range(20)) 
        while UserProfile.objects.filter(verifycode=a).exists():
            a = ''.join(random.choice(char) for _ in range(20))
        u = UserProfile.objects.get(userz = ausername)
        u.verifycode = a
        u.save()
        print("sending mail")
        subject = 'Forgot password!'
        message = f'Hi {ausername.first_name} {ausername.last_name},\n\nYour requested password reset link is below:\nhttp://127.0.0.1:8000/changepassword/{a}\n\nThanks,\nTeam Indian Kalakriti'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [ausername.email,]
        send_mail( subject, message, email_from, recipient_list )
        print("mail sent")
        return redirect("/login")

    return render(request,"forgotpassword.html")

def changepassword(request,slug):
    if request.method == "POST":
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        if password == password2:
            with transaction.atomic():
                u = UserProfile.objects.get(verifycode=slug)
                user = u.userz
                user.set_password(password)
                user.save()
                u.verifycode = ""
                u.save()
                return redirect("/login")
    if UserProfile.objects.filter(verifycode=slug).exists():
        return render(request,"changepassword.html")
    return redirect('/')

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
        subject = 'Order placed'
        message = f'Hi {request.user.first_name} {request.user.last_name},\n\nYour order for order id {oid} has been placed. It will be soon at your doorstep.\n\nThanks,\nTeam Indian Kalakriti\n\nThis is an email generated from a project and not a real order placed.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.user.email,]
        send_mail( subject, message, email_from, recipient_list )
        return render(request,'orderplaced.html',{"template":"base2.html","orderid":oid})
    p = Product.objects.get(pk=slug)
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
                if item.product.quantity==0:
                    item.product.outofstock = True
                item.product.save()
                item.delete()
        subject = 'Order placed'
        message = f'Hi {request.user.first_name} {request.user.last_name},\n\nYour order for order id {oid} has been placed. It will be soon at your doorstep.\n\nThanks,\nTeam Indian Kalakriti\n\nThis is an email generated from a project and not a real order placed.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.user.email,]
        send_mail( subject, message, email_from, recipient_list )
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
    if request.user.is_anonymous:
        return redirect("/login")
    if request.method == "GET":
        if slug=="addtowishlist":
            productID = request.GET.get("productID")[2:]
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
            productID = request.GET.get("productID")[2:]
            user = request.user
            with transaction.atomic():
                try:
                    Wishlist.objects.filter(product=productID,user=user)[0].delete()
                    return JsonResponse({"pid":productID,"color":"white","message":"Successfully removed from wishlist!"},status=200)
                except:
                    return JsonResponse({"Error":"something went wrong"},status=400)


        if slug=="addtocart":
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
                    newcart.save()
                    totalamount = totalamount+newcart.product.price
                    return JsonResponse({"pid":productID,"button":"added","totalamount":totalamount,"message":"Successfully added to Cart!"},status=200)
                except:
                    return JsonResponse({"Error":"something went wrong"},status=400)

        if slug=="removefromcart":
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
                        cartobj.delete()
                    elif cartobj.quantity>1:
                        cartobj.quantity-=1
                        cartobj.save()
                    totalamount = totalamount-cartobj.product.price
                    return JsonResponse({"pid":productID,"button":"add","totalamount":totalamount,"message":"Successfully removed from Cart!"},status=200)
                except:
                    return JsonResponse({"error":"Something went wrong"},status=400)
                
