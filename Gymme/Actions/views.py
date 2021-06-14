import uuid
import base64
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files.base import ContentFile


# from Gymme.Accounts.models import *


# Create your views here.
def homepage(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            searchQuery = request.POST['search']
            print(searchQuery)
            searchResults = []
            if searchResults != '':
                trainerSearchResults = Trainer.objects.filter(trainer__username__icontains=searchQuery)
                print(trainerSearchResults)
                if not trainerSearchResults:
                    pass
                else:
                    for result in trainerSearchResults:
                        searchResults.append(result)
                videosSearchResults = ExploreVideos.objects.filter(title__icontains=searchQuery)
                if not videosSearchResults:
                    pass
                else:
                    for result in videosSearchResults:
                        searchResults.append(result)
            print(searchResults)
            vid = ExploreVideos.objects.all()
            traineeId = request.user.id
            trainee = People.objects.get(user_id=traineeId)
            chatt = chatroom.objects.filter(trainee=trainee)
            target = None
            if Trainer.objects.filter(trainer_id=request.user.id).exists():
                target = Trainer.objects.get(trainer_id=request.user.id)
            else:
                target = People.objects.get(user_id=request.user.id)
            context = {'vid': vid, 'chat': chatt, 'target': target, 'searchResults': searchResults}
            return render(request, 'Actions/base.html', context)
        else:
            vid = ExploreVideos.objects.all()
            personId = request.user.id
            person = None
            if People.objects.filter(user_id=personId).exists():
                person = People.objects.get(user_id=personId)
                chatt = chatroom.objects.filter(trainee=person)

            else:
                person = Trainer.objects.get(trainer_id=personId)
                chatt = chatroom.objects.filter(trainerChat=person)
            target = None
            if Trainer.objects.filter(trainer_id=request.user.id).exists():
                target = Trainer.objects.get(trainer_id=request.user.id)
            else:
                target = People.objects.get(user_id=request.user.id)
            context = {'vid': vid, 'chat': chatt, 'target': target}
            return render(request, 'Actions/base.html', context)
    else:
        return redirect('userSignin')


def addchat(request, trainer):
    if request.user.is_authenticated:
        code = uuid.uuid4().hex
        trainerInChat = Trainer.objects.get(trainer_id=trainer)
        traineeId = request.user.id
        trainee = People.objects.get(user_id=traineeId)
        chatroom.objects.create(roomcode=code, trainee=trainee, trainerChat=trainerInChat)
        vid = ExploreVideos.objects.all()
        target = None
        if Trainer.objects.filter(trainer_id=request.user.id).exists():
            target = Trainer.objects.get(trainer_id=request.user.id)
            chatList = chatroom.objects.filter(trainerChat=target)
            trainer = True
        else:
            target = People.objects.get(user_id=request.user.id)
            chatList = chatroom.objects.filter(trainee=target)
            trainer = False
        context = {'vid': vid, 'chat': chatList, 'target': target, 'trainer':trainer}
        return render(request, 'Actions/base.html', context)
    else:
        return redirect('userSignin')


def explore(request):
    if request.user.is_authenticated:
        vid = ExploreVideos.objects.all()
        target = None
        if Trainer.objects.filter(trainer_id=request.user.id).exists():
            target = Trainer.objects.get(trainer_id=request.user.id)

        else:
            target = People.objects.get(user_id=request.user.id)
        context = {'vid': vid, 'target': target}
        return render(request, 'Actions/explore.html', context)
    else:
        return redirect('userSignin')


def chat(request):
    if request.user.is_authenticated:
        chatList = None
        target = None
        trainer = None
        if Trainer.objects.filter(trainer_id=request.user.id).exists():
            target = Trainer.objects.get(trainer_id=request.user.id)
            chatList = chatroom.objects.filter(trainerChat=target)
            trainer = True
        else:
            target = People.objects.get(user_id=request.user.id)
            chatList = chatroom.objects.filter(trainee=target)
            trainer = False
        context = {'chat': chatList, 'target': target, 'trainer': trainer}
        return render(request, 'Actions/chat.html', context)
    else:
        return redirect('userSignin')


def chat_room(request, roomCode):
    print('hello')
    print(roomCode)
    if request.user.is_authenticated:
        couple = chatroom.objects.get(roomcode=roomCode)
        if couple.trainee.user == request.user or couple.trainerChat.trainer == request.user:
            chatList = None
            target = None
            if Trainer.objects.filter(trainer_id=request.user.id).exists():
                target = Trainer.objects.get(trainer_id=request.user.id)
                chatList = chatroom.objects.filter(trainerChat=target)
                trainer = True
            else:
                target = People.objects.get(user_id=request.user.id)
                chatList = chatroom.objects.filter(trainee=target)
                trainer = False
            chats = None
            allChats = None
            if chatContent.objects.filter(chatRoom_id=couple.id).exists():
                allChats = chatContent.objects.filter(chatRoom_id=couple.id)
                chats = chatContent.objects.filter(chatRoom_id=couple.id).filter(chatter_id=request.user.id)
            context = {'chatList': chatList, 'target': target, 'roomCode': roomCode, 'chats': chats, 'trainer': trainer, 'couple': couple, 'allChats': allChats}
            return render(request, 'Actions/chatroom.html', context)
        else:
            return render(request, 'Actions/403.html')
    else:
        return redirect('userSignin')


def profile(request):
    if request.user.is_authenticated:
        vid = ExploreVideos.objects.all()
        target = None
        vid = ExploreVideos.objects.all()
        if Trainer.objects.filter(trainer_id=request.user.id).exists():
            target = Trainer.objects.get(trainer_id=request.user.id)
        else:
            target = People.objects.get(user_id=request.user.id)

        flag = None
        if Trainer.objects.filter(trainer_id=request.user.id).exists():
            flag = True
        else:
            flag = False
        context = {'flag': flag, 'vid': vid, 'target': target}
        return render(request, 'Actions/profile.html', context)
    else:
        return redirect('userSignin')


def edit_profile(request):
    target = None
    flag = None
    username = None
    about = None
    work = None
    homeState = None
    homeCountry = None
    workState = None
    workCountry = None
    interests = None
    if request.user.is_authenticated:
        if request.method == 'POST':
            if Trainer.objects.filter(trainer_id=request.user.id).exists():
                target = Trainer.objects.get(trainer_id=request.user.id)
                if request.POST['username'] != "":
                    username = request.POST['username']
                    actualUser = User.objects.get(id=request.user.id)
                    actualUser.username = username
                    actualUser.save()
                if request.POST['about'] != "":
                    about = request.POST['about']
                    target.about = about
                    target.save()
                if request.POST['work'] != "":
                    work = request.POST['work']
                    target.work = work
                    target.save()
                if request.POST['homeState'] != "":
                    homeState = request.POST['homeState']
                    target.homeState = homeState
                    target.save()
                if request.POST['homeCountry'] != "":
                    homeCountry = request.POST['homeCountry']
                    target.homeCountry = homeCountry
                    target.save()
                if request.POST['workState'] != "":
                    workState = request.POST['workState']
                    target.workState = workState
                    target.save()
                if request.POST['workCountry'] != "":
                    workCountry = request.POST['workCountry']
                    target.workCountry = workCountry
                    target.save()
                if request.POST['interests'] != "":
                    interests = request.POST['interests']
                    target.interests = interests
                    target.save()
                if request.POST.get('coverImage') != "":
                    coverImage = request.POST.get('coverImage')
                    name = "coverPictureT"
                    format, img = coverImage.split(';base64,')
                    ext = format.split('/')[-1]
                    img_data = ContentFile(base64.b64decode(img), name=name + '.' + ext)
                    target.coverPic = img_data
                    target.save()
                if request.POST.get('proPic') != "":
                    proPic = request.POST.get('proPic')
                    name = "proPicT"
                    format, img = proPic.split(';base64,')
                    ext = format.split('/')[-1]
                    img_data1 = ContentFile(base64.b64decode(img), name=name + '.' + ext)
                    target.image = img_data1
                    target.save()
            else:
                target = People.objects.get(user_id=request.user.id)
                if request.POST['username'] != "":
                    username = request.POST['username']
                    actualUser = User.objects.get(id=request.user.id)
                    actualUser.username = username
                    actualUser.save()
                if request.POST['about'] != "":
                    about = request.POST['about']
                    target.about = about
                    target.save()
                if request.POST['work'] != "":
                    work = request.POST['work']
                    target.work = work
                    target.save()
                if request.POST['homeState'] != "":
                    homeState = request.POST['homeState']
                    target.homeState = homeState
                    target.save()
                if request.POST['homeCountry'] != "":
                    homeCountry = request.POST['homeCountry']
                    target.homeCountry = homeCountry
                    target.save()
                if request.POST['workState'] != "":
                    workState = request.POST['workState']
                    target.workState = workState
                    target.save()
                if request.POST['workCountry'] != "":
                    workCountry = request.POST['workCountry']
                    target.workCountry = workCountry
                    target.save()
                if request.POST['interests'] != "":
                    interests = request.POST['interests']
                    target.interests = interests
                    target.save()
                if request.POST.get('coverImage') != "":
                    coverImage = request.POST.get('coverImage')
                    name = "coverPicture"
                    format, img = coverImage.split(';base64,')
                    ext = format.split('/')[-1]
                    img_data = ContentFile(base64.b64decode(img), name=name + '.' + ext)
                    target.coverPic = img_data
                    target.save()
                if request.POST.get('proPic') != "":
                    proPic = request.POST.get('proPic')
                    name = "proPic"
                    format, img = proPic.split(';base64,')
                    ext = format.split('/')[-1]
                    img_data1 = ContentFile(base64.b64decode(img), name=name + '.' + ext)
                    target.image = img_data1
                    target.save()
            if Trainer.objects.filter(trainer_id=request.user.id).exists():
                flag = True
            else:
                flag = False
            vid = ExploreVideos.objects.all()
            context = {'flag': flag, 'vid': vid, 'target': target}
            return render(request, 'Actions/editProfile.html', context)

        else:
            vid = ExploreVideos.objects.all()
            if Trainer.objects.filter(trainer_id=request.user.id).exists():
                target = Trainer.objects.get(trainer_id=request.user.id)
            else:
                target = People.objects.get(user_id=request.user.id)

            if Trainer.objects.filter(trainer_id=request.user.id).exists():
                flag = True
            else:
                flag = False

            context = {'flag': flag, 'vid': vid, 'target': target}
            return render(request, 'Actions/editProfile.html', context)
    else:
        return redirect('userSignin')


def videoUpload(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if Trainer.objects.filter(trainer_id=request.user.id).exists():
                trainer = Trainer.objects.get(trainer_id=request.user.id)
                video = request.FILES.get('videofile')
                print(video)
                title = request.POST['title']
                description = request.POST['description']
                ExploreVideos.objects.create(trainer=trainer, title=title, discription=description, video=video)
                return render(request, 'Actions/videoUpload.html')
            else:
                # messages.add_message(request, CRITICAL, 'You can not add videos.')
                return render(request, 'Actions/videoUpload.html', messages)
        else:
            return render(request, 'Actions/videoUpload.html')
    else:
        return redirect('userSignin')
