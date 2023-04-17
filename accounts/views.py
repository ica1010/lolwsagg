from base64 import urlsafe_b64decode
from django.contrib import messages, auth
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
import requests
from LolSwagg.settings import MESSAGE_TAGS
from accounts.models import Account, UserProfile
from carts.models import Cart, Cartitems
from carts.views import _cart_id
from orders.models import Order, OrderProduct
from store.models import Product
from .forms import RegistrationForm, UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username= email.split('@')[0]
            user= Account.objects.create_user(first_name=first_name,last_name=last_name,email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = 'userprofile/f1.jpg'
            profile.save()

            current_site= get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user':user,
                'domain':current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject , message, to=[to_email])
            send_email.send()
            return redirect ('/accounts/login/?command=verification&email='+email )
    else:
        form= RegistrationForm()
    context={
        'form':form,
    }
    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate( email=email, password=password )
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = Cartitems.objects.filter(cart= cart).exists()
                if is_cart_item_exists:
                    cart_item = Cartitems.objects.filter(Cart=cart)
                    product_variation =[]
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))
                    cart_item = Cartitems.objects.filter(user=user)
                    ex_var_list = []
                    id=[]
                    for item in cart_item :
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index= ex_var_list.index(pr)
                            item_id = id[index]
                            item= Cartitems.objects.get(id=item_id)
                            item.quantity +=1
                            item.user= user
                            item.save()
                        else:
                            cart_item=Cartitems.objects.filter(Cart=cart)
                            for item in cart_item:
                                item.user= user
                                item.save()
            except:
                pass
            auth.login(request, user)
            messages.success(request,'you are now logged in')
            url= request.META.get('HTTP_REFERER')
            try :
                query= requests.utils.urlparse(url).query
                params= dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('dashboard')
        else:
            messages.error(request, 'invalid information')
            return redirect('login')    
    return render(request, 'accounts/login.html')


@login_required( login_url = 'login' )
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError,Account.DoesNotExist):
        user= None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations  your account is activated . ')
        return redirect('login')
    else:
        messages.error(request, 'invalid activation link')
        return redirect('register')
    
def dashboard(request):
    products=Product.objects.all().filter(is_available=True)
    product_count = products.count()

    userprofile = get_object_or_404(UserProfile, user=request.user)
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()

    context = {
        'product_count': product_count,
        'userprofile': userprofile,
        'orders_count': orders_count,
    }
    return render(request, 'accounts/dashbord.html', context)

@login_required(login_url='login')
def my_orders(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    orders_count = orders.count()

    context = {
        'userprofile': userprofile,
        'orders_count': orders_count,
        'orders': orders,
    }
    return render(request, 'accounts/my_orders.html', context)

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email__exact = email)
            
            current_site= get_current_site(request)
            mail_subject = 'Reset your account'
            message = render_to_string('accounts/reset_password_email.html', {
                'user':user,
                'domain':current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject , message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address .')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist !')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')

def resetpassword_validate(request,uidb64 , token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user , token):
        request.session['uid']= uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has expired !')
        return redirect('login')
    
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password :
            uid= request.session.get('uid')
            user = request.Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.session(request , 'Password reset succesful')
            return redirect ('login')
        else:
            messages.error(request , 'Password do not macth !')
            return redirect ('resetPassword')
    else:
        return render(request ,'accounts/resetPassword.html')
@login_required(login_url='login')
def edit_profile(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
        'orders_count': orders_count,
    }
    return render(request, 'accounts/edit_profile.html', context)


@login_required(login_url='login')
def change_password(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request, 'Password updated successfully.')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('change_password')
    context = {
        'userprofile': userprofile,
        'orders_count': orders_count,
    }
    return render(request, 'accounts/change_password.html',context)


@login_required(login_url='login')
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'accounts/order_detail.html', context)
