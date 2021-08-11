# urls.py for mold_management  


from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')), # user application urls start. 
    path('', include('user_panel.urls')), 
    path('mould/', include('mould.urls')), 
    path('quality/', include('MouldQuality.urls')), 
]
