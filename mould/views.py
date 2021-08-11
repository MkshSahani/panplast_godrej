from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required 
from .models import Mould, MouldDailyCheck, MouldDamage, MouldDamageArchive, MouldStatus, MouldComment, GeneralCleaningPresent, GeneralClearningArchieve, MouldUnload, MouldDailyCheck, PreventiveMaintaince 
from .models import GeneralClearningArchieve, PreventiveMaintainceArchive
from MouldQuality.models import DamageType
import matplotlib.pyplot as plt  
import matplotlib.dates as mdates 
import os
import datetime 

# ------------------------------------------------- 


MOULD_DELECTED = False 
MOULD_ID_DELETED = None 
BACK_FROM_GCLEAN = False 
BACK_FROM_PCLEAN = False 
BACK_FROM_DAMAGE = False 


class MouldData: 

    def __init__(self): 
        self.threshold = None 
        self.presentCount = None 
    
    def isThresholdCross(self): 
        diffrence = self.threshold - self.presentCount 
        alert_flag = True 
        if diffrence <= 500: 
            alert_flag = True 
        else: 
            alert_flag = False 
 
        return alert_flag     
    

@login_required 
def mould_registration(request): 
    context = {}
    context['mouldRegistered'] = False 
    if request.method == "POST": 
        mould_id = request.POST.get('mouldNumber')
        mould_name = request.POST.get('mouldName')
        cavity_number = request.POST.get('cavityNumber')
        general_cleaning_threshold_value = request.POST.get('GeneralCleaningthresholdValue')
        preventive_maintaince_value = request.POST.get('PreventiveMaintainceValue')
        tool_life_count = request.POST.get('toolLifeCount')
        mould_desc = request.POST.get('mouldDesc')
        mould_order_number = request.POST.get('orderNumber')
        mould_raw_material = request.POST.get('rawMaterial')        
        part_weight = request.POST.get('partWeight')
        runner_weight = request.POST.get('runnerWeight')
        tonnage = request.POST.get('tonnage')
        cycle_time = request.POST.get('cycleTime')
        target_shots = request.POST.get('shotsPerDay')
        mould = Mould()
        mould.mould_id = mould_id 
        mould.mould_name = mould_name 
        mould.cavity_number = cavity_number 
        mould.registered_by = request.user 
        mould.general_maintaince_cleaning_threshold_value = general_cleaning_threshold_value  
        mould.present_count = 0 
        mould.preventive_maintaince_clearning_thresold_value = preventive_maintaince_value 
        mould.tool_life = tool_life_count 
        
        mould.moud_desc = mould_desc
        mould.order_number = mould_order_number
        mould.raw_material = mould_raw_material 
        mould.part_weight = part_weight 
        mould.runner_weight = runner_weight 
        mould.tonnage = tonnage 
        mould.cycle_time = cycle_time 
        mould.number_of_shots_per_day = target_shots
        
        mould.save() # mould registered. 
        context['mouldRegistered'] = True 
        context['mouldName'] = mould_name
        print(mould_id, mould_name, cavity_number)
        return render(request, 'mould_registration.html', context)
    else: 
        context['mouldRegistered'] = False 
        return render(request, 'mould_registration.html', context)



@login_required 
def mould_view(request, mould_id): 
    context = {}
    if request.method == "POST": 
        comment_on_mould_id = request.POST.get('id')
        comment_text = request.POST.get('comment')
        comment_by = request.user 
        comment = MouldComment()
        comment.comment_text = comment_text 
        comment.commented_by = comment_by
        comment.mould_id = Mould.objects.get(mould_id = comment_on_mould_id)
        comment.save()
        return redirect(f'/mould/{comment_on_mould_id}')

    global BACK_FROM_GCLEAN, BACK_FROM_PCLEAN, BACK_FROM_DAMAGE 
    if BACK_FROM_GCLEAN: 
        context['BACK_G_CLEAN'] = True 
        BACK_FROM_GCLEAN = False 
    else: 
        context['BACK_G_CLEAN'] = False 

    if BACK_FROM_PCLEAN: 
        context['BACK_P_CLEAN'] = True 
        BACK_FROM_PCLEAN = False 
    else: 
        context['BACK_P_CLEAN'] = False

    if BACK_FROM_DAMAGE: 
        context['BACK_FROM_DAMAGE'] = True 
        BACK_FROM_DAMAGE = False
    else:
        context['BACK_FROM_DAMAGE'] = False

    try: 
        damage = MouldDamage.objects.get(mould_id = Mould.objects.get(mould_id = mould_id))
        context['DAMAGE'] = True 
        context['damage'] = damage
    except: 
        context['DAMAGE'] = False   
        

    comments = MouldComment.objects.filter(mould_id = mould_id).order_by('commented_date_time')
    comments = list(comments)[::-1]
    print(comments)
    context['comments'] = comments 
    mould_data =  Mould.objects.get(mould_id = mould_id)
    context['data'] = mould_data 
    
    # if mould in general_cleaning 

    try: 
        mould_g_clean_data = GeneralCleaningPresent.objects.get(mould_id = mould_data)
        print(mould_g_clean_data)
        context['mould_g_clean_data'] = mould_g_clean_data 
        context['IN_CLEAN'] = True 
    except: 
        context['IN_CLEAN'] = False 

    
    try: 
        mould_p_maintain = PreventiveMaintaince.objects.get(mould_id = mould_data)
        print(mould_p_maintain)
        context['mould_p_main'] = mould_p_maintain 
        context['IN_MAIN'] = True 
    except: 
        context['IN_MAIN'] = False 



    drawGraphMould_vs_shots(mould_data)
    return render(request, 'mould_id.html', context)


@login_required 
def mould_update(request): 
    context = {}
    context['MouldUpdate'] = False 
    if request.method == "POST": 
        context['MouldUpdate'] = True 
        mould_data = Mould.objects.all() 
        context['Mould_Data'] = mould_data 
        mould_id = request.POST.get('mouldID')
        increment = request.POST.get('increment')

        target_mould = Mould.objects.get(mould_id = mould_id)
        target_mould.present_count = target_mould.present_count + int(increment) 
        target_mould.general_cleaning_maintance_count = target_mould.general_cleaning_maintance_count + int(increment)
        target_mould.preventice_maintaince_count = target_mould.preventice_maintaince_count + int(increment)
        target_mould.save()


        mould_entry = MouldStatus()
        mould_entry.mould_id = target_mould 
        mould_entry.count_increment = increment 
        mould_entry.save()
        print(mould_id, increment)
        mould_entry_data = MouldStatus.objects.filter(mould_id = target_mould)
        context['target_mould_data'] = mould_entry_data 

        return render(request, 'mould_update.html', context)
    else: 
        mould_data = Mould.objects.all() 
        context['Mould_Data'] = mould_data 
        return render(request, 'mould_update.html', context)


@login_required
def mould_search(request): 
    context = {}
    mould_id = Mould.objects.all()
    global MOULD_DELECTED, MOULD_ID_DELETED 
    if MOULD_DELECTED: 
        context['mould_deleted'] = True 
        context['mould_id_deleted'] = MOULD_ID_DELETED 
        MOULD_ID_DELETED = None 
        MOULD_DELECTED = False 
    mould_list_id = []
    for mould in mould_id: 
        mould_list_id.append(mould.mould_id)
    context['mould_id'] = mould_list_id
    if request.method == "POST": 
        mould_id = request.POST.get('mould_id')
        return redirect(f'/mould/{mould_id}')
    else: 
        return render(request, 'mould_search.html', context)


@login_required 
def mould_data_update(request, mould_id): 
    context = {}
    mould_data = Mould.objects.get(mould_id = mould_id)
    context['MouldData'] = mould_data 
    if request.method == "POST": 
        return render(request, 'mould_data_update.html', context)
    else: 
        return render(request, 'mould_data_update.html', context)



# ------------------------------------------------------------
# Graph Drawer. 

def drawGraphMould_vs_shots(mould_id): 
    mould_status_data = MouldStatus.objects.filter(mould_id = mould_id).order_by('status_update')
    
    increment_date = []
    increment_count = []

    for mould in mould_status_data: 
        increment_date.append(mould.status_update.date())
        increment_count.append(mould.count_increment)
    print(increment_count)
    print(increment_date)
    plt.title(f'Shot vs Date for Mould ID {mould_id}')
    plt.xlabel('Date')
    plt.ylabel('Shot Count')
    # plt.show()
    plt.plot(increment_date, increment_count,marker='>', color='blue')
    # beautify the x-labels
    plt.gcf().autofmt_xdate()
    myFmt = mdates.DateFormatter('%D:%M:%Y')
    plt.gca().xaxis.set_major_formatter(myFmt)
    plt.savefig('mould/static/images/mould_daily_count.png')
    plt.close()

# ------------------------------------------------------------ 


@login_required 
def mould_value_update(request, mould_id): 
    context = {}
    context['mould_id'] = mould_id
    mouldData = Mould.objects.get(mould_id = mould_id)
    print(mouldData)
    context['mouldData'] = mouldData 
    context['moldUpdated'] = False 

    if request.method == "POST": 
        mould_name = request.POST.get('mouldName')
        mould_cavity_number = request.POST.get('cavityNumber')
        mould_general_cleaning = request.POST.get('GeneralCleaningthresholdValue')
        mould_preventive_cleaning = request.POST.get('PreventiveMaintainceValue')
        mould_tool_life = request.POST.get('toolLifeCount')
        mouldData.mold_name = mould_name 
        mouldData.cavity_number = mould_cavity_number 
        mouldData.general_maintaince_cleaning_threshold_value = mould_general_cleaning 
        mouldData.preventive_maintaince_clearning_thresold_value = mould_preventive_cleaning 
        mouldData.tool_life = mould_tool_life 
        mouldData.save() # tool date updated. 
        context['mouldUpdated'] = True 
        return render(request, 'mould_value_update.html', context)
    return render(request, 'mould_value_update.html', context)

# ----------------------- Mould Delete ------------------------- 
@login_required 
def mould_delete(request, mould_id):
    mould_data = Mould.objects.get(mould_id = mould_id)
    mould_data.delete()
    global MOULD_DELECTED, MOULD_ID_DELETED
    MOULD_ID_DELETED = mould_id 
    MOULD_DELECTED = True 
    return redirect('/mould/mouldSearch/')



@login_required 
def general_cleaning(request, mould_id): 
    mould_data = Mould.objects.get(mould_id = mould_id)
    context = {}
    context['mould_data'] = mould_data 
    return render(request, 'mould_general_cleaning.html', context)


@login_required 
def p_maintaince(request, mould_id): 
    mould_data = Mould.objects.get(mould_id = mould_id)
    context = {}
    context['mould_data'] = mould_data 
    return render(request, 'mould_preventive_maintain.html', context)


@login_required 
def general_cleaning_accept(request): 
    context = {}
    if request.method == "POST": 
        mould_id = request.POST.get('id')
        comment = request.POST.get('comment')
        try:
            general_cleaning = GeneralCleaningPresent.objects.get(mould_id = mould_id)
        except: 
            general_cleaning = None 
        if general_cleaning is not None: 
            context['ALREDY_IN_SERVICE'] = True
            return render(request, 'mould_gclean_accept.html',context) 
        else: 
            general_cleaning_accept_object = GeneralCleaningPresent()
            general_cleaning_accept_object.mould_id = Mould.objects.get(mould_id = mould_id)
            general_cleaning_accept_object.comment = comment 
            general_cleaning_accept_object.save()
        
            context['ACCEPTED'] = True 
            context['mould_data'] = Mould.objects.get(mould_id = mould_id)
            print("----------------")
            print(context['mould_data'])
            return render(request, 'mould_gclean_accept.html', context)
    else: 
        context['NO_DATA'] = True 
        return render(request, 'mould_gclean_accept.html', context)

@login_required 
def p_maintain_accept(request):
    context = {}
    if request.method == "POST": 
        mould_id = request.POST.get('id')
        comment = request.POST.get('comment')
        try:
            general_cleaning = PreventiveMaintaince.objects.get(mould_id = mould_id)
        except: 
            general_cleaning = None 
        if general_cleaning is not None: 
            context['ALREDY_IN_SERVICE'] = True
            return render(request, 'mould_pmaintain_accept.html',context) 
        else: 
            general_cleaning_accept_object = PreventiveMaintaince()
            general_cleaning_accept_object.mould_id = Mould.objects.get(mould_id = mould_id)
            general_cleaning_accept_object.comment = comment 
            general_cleaning_accept_object.save()
        
            context['ACCEPTED'] = True 
            context['mould_data'] = Mould.objects.get(mould_id = mould_id)
            print("----------------")
            print(context['mould_data'])
            return render(request, 'mould_pmaintain_accept.html', context)
    else: 
        context['NO_DATA'] = True 
        return render(request, 'mould_gclean_accept.html', context)

# ----------------------------------------------

def inspection_type_choice(request): 
    context = {}
    # render mould insepction choince html page with context if we need any variable. 
    # init is here. 
    return render(request, 'mould_inspection_choice.html', context) 





# ----------------------------------------------- 

def mould_unload(request): 
    context = {}

    if request.method == "POST": 
        mould_name = request.POST.get('mouldName')
        mould_id = request.POST.get('mouldNumber')
        cavity_number = request.POST.get('cavityNumber')
        clause_1 = request.POST.get('inspect_clause_1')
        clause_2 = request.POST.get('inspect_clause_2')
        clause_3 = request.POST.get('inspect_clause_3')
        clause_4 = request.POST.get('inspect_clause_4')
        clause_5 = request.POST.get('inspect_clause_5')
        clause_6 = request.POST.get('inspect_clause_6')
        clause_7 = request.POST.get('inspect_clause_7')
        print(mould_id, clause_1, clause_2, clause_3, clause_4)
        print(clause_5, clause_6, clause_7)

        mould_unload_obj = MouldUnload()
        mould_unload_obj.mould_id = mould_id 
        mould_unload_obj.mould_name = mould_name 
        mould_unload_obj.clause_1 = False if clause_1 is None else True
        mould_unload_obj.clause_2 = False if clause_2 is None else True 
        mould_unload_obj.clause_3 = False if clause_3 is None else True 
        mould_unload_obj.clause_4 = False if clause_4 is None else True
        mould_unload_obj.clause_5 = False if clause_5 is None else True
        mould_unload_obj.clause_6 = False if clause_6 is None else True 

        mould_unload_obj.save() # save unloaded data in object. 

        context['UNLOAD'] = True 
        context['mould_name'] = mould_name 

    return render(request, 'inspection_mould_register.html', context) # render mould unload html page. 


# ----------------------------------------------- 

def mould_daily_inspection(request): 

    context = {}
    mould_data = Mould.objects.all()
    mould_id = []
    for mould in mould_data: 
        mould_id.append(mould.mould_id)
    context['mould_id'] = mould_id 
    if request.method == "POST": 
        machine_number = request.POST.get('machineNumber')
        mould_id = request.POST.get('mouldNumber')
        cavity_number = request.POST.get('cavityNumber')
        clause_1 = request.POST.get('inspect_clause_1')
        clause_2 = request.POST.get('inspect_clause_2')
        clause_3 = request.POST.get('inspect_clause_3')
        clause_4 = request.POST.get('inspect_clause_4')
        clause_5 = request.POST.get('inspect_clause_5')
        clause_6 = request.POST.get('inspect_clause_6')
        clause_7 = request.POST.get('inspect_clause_7')
        clause_8 = request.POST.get('inspect_clause_8')
        clause_9 = request.POST.get('inspect_clause_9')
        clause_10 = request.POST.get('inspect_clause_10')




        print(mould_id, machine_number, clause_1, clause_2, clause_3, clause_4)
        print(clause_5, clause_6, clause_7, clause_8, clause_9, clause_10)
        
        mould_daily_chec_object = MouldDailyCheck()
        mould_daily_chec_object.mould_id = Mould.objects.get(mould_id = mould_id)
        mould_daily_chec_object.machine_id = machine_number  
        mould_daily_chec_object.clause_1 = False if clause_1 is None else True
        mould_daily_chec_object.clause_2 = False if clause_2 is None else True 
        mould_daily_chec_object.clause_3 = False if clause_3 is None else True 
        mould_daily_chec_object.clause_4 = False if clause_4 is None else True
        mould_daily_chec_object.clause_5 = False if clause_5 is None else True
        mould_daily_chec_object.clause_6 = False if clause_6 is None else True
        mould_daily_chec_object.clause_7 = False if clause_7 is None else True 
        mould_daily_chec_object.clause_8 = False if clause_8 is None else True
        mould_daily_chec_object.clause_9 = False if clause_9 is None else True
        mould_daily_chec_object.clause_10 = False if clause_10 is None else True
        mould_daily_chec_object.save() # save daily updates.

        context['SAVED'] = True 
        context['mould_id_value'] = mould_id 

    return render(request, 'inspection_mould_inspec.html', context) # render mould inspection html page. 

# -----------------------------------------------
# DataCollectorClass 


    
@login_required 
def mould_back_from_cleaning(request, mould_id): 
    global BACK_FROM_GCLEAN
    print("----------")
     
    mould_g_clean_data = GeneralCleaningPresent.objects.get(mould_id = Mould.objects.get(mould_id = mould_id))
    mould_g_clean_archive_data = GeneralClearningArchieve()
    mould_g_clean_archive_data.mould_id = mould_g_clean_data.mould_id 
    
    mould_g_clean_archive_data.date_applied_for_cleaning = mould_g_clean_data.date_applied_for_cleaning 
    mould_g_clean_archive_data.comment = mould_g_clean_data.comment 
    mould_g_clean_archive_data.save()
    mould_g_clean_data.delete()

    mould_data = Mould.objects.get(mould_id = mould_id)
    mould_data.general_cleaning_maintance_count = 0 
    mould_data.save()

    BACK_FROM_GCLEAN = True 
    return redirect(f'/mould/{mould_id}')
    

@login_required 
def mould_back_from_maintaince(request, mould_id): 
    print("----------") 
    global BACK_FROM_PCLEAN
    mould_g_clean_data = PreventiveMaintaince.objects.get(mould_id = Mould.objects.get(mould_id = mould_id))
    mould_g_clean_archive_data = PreventiveMaintainceArchive()
    mould_g_clean_archive_data.mould_id = mould_g_clean_data.mould_id 
    mould_g_clean_archive_data.date_applied_for_maitaince= mould_g_clean_data.date_applied_for_maitaince 
    mould_g_clean_archive_data.comment = mould_g_clean_data.comment 
    mould_g_clean_archive_data.save()
    
    mould_data = Mould.objects.get(mould_id = mould_id)
    mould_data.preventice_maintaince_count = 0
    mould_data.save()
    mould_g_clean_data.delete()

    BACK_FROM_PCLEAN = True 
    return redirect(f'/mould/{mould_id}')



@login_required 
def mould_damage(request, mould_id): 
    context = {}
    context['mould_data'] = Mould.objects.get(mould_id = mould_id) # store Mould Data Here. 
    list_of_damage = DamageType.objects.all()
    main_list_of_damage = []
    for damage in list_of_damage: 
        main_list_of_damage.append(damage.damage_name)

    context['ADDED_TO_DAMAGE'] = False 

    context['mould_damage']  = main_list_of_damage

    if request.method == "POST": 
        try: 
            damage_obj = MouldDamage.objects.get(mould_id = Mould.objects.get(mould_id = mould_id))
            context['ALREADY_DAMAGE'] = True 
        except: 
            damage_type = request.POST.get('damage_type')
            damage_comment = request.POST.get('comment')
            damage_obj_create = MouldDamage()
            damage_obj_create.mould_id = Mould.objects.get(mould_id = mould_id)
            damage_obj_create.damage_name = damage_type
            # damage_obj_create.damage_comment = damage_comment  
            damage_obj_create.save()
            context['ADDED_TO_DAMAGE'] = True 

    return render(request, 'mould_damage_add.html', context)

#----------------------------------------------------------------- 


@login_required 
def get_back_from_damage(request, mould_id):
    global BACK_FROM_DAMAGE 
     
    damage_obj = MouldDamage.objects.get(mould_id = Mould.objects.get(mould_id = mould_id))
    damage_obj_archive = MouldDamageArchive()
    damage_obj_archive.mould_id = Mould.objects.get(mould_id = mould_id)
    damage_obj_archive.damage_name = damage_obj.damage_name 
    damage_obj_archive.damage_occurued_on = damage_obj.damage_occurued_on
    damage_obj_archive.save()
    damage_obj.delete()
    BACK_FROM_DAMAGE = True 

    
    return redirect(f'/mould/{mould_id}') # redirect to Mould Home Page. 

