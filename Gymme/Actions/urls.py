from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('addChat/<int:trainer>', views.addchat, name='addChat'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='editProfile'),
    path('chat/', views.chat, name='chat'),
    path('chathere/<str:roomCode>', views.chat_room, name='chatroom'),
    path('explore/', views.explore, name='explore'),
    path('videoUpload/', views.videoUpload, name='videoUpload'),

]
