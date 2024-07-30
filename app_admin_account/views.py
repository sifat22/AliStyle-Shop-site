from django.shortcuts import render,redirect, get_object_or_404
from .forms import UserRegistrationForm,UserProfileForm,UserForm,CreateProfileForm
from .models import Account, UserProfile
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from app_order.models import Order,OrderProduct,Payment
from app_cart.models import CartItem
from django.contrib.auth import update_session_auth_hash

# Create your views here.

#for email activation
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.

def user_register(request):
    if request.method=='POST':
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data.get('first_name')
            last_name=form.cleaned_data.get('last_name')
            phone_number=form.cleaned_data.get('phone_number')
            email=form.cleaned_data.get('email')
            password=form.cleaned_data.get('password')
            username=email.split("@")[0]

            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number=phone_number
            user.save()


            #User Activation by gmail

            #User Activation  er jnne default reg er kichui change kora hoinai
            current_site = get_current_site(request)
            mail_subject = 'Please Activate your account!'
            message = render_to_string('app_account/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_mail = EmailMessage(mail_subject, message, to=[to_email])
            send_mail.send()

            #success registration message  before activing user we can use this
            #messages.success(request,'Thank You for registering with us.We have sent you verification email to youor email address')
            #after user activation the success message are
            return redirect("email_activation_sent")
            #User Activation by gmail end
    else:
        form = UserRegistrationForm
    return render(request,"app_account/register.html",{
        'form' : form,
    })

def email_activation_sent(request):
    return render(request, 'app_account/email_activation_sent.html')


#when we get the activation link in mail
def activate(request, uidb64, token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError , ValueError ,OverflowError ,Account.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,'Congratulation Your Account is activated')
        return redirect("dashboard")
    else:
        messages.error(request,'invalid activation link')
        return redirect('register')
    

def user_login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']

        user=auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request, user)
            #messages.success(request,"Login Successfull")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid login credentials")
            return redirect("login")
    return render(request,"app_account/login.html")


# for ggole login page design

def google_login(request):
    return render(request,"app_account/google_login.html")




#user logout
@login_required(login_url = 'login')
def user_logout(request):
    auth.logout(request)
    messages.success(request,"You are Logged Out")
    return redirect("login")



#dashboard

@login_required
def dashboard(request):
    #get order
    # orders=Order.objects.order_by('created_at').filter(user=request.user,is_ordered=True)
    # order_count=orders.count()
    user = request.user
    
    in_profile = UserProfile.objects.filter(user= user).exists()
    if in_profile:
        userprofile = UserProfile.objects.get(user= user)
        return render(request,"app_account/dashboard.html",{
            'in_profile' : in_profile,
            'userprofile' : userprofile
        })
    else:
        return render(request,"app_account/dashboard.html")
        
    


#my profile
@login_required(login_url= 'login')
def create_profile(request,user_id):
    user = get_object_or_404(Account, id = user_id)
    if request.method=='POST':
        form = CreateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            print('valid')
            data= UserProfile()
            data.user = user
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.profile_picture = form.cleaned_data['profile_picture']
            data.city = form.cleaned_data['city']
            data.state = form.cleaned_data['state']
            data.country = form.cleaned_data['country']
            data.save()
            messages.success(request,"User Profile Created Successfully")
            return redirect("dashboard")
    else:
        
        return render(request,"app_account/my_profile.html")
            
    






#Edit Profile
@login_required(login_url= 'login')
def edit_profile(request, user_id):
    userprofile = get_object_or_404(UserProfile, user__id = user_id)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance = request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance = userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "User Profile Updated Successfully")
            return redirect ('dashboard')
    else:
        user_form = UserForm(instance = request.user)
        profile_form = UserProfileForm(instance = userprofile)

    return render(request,"app_account/edit_profile.html",{
        'user_form':user_form,
        'profile_form':profile_form,
        'userprofile':userprofile,
    })

#change password
@login_required(login_url= 'login')
def change_password(request):
    if request.method == 'POST':
        user = Account.objects.get(username__exact= request.user.username)
        if user.has_usable_password():
            current_password= request.POST['current_password']
            new_password=request.POST['new_password']
            confirm_password=request.POST['confirm_password'] 
        else:
            new_password=request.POST['new_password']
            confirm_password=request.POST['confirm_password'] 


        if new_password == confirm_password:
            if user.has_usable_password():
                # User has a password, so verify the current password
                if current_password:
                    success = user.check_password(current_password)
                    if success:
                        user.set_password(new_password)
                        user.save()
                        update_session_auth_hash(request, user)  # Keep the user logged in after password change
                        messages.success(request, "Password Updated Successfully!")
                        return redirect('change_password')
                    else:
                        messages.error(request, 'Invalid Current Password')
                        return redirect('change_password')
                else:
                    messages.error(request, 'Current Password is required')
                    return redirect('change_password')
            else:
                # User signed up with Google and doesn't have a current password
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)  # Keep the user logged in after password change
                messages.success(request, "Password Set Successfully!")
                return redirect('change_password')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('change_password')

    return render(request, 'app_account/change_pass.html', {'has_usable_password': request.user.has_usable_password()})


#my order
@login_required(login_url='login')
def my_order(request):
    orders=Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    return render(request,'app_account/my_order.html',{
        'order':orders,
    })

def view_order(request, order_id):
    order_detail=OrderProduct.objects.filter(order__order_number=order_id)
    order=Order.objects.get(order_number=order_id)
    payment_status = order.cash_payment.status
    
    subtotal=0
    grand_total = 0
    for i in order_detail:
        subtotal+=(i.product_price * i.quantity)
    grand_total = order.tax + subtotal
    return render(request,'app_account/view_order.html',{
        'order_detail':order_detail,
        'order':order,
        'subtotal':subtotal,
        "grand_total":grand_total,
        'payment' : payment_status,
    })

def delete_order(request, order_id):
    order=Order.objects.get(order_number=order_id)
    order.delete()
    return redirect("my_order")




