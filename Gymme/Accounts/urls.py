from django.urls import path
from . import views


urlpatterns = [
    path('user_signup/', views.user_signup, name='userSignup'),
    path('user_signin/', views.user_signin, name='userSignin'),
    path('trainer_signup/', views.trainer_signup, name='trainerSignup'),
    path('admin_signup/', views.admin_signup, name='adminSignup'),
    path('admin_signin/', views.admin_signin, name='adminSignin'),
    path('user_signout/', views.user_signout, name='userSignout'),

]
