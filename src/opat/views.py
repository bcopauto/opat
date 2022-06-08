from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from applications.views import apps




def home(request):    
    return render(request, 'home.html', {})

def oplogin(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        print(user.username)
        print(user.password)
        if not request.user.is_authenticated:
            return render(request, 'home.html', {})
        
        return redirect(apps)

    else:
        print('You need to request access to view this page.') 
        return render(request, 'login.html', {})

def oplogout(request):
    logout(request)
    return redirect(home)
        
          
