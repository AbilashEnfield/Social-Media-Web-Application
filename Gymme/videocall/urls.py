from django.urls import path
from . import views


urlpatterns = [
    path('videoCall/<str:roomCode>', views.videoCall, name='videocall'),

]
