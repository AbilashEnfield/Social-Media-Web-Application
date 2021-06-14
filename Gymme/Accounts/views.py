from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.http import JsonResponse
from . models import *


# Create your views here.
def user_signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            phone = request.POST['phone']
            password = request.POST['password']
            if User.objects.filter(email=email).exists():
                return JsonResponse('email', safe=False)
            elif User.objects.filter(username=username).exists():
                return JsonResponse('username', safe=False)
            elif People.objects.filter(phone_number=phone).exists():
                return JsonResponse('phone', safe=False)
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                People.objects.create(user=user, phone_number=phone)
                auth.login(request, user)
                data = True
                return JsonResponse(data, safe=False)
        else:
            return render(request, 'Accounts/user_signup.html')


def trainer_signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            phone = request.POST['phone']
            password = request.POST['password']
            category = request.POST['category']
            if User.objects.filter(email=email).exists():
                return JsonResponse('email', safe=False)
            elif User.objects.filter(username=username).exists():
                return JsonResponse('username', safe=False)
            elif People.objects.filter(phone_number=phone).exists():
                return JsonResponse('phone', safe=False)
            else:
                if category is not None:
                    if Category.objects.filter(name=category).exists():
                        User.objects.create(username=username, password=password, email=email)
                        trainer = User.objects.get(username=username)
                        categoryInst = Category.objects.get(name=category)
                        Trainer.objects.create(trainer=trainer, phone_number=phone, category=categoryInst)
                        auth.login(request, trainer)
                        return JsonResponse('true', safe=False)
                    else:
                        Category.objects.create(name=category)
                        User.objects.create(username=username, password=password, email=email)
                        trainer = User.objects.get(username=username)
                        categoryInst = Category.objects.get(name=category)
                        Trainer.objects.create(trainer=trainer, phone_number=phone, category=categoryInst)
                        auth.login(request, trainer)
                        return JsonResponse('true', safe=False)
                else:
                    return redirect('trainerSignup')
        else:
            categories = Category.objects.all()
            context = {'categories': categories}
            return render(request, 'Accounts/trainer_signup.html', context)


def user_signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            print(username)
            password = request.POST['password']
            print(password)
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                data = True
                return JsonResponse('True', safe=False)
            else:
                data = False
                return JsonResponse('False', safe=False)
        else:
            return render(request, 'Accounts/user_signin.html')


def admin_signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        # if User.objects.filter()
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            phone = request.POST['phone']
            password = request.POST['password']
            if User.objects.filter(email=email).exists():
                return JsonResponse('email', safe=False)
            elif User.objects.filter(username=username).exists():
                return JsonResponse('username', safe=False)
            elif People.objects.filter(phone_number=phone).exists():
                return JsonResponse('phone', safe=False)
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                People.objects.create(user=user, phone_number=phone)
                auth.login(request, user)
                return JsonResponse('true', safe=False)
        else:
            return render(request, 'Accounts/admin_signup.html')


def admin_signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return JsonResponse('true', safe=False)
            else:
                return JsonResponse('false', safe=False)
        else:
            return render(request, 'Accounts/admin_signin.html')


def user_signout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return render(request, 'Accounts/user_signin.html')
    else:
        return redirect('home')
