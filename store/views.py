from django.shortcuts import render , redirect
from . models import Product , Category , Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm , UserUpdateForm , ChangePasswordForm , UserInfoForm
from django import forms

from payment_1.forms import ShippingForm
from payment_1.models import ShippingAddress

from django.db.models import Q
import json
from cart.cart import Cart


def category_summary(request):
    categories = Category.objects.all()
    return render(request , 'category_summary.html' , {'categories':categories})

def category(request , foo):
    foo = foo.replace('-',' ')
    
    try:
        category=Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request , 'category.html' , {'products':products , 'category':category})
    except:
        messages.warning(request,("This category doesn't exist..."))
        return redirect('home')

def product(request,pk):
    product=Product.objects.get(id=pk)
    return render(request , 'product.html',{'product':product})

def home(request):
    products=Product.objects.all()
    return render(request , 'home.html',{'products':products})

def about(request):
    return render(request , 'about.html' , {})

def login_user(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            # Do some shopping cart stuff
            current_user = Profile.objects.get(user__id = request.user.id)
            # Get their saved cart from database
            saved_cart = current_user.old_cart
            # Convert database string to python dictionary
            if saved_cart:
                # Convert to dictionary using JSON
                converted_cart = json.loads(saved_cart)
                #Add the loaded cart dictionary to our sassion
                # Get the cart
                cart = Cart(request)
                # Loop througth the cart and add the items from the database
                for key,value in converted_cart.items():
                    cart.db_add(product=key , quantity=value)
            return redirect('home')
                
        else:
            messages.success(request,('There is an error....'))
            return redirect('login')
    else:
        return render(request,'login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request,('You have been logged out....'))
    return redirect('login')

def register_user(request):
    form=SignUpForm()
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user=authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,('You have register successfully ! Please enter your info...'))
            return redirect('update_info')
        else:
            messages.success(request,('Oh , There was a problem please try again...'))
            return redirect('register')
    else:
        return render(request , 'register.html',{'form':form})
    
    
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UserUpdateForm(request.POST or None , instance = current_user)
        
        if user_form.is_valid():
            user_form.save()
            
            login(request , current_user)
            
            messages.success(request , ('User has been Update successfully..'))
            return redirect('home')
        return render(request , "update_user.html" , {'user_form':user_form})
    else:
        messages.success(request,('You should login at first..'))
    return redirect('login')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        
        if request.method == 'POST':
            form=ChangePasswordForm(current_user , request.POST)
            if form.is_valid():
                form.save()
                messages.success(request , ('Your password has been changed successfully ... Please log in again..'))
                login(request , current_user)
                return redirect('home')
            
            else:
                for error in list(form.errors.values()):
                    messages.error(request , error)
                return redirect('update_password')
      
        else:
            form = ChangePasswordForm(current_user)
            return render(request , "update_password.html" , {'form':form})
    
    messages.success(request , ('User has been Update successfully..'))
    return redirect('home')

def update_info(request):
    if request.user.is_authenticated:
        # Get current user
        current_user = Profile.objects.get(user__id=request.user.id)
        # Get current User's Shipping Info
        shipping_user = ShippingAddress.objects.get(user=request.user)
        # Get original User Form
        
        user_form = UserInfoForm(request.POST or None , instance = current_user)
        # Get User's Shipping Form
        shipping_form=ShippingForm(instance = shipping_user)
        
        if user_form.is_valid() or shipping_form.is_valid():
            shipping_form.save()
            user_form.save()
            
            messages.success(request , ('User has been Update Info successfully..'))
            return redirect('home')
        return render(request , "update_info.html" , {'form':user_form , 'shipping_form':shipping_form})
    else:
        messages.success(request,('You should login at first..'))
    return redirect('login')

def search(request):
    # Determine if they filled out the form
    if request.method == 'POST':
        searched = request.POST['Searched']
        # Quary the products DB model
        searched = Product.objects.filter(Q(name__icontains = searched)|Q(description__icontains = searched))
        # Test it exist
        if not searched:
            messages.success(request,('Sorry ! This type products do not exist. Please try again.'))
            return render(request , 'search.html')
        else:
            return render(request , 'search.html' , {'searched':searched})
    else:
        return render(request , "search.html" , {})
