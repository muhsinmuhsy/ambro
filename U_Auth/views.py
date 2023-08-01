from django.shortcuts import render

from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error = 'User Name or Password Incorrect.'
    else:
        error = None
    return render(request, 'Auth/admin_login.html', {'error': error})


def admin_logout(request):
    logout(request)
    return redirect('dashboard')