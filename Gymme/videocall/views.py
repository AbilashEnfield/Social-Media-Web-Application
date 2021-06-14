from django.shortcuts import render
from Actions.models import *
from django.contrib.auth.models import User
from Actions.templates.Actions import *
from Accounts.templates.Accounts import *


# Create your views here.
def videoCall(request, roomCode):
    if request.user.is_authenticated:
        couple = chatroom.objects.get(roomcode=roomCode)
        if couple.trainee.user == request.user or couple.trainerChat.trainer == request.user:
            if Trainer.objects.filter(trainer_id=request.user.id).exists():
                target = Trainer.objects.get(trainer_id=request.user.id)
            else:
                target = People.objects.get(user_id=request.user.id)
            context = {'roomCode': roomCode, 'target': target}
            return render(request, 'videocall/video_call.html', context)
        else:
            return render(request, 'Actions/403.html')
    else:
        return render(request, 'Accounts/user_signin.html')
