from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.


def home(request):
    if request.session.get('username'):
        username=request.session .get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')

def register(request):
    uf=Userform()
    pf=Profileform()
    d={'uf':uf,'pf':pf}

    if request.method=="POST" and request.FILES:
        ufd=Userform(request.POST)
        pfd=Profileform(request.POST,request.FILES)
        if ufd.is_valid() and pfd.is_valid():
            ufo=ufd.save(commit=False)
            password=ufd.cleaned_data['password']
            ufo.set_password(password)
            ufo.save()

            pfo=pfd.save(commit=False)
            pfo.profile_user=ufo
            pfo.save()

            send_mail('Registration','Registration is successfully, Thanks for Registration','muniraji775@gmail.com',[ufo.email],fail_silently=False)

            return HttpResponse('Registration is successfully')
    return render(request,'register.html',d)

def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        user=authenticate(username=username,password=password)
        if user and user.is_active:
            login(request,user)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('You are not an authencated user')

    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))