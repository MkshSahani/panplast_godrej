from django.db import models
from django.contrib.auth.models import User 

# ---------------------------------------------------------------- 
class Employee(models.Model): 

    employee_id = models.ForeignKey(User, related_name='EMP_USER', on_delete=models.CASCADE) # foreign key refrecing to user. 
    employee_level = models.IntegerField() # employee level for dataAcess. 
    employee_address = models.TextField(max_length=200)
    employee_phone = models.IntegerField()
    def __str__(self): 
        return str(self.employee_id)

    # * woker level. -> 0 
    # * supervisor level. -> 1
    # * manager level. -> 2
    # * plant-head. -> 3 ---> mr. atul Tyagi. 
    
