from django.urls import path 
from . import views 
urlpatterns = [
    path('login/', views.user_login, name = "userLogin"), 
    path('signup/', views.user_signup, name = "userSignup"), 
    path('', views.user_profile, name = "userProfile"), 
    path('logout/', views.user_logout, name = "userLogout"), 
]
