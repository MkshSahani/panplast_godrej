from django.urls import path
from . import views 

urlpatterns = [
    path('', views.QualityPageRender,name = "MouldQuality"), 
    path('ppm', views.ppmDataView, name = "ppmData"),
    path('mouldInspect', views.inspectionDataShow, name = "MouldInspectView"),  
    path('mouldSelect/', views.mold_name_select, name = "MouldNameSelect"), 
    path('historyCard/<int:mould_id>', views.mold_history_card), 
    path('auditTrack/', views.audit_track, name = "Audit"), 
    path('capaData/', views.capa_data_show, name = "CapaData"), 
    path('newIteam/',views.add_new_capa_item, name = "NewIteam"), 
    path('updateCAPA/<int:serial_number>', views.capa_update), 
]
