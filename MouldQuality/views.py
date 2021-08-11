from django.db.models.query import RawQuerySet
from django.shortcuts import redirect, render
from mould.models import GeneralCleaningPresent, GeneralClearningArchieve, Mould, MouldDailyCheck, PreventiveMaintainceArchive
from mould.models import MouldDamageArchive
from django.contrib.auth.decorators import login_required 

from .utils import DataCollector 
from .models import PPMData, AuditTrack, capa_data


@login_required 
def QualityPageRender(request): 
    context = {}

    # get list of moulds. 
    mould_data_list = Mould.objects.all()
    mould_commulative_cont_data = []
    
    for mould in mould_data_list: 
        mould_data_collector = DataCollector(mould.mould_id)
        print("-----")
        print(mould_data_collector.get_commulative_count())
        print("-----")
        mould_commulative_cont_data.append(MouldCommulativeCount(mould, 
        
            mould_data_collector.get_commulative_count(), 
            
            mould_data_collector.count_g_clean(), 
            
            mould_data_collector.count_p_main()))

    print(data.g_clean for data in mould_commulative_cont_data)

    context['mould_data'] = mould_commulative_cont_data    

    return render(request, 'quality/mould_quality.html', context)





# -------------------------------------------- 
@login_required 
def ppmDataView(request): 
    context = {}
    
    
    if request.method == "POST": 

        new_code = request.POST.get('newCode')
        vendor_name = request.POST.get('vendorName')
        total_number_of_lot = request.POST.get('totalLot')
        rejected_number_of_lot = request.POST.get('rejectedLot')

        ppm_obect = PPMData()
        ppm_obect.new_code = new_code 
        ppm_obect.vendor_name = vendor_name 
        ppm_obect.total_number_of_lot = total_number_of_lot
        ppm_obect.total_number_of_lot_rejected = rejected_number_of_lot 

        ppm_obect.save()    
    
    ppm_data = PPMData.objects.all()
    context['ppm_data'] = ppm_data 
    if len(ppm_data) == 0: 
        context['NO_DATA'] = True 
    else: 
        context['NO_DATA'] = False 

    for ppm in ppm_data: 
        print(ppm.ppm_data_added)

    return render(request, 'quality/ppmData.html', context)

# -------------------------------------------- 
@login_required
def inspectionDataShow(request):

    context = {}
    mould_check_data = MouldDailyCheck.objects.all()[::-1]
    if len(mould_check_data) > 10: 
        mould_check_data = mould_check_data[:10]
    
    context['mould_check_data'] = mould_check_data 
    return render(request, 'quality/mould_inspection_show.html', context) # render inspect data show page. 
    


# ---------------------------------------------

class MouldCommulativeCount: 

    def __init__(self, mould_data, commulative_count, g_clean, p_main):
        self.mould_data = mould_data 
        self.commulative_count = commulative_count 
        self.g_clean = g_clean 
        self.p_main = p_main 



# ------------------------------------------------ 
@login_required 
def mold_name_select(request): 
    context = {}

    if request.method == "POST": 
        mould_id = request.POST.get('mould_id')
        return redirect(f'/quality/historyCard/{mould_id}') 
    else: 
        mould_data_list = Mould.objects.all()
        mould_id = [mould.mould_id for mould in mould_data_list]

        context['mould_id'] =  mould_id 
        return render(request, 'quality/mould_select.html', context) 



# -------------------------------------------------- 
@login_required 
def mold_history_card(request, mould_id): 

    context = {}

    # mould data 
    context['mould_data'] = Mould.objects.get(mould_id = mould_id)
    context['GEN_CLEAN_DATA'] = GeneralClearningArchieve.objects.filter(mould_id = Mould.objects.get(mould_id = mould_id))
    context['P_MAIN_DATA'] = PreventiveMaintainceArchive.objects.filter(mould_id= Mould.objects.get(mould_id = mould_id))
    context['DAMAGE_DATA'] = MouldDamageArchive.objects.filter(mould_id = Mould.objects.get(mould_id = mould_id))
    
    if len(context['GEN_CLEAN_DATA']) != 0: 
        context['G_CLEAN'] = True 
    
    if len(context['P_MAIN_DATA']) != 0: 
        context['P_MAIN'] = True 
    
    if len(context['DAMAGE_DATA']) != 0: 
        context['DAMAGE'] = True 

    print(context['GEN_CLEAN_DATA'])

    return render(request, 'quality/mould_history_card.html', context) # return history card. 


@login_required 
def audit_track(request): 

    context = {}

    if request.method == "POST": 
        audit_track = AuditTrack()
        audit_track.supplier = request.POST.get('supplier')
        audit_track.audit_type = request.POST.get('type')
        audit_track.tools = request.POST.get('tools')
        audit_track.no_of_machine = request.POST.get('numberOfMachine')
        audit_track.godrej_auitor = request.POST.get('gAuditor')
        audit_track.supplier_audito = request.POST.get('sAuditor')
        audit_track.score = request.POST.get('score')

        audit_track.save()

    audit_data_list = AuditTrack.objects.all()[::-1] # list of all audit. 
    context['AUDIT_DATA'] = audit_data_list 
    if len(audit_data_list) == 0: 
        context['NO_DATA'] = True
    
   
    return render(request, 'quality/audit_track.html', context)


# ---------------------------------------------------- 
@login_required 
def capa_data_show(request): 

    context = {}
    context['capa_data'] = capa_data.objects.all()[::-1]
    if len(context['capa_data']) == 0: 
        context['NO_DATA'] = True 

    return render(request, 'quality/capa_data.html', context)


# ------------------------------------------------------
@login_required 
def capa_update(request, serial_number):
    context = {}
    
    
    if request.method == "POST": 

        capa_data_update_obj = capa_data.objects.get(serial_number = serial_number)
        capa_data_update_obj.capa_comment = request.POST.get('capaComment')
        capa_data_update_obj.capa_submitted = request.POST.get('cappaSubmitted')
        capa_data_update_obj.capa_recv = request.POST.get('capparecv')
        capa_data_update_obj.remark = request.POST.get('remark')
        capa_data_update_obj.save()
        context['UPDTED'] = True 
        
    
    
    
    capa_data_obj = capa_data.objects.get(serial_number = serial_number)
    context['capa_data_obj'] = capa_data_obj




    return render(request, 'quality/capa_update.html', context)
    



# ----------------------------------------------------- 
def add_new_capa_item(request): 

    context = {}

    if request.method == "POST": 

        iteam_code = request.POST.get('icode')
        iteam_name = request.POST.get('iname')
        rejection_reason = request.POST.get('reason')

        register_iteam = capa_data()
        register_iteam.item_code = iteam_code 
        register_iteam.item_name = iteam_name
        register_iteam.rejection_reason = rejection_reason 
        
        register_iteam.capa_comment = "-"
        register_iteam.capa_submitted ="-"
        register_iteam.capa_recv = "-"
        register_iteam.remark = "-"
        
        
        register_iteam.save()
        context['REG'] = True 

    return render(request, 'quality/new_capa_item.html', context)