import re
from django.shortcuts import render,redirect
from datetime import datetime
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth import get_user_model,authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile
from .form import profileform
from .models import CustomUser
from core.models import Order
from django.template.loader import render_to_string
from django.core.mail import send_mail
User = get_user_model()
'''SIGNUP VIEW'''
def signup(request):
    if request.method == 'POST':
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return redirect('signup')

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already used")
                return redirect('signup')

            try:
                validate_password(password)
                if not re.search(r"[A-Z]", password):
                    messages.error(request, "Your password must contain at least one uppercase letter.")
                    return redirect('signup')

                if not re.search(r"\d", password):
                    messages.error(request, "Your password must contain at least one digit.")
                    return redirect('signup')

                User.objects.create_user(first_name=fname, last_name=lname, username=username, email=email, password=password)
                messages.success(request, "Account created successfully! Please log in.")
                return redirect('log_in')
            except ValidationError as e:
                for i in e.messages:
                    messages.error(request, i)
                return redirect('signup')
        else:
            messages.error(request, "Password and Confirm Password do not match.")
            return redirect('signup')

    return render(request, 'account/signup.html', {'date': datetime.now()})


# LOGIN VIEW
def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me', False)

        if not User.objects.filter(username=username).exists():
            messages.error(request, "This username is not registered.")
            return redirect("log_in")

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

            if remember_me:
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)

            next_url = request.POST.get('next', '')
            return redirect(next_url if next_url else 'index')
        else:
            messages.error(request, "Invalid password.")
            return redirect('log_in')

    next_url = request.GET.get('next', '')
    return render(request, 'account/login.html', {'date': datetime.now(), 'next': next_url})


# LOGOUT VIEW
def log_out(request):
    logout(request)
    return redirect('log_in')

def change_password(request):
    form=PasswordChangeForm(user=request.user)
    
    if request.method== 'POST':
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('log_in')
    return render(request,"core/auth/password_change.html",{'form':form})

@login_required(login_url='log_in')
def profile(request):
    return render(request,'profile/profile.html')

@login_required(login_url='log_in')
def update_profile(request):
    profile,created= Profile.objects.get_or_create(user=request.user)
    form=profileform(instance=profile)
    
    if request.method=='POST':
        form=profileform(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
  
    context={
        'form':form,
        'user':request.user,
        'profile':request.user.profile
    }
    return render(request,'profile/update_profile.html',context)
@login_required(login_url='log_in')
def reset_password(request):
    form2=PasswordChangeForm(user=request.user)
    if request.method== 'POST':
        form2=PasswordChangeForm(user=request.user,data=request.POST)
        if form2.is_valid():
            form2.save()
            return redirect('log_in')
    return render(request,'profile/reset_password.html',{'form2':form2})

@login_required(login_url='log_in')
def my_order(request):
    if request.method=='POST':
        phone=request.POST['phone']
        address=request.POST['address']
        cart=request.session.get('cart')
        uid=request.session.get("_auth_user_id")
        user=CustomUser.objects.get(id=uid)
        print(cart)

        product_list=[]
        for i in cart:
            product=cart[i]['name']
            quantity=cart[i]['quantity']
            price=cart[i]['price']
            total=quantity*float(price)
            image=cart[i]['image']
            
            order=Order(
                product=product,
                user=user,
                price=price,
                quantity=quantity,
                image=image,
                total=total,
                phone=phone,
                address=address
            )
            order.save()

            product_list.append({
                'name':product,
                'quantity':quantity,
                'total':total
            })

        request.session['cart']={}
        try:
            subject = "Thank You for Your Order! here Your Order Confirmation"
            message_body = render_to_string('account/order_message.html', {  
                'name': user.first_name,
                'product_list': product_list,
                'address': address,
                'phone': phone,
                'date': datetime.now()
            })
            send_mail(
                subject,
                message_body,
                'sujanmijar018@gmail.com',  # Sender email
                [user.email],                    # Recipient email
                fail_silently=False,
            )
            messages.success(request, f"Dear {user.first_name}, your order has been placed successfully and a email has been sent")
        except Exception as e:
                messages.error(request, f"Error: {str(e)}")
                return redirect('my_order')
        return redirect('my_order')
    
    uid=request.session.get("_auth_user_id")
    user=CustomUser.objects.get(id=uid)
    order=Order.objects.filter(user=user)
            
    return render(request,'profile/my_order.html',{'order':order})