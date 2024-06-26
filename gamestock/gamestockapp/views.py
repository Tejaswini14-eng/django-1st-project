from django.shortcuts import render,HttpResponse,redirect
from gamestockapp.forms import AddProductForm,updateproductform,UserLoginForm,UserRegisterForm,updateuserform
from .models import product , cart , orders,Review
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import random
from django.conf import settings
from django.core.mail import get_connection , EmailMessage
import razorpay
# Create your views here.



def index(request):
    return render(request,'index.html')


@login_required(login_url='/login')
def createproduct(request):
    if request.method == 'GET':
        form = AddProductForm()
        context = {'form':form}
        return render(request,'AddProduct.html',context)
    else:
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/products/view')
        else:
            context = {'error':'product not saved'}
            return render(request,'AddProduct.html',context)


def readproduct(request):
    prod = product.objects.filter(isAvailable = True)
    context = {'data':prod}
    
    return render (request,'showproduct.html',context)


def productDetails(request,rid):
    products = product.objects.filter(id = rid)

    prod = product.objects.get(id = rid)

    review = Review.objects.filter(product = prod)

    rating = 0
    n = 0
    

    for x in review:

        rating += x.rating
        n += 1

    avg_rating = int(rating/n)

    context = {'data':products , 'rating' : avg_rating}
    return render(request,'productdetail.html',context)

def updateproduct(request,rid):
    if request.method == 'GET':
        prod = product.objects.get(id = rid)
        form = updateproductform()

        form.fields['prod_name'].initial = prod.prod_name
        form.fields['description'].initial = prod.description
        form.fields['manufacturer'].initial = prod.manufacturer
        form.fields['price'].initial = prod.price
        form.fields['category'].initial = prod.category
        form.fields['isAvailable'].initial = prod.isAvailable
       

        context = {'form': form}

        return render(request,'updateproduct.html',context)
    
    else:
        prod = product.objects.get(id = rid)
        form = updateproductform(request.POST,instance=prod)

        if form.is_valid():
            form.save()
            return redirect('/products/view')
        
        else:
            return HttpResponse('Product Not Saved')


def deleteproduct(request,rid):
    prod = product.objects.filter(id = rid)
    prod.delete()
    return redirect('/products/view')

def userRegister(request):
    if request.method == 'GET':
        form = UserRegisterForm()
        context = {'form' : form }
        return render(request,'Registeration.html',context)
    else:
        form  = UserRegisterForm(request.POST)

        print(form)
        if form.is_valid():
            password = form.cleaned_data['password']
            confirmPassword = form.cleaned_data['confirmPassword']
            if password == confirmPassword:
                user = form.save(commit = False)

                user.set_password(password)

                user.save()
                return redirect('/login')
            
            else:
                return HttpResponse('form not saved')





def userLogin(request):
    if request.method == 'GET':
        form = UserLoginForm(request.POST)
        context = {'form' : form}
        return render(request,'UserLogin.html',context)
    
    else:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username = username , password = password)

            if user is not None:
                login(request,user)
                return redirect('/')
            
            else:
                return HttpResponse('username or password is incorrect')

def userLogout(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/login')
def readuser(request):
    user = User.objects.filter()
    context = {'data': user}
    
    return render (request,'showuser.html',context)


def updateuser(request,rid):
    if request.method == 'GET':
        user = User.objects.get(id = rid)
        form = updateuserform(instance = user)

        
       
       

        context = {'form': form}

        return render(request,'updateuser.html',context)
    
    else:
        user = User.objects.get(id = rid)
        form = updateuserform(request.POST,instance=user)

        if form.is_valid():
            form.save()
            return redirect('/users/view')
        
        else:
            return HttpResponse('user Not Saved')
        

def add_to_cart(request,rid):
    products = product.objects.get(id = rid)
    data = cart.objects.filter(user = request.user , products = products).exists()

    if data:
        return redirect('/showcart')
    else:
        price = products.price
        Cart = cart.objects.create(user = request.user , products = products , price  = price)
        Cart.save()
        return redirect('/showcart')

def showcart(request):
    Cart = cart.objects.filter(user = request.user)
    total_price = 0
    
    for x in Cart:
        total_price += x.price

    context = {'data': Cart}
    context['total_price'] = total_price
    return render(request,'showcart.html',context) 

def removecart(request,rid):
    Cart = cart.objects.filter(id = rid)
    Cart.delete()
    return redirect('/showcart')

def updatecart(request,cid,rid):
    Cart = cart.objects.filter(id = rid)
    c = cart.objects.get(id = rid)
    price = c.products.price * float(cid)
    Cart.update(quantity = cid, price = price)
    return redirect('/showcart')

def add_to_order(request):
    Cart = cart.objects.filter(user = request.user)

    total_price = 0

    for x in Cart:
        product = x.products
        quantity = x.quantity
        price = x.price

        total_price += x.price

        order = orders.objects.create(user = request.user , product = product, quantity= quantity, price = price )

        order.save()

    client = razorpay.Client(auth = (settings.KEY_ID , settings.KEY_SECRET))

    payment = client.order.create({'amount' : int(total_price*100),'currency'  : 'INR' , 'payment_capture': 1})

    context = {'data':payment, 'amount' : int(total_price*100)}


    Cart.delete()

    return render(request,'payment.html',context)

def show_orders(request):
    data = orders.objects.filter(user = request.user)

    context = {'data' : data}

    return render(request , 'orders.html', context)

def add_review(request,rid):

    products = product.objects.get(id = rid)
    review = Review.objects.filter(product = products , user = request.user ).exists()

    if review:
        return HttpResponse('Review alsready exists')

    else:
        if request.method == "GET":
            return render(request,'addreview.html')
        
        else:
            rating = request.POST['rate']
            image = request.FILES['image']
            review  = request.POST['review']

            r = Review.objects.create(user = request.user , product = products, rating = rating , image = image , review = review)

            r.save()
            return HttpResponse("Data Saved")
        

def forgot_password(request):
    if request.method == 'GET':
        return render(request,'emailreturn.html')
    
    else:
        email = request.POST['user_email']

        user = User.objects.filter(email = email).exists()

        if user:
            otp = random.randint(1000,9999)

            request.session['email_otp'] = otp
            

            with get_connection(

                host = settings.EMAIL_HOST,
                post = settings.EMAIL_PORT,
                username = settings.EMAIL_HOST_USER,
                password = settings.EMAIL_HOST_PASSWORD,
                use_tls = settings.EMAIL_USE_TLS 
            ) as connection:
                
                subject = "OTP verification"
                email_from = settings.EMAIL_HOST_USER
                reception_list = [ email ]
                message = f"OTP for reset password {otp}"

                EmailMessage(subject ,message , email_from , reception_list ,  connection = connection).send()

                return redirect('/verify_otp')
            

        else:
            return HttpResponse('User is not registered')


def verify_otp(request):
    if request.method == 'GET':
        return render(request,'otpverification.html')
    
    else:
        user_otp = int(request.POST['otp_user'])
        email_otp = int(request.session['email_otp'])

        if user_otp == email_otp:
            return redirect('/change_password')
        
        else:
            return redirect('/forgot_password')
        
def change_password(request):
    if request.method == 'GET':
        return render(request,'newpassword.html')
    
    else:
        email = request.session['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            user = User.objects.get(email = email)
            user.set_password(password)
            user.save()

            return redirect('/login')
        
        else:
            return HttpResponse('password and confirm_password does not match')