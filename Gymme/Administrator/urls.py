from django.urls import path
from . import views


urlpatterns = [
    path('admin_dashboard/', views.admin_dashboard, name='adminDashboard'),
    path('people_list/', views.people_list, name='peopleList'),
    path('blockPeople/<int:id>', views.block_people, name='blockPeople'),
    path('trainer_list/', views.trainer_list, name='trainerList'),
    path('blockTrainer/<int:id>', views.block_trainer, name='blockTrainer'),
    path('videos_list/', views.videos_list, name='videosList'),
    path('banVideo/<int:id>', views.ban_video, name='banVideo'),

]
