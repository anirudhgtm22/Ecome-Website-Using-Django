from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Category
from .models import Cake
from .models import Customer
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import check_password
from .models import Order
from django.db import transaction
from django.contrib.auth.decorators import login_required
# from .models import get_orders_by_customer



# apps.check_models_ready()

# Create your views here.

def index(request):
    all_categories = Category.objects.all()
    context = {
        'categories': all_categories,
    }
    return render(request, 'index.html', context)

def about(request):
    return render(request,'about.html')
    # return HttpResponse("this is about page")

def contact(request):
    return render(request,'contact.html')
    #return HttpResponse("this is about page")

def tracker(request):
    return render(request,'tracker.html')
    #return HttpResponse("this is about page")

def search(request):
    return render(request,'search.html')
    #return HttpResponse("this is about page")    

def productview(request):
    return render(request,'prodview.html')
    #return HttpResponse("this is about page")

def success(request):
    return render(request,'success.html') 

def go_cart(request):
    cart = request.session.get('cart')
    if not cart:
        return render(request, 'gocart.html')
    else:
        ids=list(request.session.get('cart').keys())
        cakes=Cake.objects.get_cakes_by_id(ids)
        return render(request,'gocart.html',{'cakes':cakes}) 
        

def checkout(request):
    if request.method =="POST":
        cake=request.POST.get('cake')
        cart= request.session.get('cart')
        remove = request.POST.get('remove')
        if cart:
            quantity =cart.get(cake)
            if quantity is not None:
                if remove:
                    if quantity<=1:
                        cart.pop(cake)
                    else:    
                        cart[cake]=quantity-1
                else:
                     cart[cake]=quantity+1    
            else:    
                cart[cake]=1
        else:
            cart={}
            cart[cake]=1
        request.session['cart']=cart 
    return redirect('/cakes')                   
    # return render(request, 'cart.html',{'cart': cart})
        
    
    # return render(request,'checkout.html')
    #return HttpResponse("this is about page")
    
def cakes(request):
    cart = request.session.get('cart', {})
    # request.session.clear()
    request.session['cart'] = cart
    all_cakes = Cake.objects.all()
    context = {
        'cakes': all_cakes,
    }
    return render(request, 'cakes.html', context)

def login2(request):
    return render(request,'login.html')

def signup(request):
    if request.method =="POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        
        customer = Customer(username=username, 
                            first_name=first_name, 
                            last_name=last_name,
                            phone=phone,
                            email=email,
                            )
        customer.save()
        customer.set_password(password)
        customer.save()
    return render(request,'signup.html')

def signin(request):
    print('coming here!')
    print(request.method)
       
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print("coming here!")
        customer = authenticate(request, username=username, password=password)
        print("coming here22!")
        print(customer)
        if customer is not None:
            #request.session['customer'] = customer
            request.session['customer_id'] = customer.id
            print('Session created with key:', request.session.session_key)
            print('customer_id stored in session:', request.session.get('customer_id'))
            login(request, customer)
            return render(request,'success.html')
        else:
            return HttpResponse('wrong')
            pass
    else:
        return render(request, 'login.html')
    
    
def logout_view(request):
    request.session.clear()
    logout(request)
    return redirect('login')  

def is_userlogged_in(request):
    if 'customer_id' in  request.session.keys():
        return True
    return False

def check_out(request):
    print("coming here")
    if request.method == "POST":
        if is_userlogged_in(request):
            try:
                address = request.POST.get('address')
                phone = request.POST.get('Phone')
                customer_id = request.session.get('customer_id')
                if not customer_id:
                    return HttpResponse('Invalid customer ID')
                customer = Customer.objects.get(id=customer_id)
                cart = request.session.get('cart')
                cakes = Cake.objects.get_cakes_by_id(list(cart.keys()))
                
                for cake in cakes:
                    cake_obj = Cake.objects.get(id=cake.id)
                    order = Order(customer=customer,
                                cake=cake_obj,
                                price=cake_obj.price,
                                address=address,
                                phone=phone,
                                quantity=cart.get(str(cake.id)))
                    order.save()
                request.session['cart'] = {}
                return render(request,'orders.html')
            except Exception as e:
                print(str(e))
                return HttpResponse('Error placing order')
        else:
            return render(request,'login.html')
            
    else:
        return HttpResponse('Invalid request')



def orders_placed(request):
    customer_id = request.session.get('customer_id')
    print('customer_id:', customer_id)
    print('session:', request.session)
    if not customer_id:
        return HttpResponse('Login to see your Past Orders')
    customer = Customer.objects.get(id=customer_id)
    orders = Order.objects.get_orders_by_customer(customer_id)
    print(orders)
    return render(request, 'orders.html', {'orders': orders, 'customer': customer})



        
        