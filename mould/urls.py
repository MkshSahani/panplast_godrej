from django.urls import path, include 
from . import views 

urlpatterns = [
    path('registration/', views.mould_registration, name="MouldRegistration"),
    path('<int:mould_id>/', views.mould_view, name = "MouldView"),
    path('update/', views.mould_update,name = "MouldUpdate"),
    path('mouldSearch/', views.mould_search, name = "MouldSearch"),
    path('data/<int:mould_id>/', views.mould_data_update, name = "MouldUpdate"),
    path('update/<int:mould_id>/', views.mould_value_update, name = "MouldValueUpdate"), 
    path('delete/<int:mould_id>/', views.mould_delete, name = "MouldDeleted"), 
    path('gclean/<int:mould_id>', views.general_cleaning, name = "Gcleaning"),
    path('pmaintain/<int:mould_id>', views.p_maintaince, name = "Pmaintain"), 
    path('gclearnaccept/', views.general_cleaning_accept, name = "GcleanAccept"),
    path('pmainainAccept/', views.p_maintain_accept, name = "PcleanAccept"),
    path('inspect/', views.inspection_type_choice, name = "Inspect"), 
    path('inspect/mouldunload', views.mould_unload, name = "MouldUnLoad"), 
    path('inspect/mouldInspect', views.mould_daily_inspection, name = "MouldInspect"), 
    path('getBackGclean/<int:mould_id>/', views.mould_back_from_cleaning),
    path('getBackMain/<int:mould_id>/', views.mould_back_from_maintaince), 
    path('damageAdd/<int:mould_id>/', views.mould_damage, ), 
    path('damageRepair/<int:mould_id>/', views.get_back_from_damage), 
    
]

