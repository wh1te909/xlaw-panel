from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

def login(request):
    if request.method == 'POST':
        if 'rememberme' in request.POST:
            request.session.set_expiry(1209600)
        
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error':'Invalid credentials. Please try again.'})
    else:
        return render(request, 'accounts/login.html')

    return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST' or request.method == 'GET':
        auth.logout(request)
        return redirect('home')