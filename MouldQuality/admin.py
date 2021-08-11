from django.contrib import admin
from .models import PPMData, DamageType, AuditTrack, capa_data
admin.site.register(PPMData) # PPM Data. 
admin.site.register(DamageType) # register DamageType database. 
admin.site.register(AuditTrack) # AuditTrack.
admin.site.register(capa_data)