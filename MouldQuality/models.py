from django.db import models
from django.contrib.auth.models import User 

# ------------------------------------- 
class PPMData(models.Model): 

    new_code =  models.CharField(max_length=100)
    vendor_name = models.CharField(max_length=200)
    ppm_data_added = models.DateField(auto_now_add=True)
    total_number_of_lot = models.IntegerField()
    total_number_of_lot_rejected = models.IntegerField()


    def ppm(self): 
        
        number_of_lot_accepted = self.total_number_of_lot - self.total_number_of_lot_rejected
        return number_of_lot_accepted / (10 ** 6)
    
    
    def __str__(self): 
        return self.new_code + self.vendor_name


# ---------------------------------------- 

class DamageType(models.Model): 

    damage_name = models.CharField(max_length=200)
    mould_severity_level = models.IntegerField()

    def __str__(self):
        return self.damage_name + "_" + str(self.mould_severity_level) 
    

# -------------------------------------------

class AuditTrack(models.Model): 

    audit_id = models.AutoField(primary_key=True)
    supplier = models.CharField(max_length=200)
    audit_type = models.CharField(max_length=20)
    tools = models.IntegerField()

    no_of_machine = models.IntegerField()

    godrej_auitor = models.CharField(max_length=50)

    supplier_audito = models.CharField(max_length=50)

    both_side_done = models.BooleanField(default = False)

    score = models.IntegerField(null=True)


    def grade(self): 

        if self.score is None: 
            return "-"
        
        elif self.score >= 90: 
            return "S"
        
        elif self.score >= 80: 
            return "A"
        
        elif self.score >= 70: 
            return "B"
        
        elif self.score >= 60: 
            return "C"

        elif self.score >= 50: 
            return "D"
        else: 
            return "E"
        
        
# ------------------------------------------------ 
class capa_data(models.Model): 

    serial_number = models.AutoField(primary_key=True)
    item_code = models.CharField(max_length=100)
    item_name = models.CharField(max_length=200)
    # last updated database. 
    last_updated = models.DateTimeField(auto_now = True)
    rejection_reason = models.CharField(max_length=100, null = True)
    capa_comment = models.CharField(max_length=200, null = True)
    capa_submitted = models.CharField(max_length=200, null = True)
    capa_recv = models.CharField(max_length=200, null = True)
    remark = models.CharField(max_length=200, null = True)

    
