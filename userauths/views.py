from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import logout
from userauths.models import User

# User = settings.AUTH_USER_MODEL

# Create your views here.
def register_view(request):
    
    form = UserRegisterForm(request.POST or None)
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Chào {username},tài khoản được tạo thành công")
            new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'] )
            login(request, new_user)
            return redirect('core:index')
   
    context = {
        'form' : form
    }
    return render(request, 'userauths/sign-up.html', context)

def login_view(request):
    

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email = email)
            user = authenticate(request, email = email, password = password)
            if user is not None:
                login(request, user)
                messages.success(request, "Đăng nhập thành công") 
                return redirect("core:index")
            else:
                messages.warning(request, "Email hoặc mật khẩu không chính xác")
        except:
            messages.warning(request, f"{email} không tồn tại")
        
        
        
    context = {}
    
    if request.user.is_authenticated:
        
        return redirect('core:index')
    
    
    return render(request, 'userauths/sign-in.html', context)


def logout_view(request):
    logout(request)
    messages.success(request, "Đã đăng xuất")
    
    return redirect('userauths:sign-in')