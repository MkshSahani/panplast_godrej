from django.urls import path 
from . import views 
from user.views import user_logout


urlpatterns = [
    path('', views.homePage, name = "homePage"),
    path('/user/login', user_logout, name="userLogout"),  
]
