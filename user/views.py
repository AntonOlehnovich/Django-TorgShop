from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from product.models import Category
from user.models import UserProfile


def index(request):
    return HttpResponse("User App")


def login_form(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            userprofile = UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage'] = userprofile.image.url
            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Ошибка авторизации! Имя или пароль некорректны")
            return HttpResponseRedirect('/login')
    # Return an 'invalid login' error message.
    category = Category.objects.all()
    context = {'category': category}
    return render(request, 'login_form.html', context)


def signup_form(request):
    category = Category.objects.all()
    context = {'category': category}
    return HttpResponse("Signup form")


def logout_func(request):
    logout(request)
    return HttpResponseRedirect('/')