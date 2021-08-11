from django.contrib import admin
from .models import Mould, MouldStatus, MouldComment, GeneralCleaningPresent, GeneralClearningArchieve, MouldUnload, MouldDailyCheck
from .models import PreventiveMaintainceArchive, MouldDamage, MouldDamageArchive
admin.site.register(Mould) # register Mould Model. 
admin.site.register(MouldStatus)
admin.site.register(MouldComment)
admin.site.register(GeneralCleaningPresent)
admin.site.register(GeneralClearningArchieve)
admin.site.register(MouldUnload) 
admin.site.register(MouldDailyCheck)
admin.site.register(PreventiveMaintainceArchive) 
admin.site.register(MouldDamage) # MouldDamage contain database Damage 
admin.site.register(MouldDamageArchive) # MouldDamageArchive contain Archive Damage. 
