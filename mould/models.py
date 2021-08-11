from django.db import models
from django.contrib.auth.models import User 

# -------------------------------------------------------------------------------
class Mould(models.Model): 

    mould_id = models.IntegerField(primary_key=True)
    mould_name = models.CharField(max_length=200)
    cavity_number = models.IntegerField()
    registered_date = models.DateTimeField(auto_now_add=True)
    registered_by = models.ForeignKey(User, on_delete=models.PROTECT) 
    general_maintaince_cleaning_threshold_value = models.IntegerField() 
    preventive_maintaince_clearning_thresold_value = models.IntegerField()
    tool_life = models.IntegerField()
    present_count = models.IntegerField()


    moud_desc = models.CharField(max_length=100)
    order_number = models.CharField(max_length=100)
    raw_material = models.CharField(max_length=100)
    part_weight = models.FloatField()  
    runner_weight = models.FloatField()
    tonnage = models.FloatField()
    cycle_time = models.FloatField()
    number_of_shots_per_day = models.IntegerField()

    preventice_maintaince_count = models.IntegerField(default=0)
    general_cleaning_maintance_count = models.IntegerField(default = 0)




    # * tool live over shots. 

    # * product code / mould_item_code : text.  
    # * mould desc / : text 
    # * order number : text 
    # * raw material : text
    # * part weight. : numeric 
    # * runner weight 
    # * tonnage 
    # * cycle time. 
    # * numbers per day. 
   

    def __str__(self): 
        return str(self.mould_id)

    def general_alert(self):  # alert general cleaning. 
        return self.general_maintaince_cleaning_threshold_value - self.general_cleaning_maintance_count  <= 200 

    def preventive_maintance_alert(self): # preventive maintance alert function. 
        return self.preventive_maintaince_clearning_thresold_value - self.preventice_maintaince_count <= 200 
       
    
    def tool_life_over_alert(self): # tool live over alert. 
        mould_status_data = MouldStatus.objects.filter(mould_id = self.mould_id)
        count = 0 
        for mould in mould_status_data: 
            count = count + mould.count_increment 
        
        return self.tool_life - count <= 500 
    
    

class MouldStatus(models.Model): 

    mould_id = models.ForeignKey(Mould, related_name='mould_status', on_delete=models.CASCADE)
    status_update = models.DateTimeField(auto_now_add=True)
    count_increment = models.IntegerField() # daily increment. 

    def __str__(self): 
        return str(self.mould_id)
    
    # excel file updated . 
    # * no movind mould -> no entry for more than 2 years. 
    


# -----------------------------------------------------------------------------------
class MouldComment(models.Model): 

    mould_id = models.ForeignKey(Mould, related_name='mould_chat', on_delete=models.CASCADE)
    # -> 
    comment_text = models.TextField()
    commented_by = models.ForeignKey(User,related_name='chat_user', on_delete=models.CASCADE)
    commented_date_time = models.DateTimeField(auto_now_add=True)



# ---------------------------------------------------------------------------------------- 

class GeneralCleaningPresent(models.Model): 

    mould_id = models.ForeignKey(Mould, related_name='mould_cleaning', on_delete=models.CASCADE, primary_key=True)
    date_applied_for_cleaning = models.DateTimeField(auto_now_add=True)
    date_get_back_from_cleaning = models.DateTimeField(null=True)
    comment = models.CharField(max_length=200) # any comment. 

# --------------------------------------------- 
class GeneralClearningArchieve(models.Model): 
    mould_id = models.ForeignKey(Mould, related_name='mould_gc_history', on_delete=models.CASCADE)
    date_applied_for_cleaning = models.DateTimeField(null=True)
    date_get_back_from_cleaning = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=200) # any comment. 

# ---------------------------------------------
class PreventiveMaintaince(models.Model): 
    mould_id = models.ForeignKey(Mould, related_name='mould_pm_history', on_delete=models.CASCADE)
    date_applied_for_maitaince = models.DateTimeField(auto_now_add=True)
    date_of_get_back_from_cleaning = models.DateTimeField(null = True)
    comment = models.CharField(max_length=200) 


class PreventiveMaintainceArchive(models.Model): 
    mould_id = models.ForeignKey(Mould, related_name='mould_pm_data', on_delete=models.CASCADE)
    date_applied_for_maitaince = models.DateTimeField(null = True)
    date_of_get_back_from_cleaning = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=200) 


# ----------------------------------------------------------------------- 
class MouldUnload(models.Model): 

    mould_id = models.IntegerField()
    mould_name = models.CharField(max_length = 200)
    cavity_number = models.CharField(max_length=200)

    clause_1 = models.BooleanField()
    clause_2 = models.BooleanField()
    clause_3 = models.BooleanField()
    clause_4 = models.BooleanField()
    clause_5 = models.BooleanField()
    clause_6 = models.BooleanField()


# ---------------------------------------------------------------

class MouldDailyCheck(models.Model): 

    mould_id = models.ForeignKey(Mould, related_name='Machine_Mould', on_delete=models.CASCADE)
    machine_id = models.CharField(max_length=100)
    date_time_of_update = models.DateTimeField(auto_now_add=True) # user time when data uploaded. 
    clause_1 = models.BooleanField()
    clause_2 = models.BooleanField()
    clause_3 = models.BooleanField()
    clause_4 = models.BooleanField()
    clause_5 = models.BooleanField()
    clause_6 = models.BooleanField()
    clause_7 = models.BooleanField()
    clause_8 = models.BooleanField()
    clause_9 = models.BooleanField()
    clause_10 = models.BooleanField()


# ----------------------------------------------------------------

class MouldDamage(models.Model): 

    mould_id = models.ForeignKey(Mould, related_name='mould_damage', on_delete=models.CASCADE)
    damage_name = models.CharField(max_length=200)
    damage_occurued_on = models.DateTimeField(auto_now_add=True)
    damage_comment = models.CharField(max_length=200)

    def __str__(self): 
        return str(self.mould_id.mould_id) + "_" + self.damage_name 
    


# ------------------------------------------------------------------- 

class MouldDamageArchive(models.Model): # archive dataBase for all Damages. 

    mould_id = models.ForeignKey(Mould, related_name='mould_damage_archive', on_delete=models.CASCADE)
    damage_name = models.CharField(max_length=200)
    damage_occurued_on = models.DateTimeField(null=True)
    damage_recovered_on = models.DateTimeField(auto_now_add=True)

    

    def __str__(self): 
        return str(self.mould_id.mould_id) + "_" + self.damage_name 

