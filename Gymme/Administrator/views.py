from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.http import JsonResponse
from .models import *
from Accounts.models import *
from Actions.models import *


# Create your views here.
def admin_dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'Administrator/adminDash.html')
    else:
        return redirect('adminSignin')


def people_list(request):
    if request.user.is_authenticated:
        ppl = People.objects.all()
        context = {'ppl': ppl}
        return render(request, 'Administrator/peoplelist.html', context)
    else:
        return redirect('adminSignin')


def block_people(request, id):
    if request.user.is_authenticated:
        user = User.objects.get(id=id)
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return redirect('peopleList')
    else:
        return redirect('adminSignin')


def trainer_list(request):
    if request.user.is_authenticated:
        ttr = Trainer.objects.all()
        context = {'ttr': ttr}
        return render(request, 'Administrator/trainerList.html', context)
    else:
        return redirect('adminSignin')


def block_trainer(request, id):
    if request.user.is_authenticated:
        user = User.objects.get(id=id)
        print(user, id)
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return redirect('trainerList')
    else:
        return redirect('adminSignin')


def videos_list(request):
    if request.user.is_authenticated:
        vds = ExploreVideos.objects.all()
        context = {'vds': vds}
        return render(request, 'Administrator/videosList.html', context)
    else:
        return redirect('adminSignin')


def ban_video(request, id):
    if request.user.is_authenticated:
        vds = ExploreVideos.objects.get(id=id)
        if vds.Active:
            vds.Active = False
        else:
            vds.Active = True
        vds.save()
        return redirect('videosList')
    else:
        return redirect('adminSignin')
