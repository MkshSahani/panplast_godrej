from mould.models import MouldStatus, GeneralClearningArchieve, PreventiveMaintainceArchive 

class DataCollector: 

    def __init__(self, mould_id = None): 
        if mould_id is not None: 
            try:
                self.mould_data = MouldStatus.objects.filter(mould_id = mould_id)  
            except: 
                self.mould_data = None 
            try:      
                self.mould_cleaning_data = GeneralClearningArchieve.objects.filter(mould_id = mould_id) 
            except:
                self.mould_cleaning_data = None 
            
            
            try:    
                self.p_main_data = PreventiveMaintainceArchive.objects.filter(mould_id = mould_id)
            except: 
                self.p_main_data = None
        
        else: 
            self.mould_data = None 
            self.mould_cleaning_data = None 
            self.p_main_data = None
        # in constructor we have calculated mould data 
        # now we will manuplate is to do desired calcualtion. 
    
    def get_commulative_count(self):
        count = 0 
        print("------")
        print(self.mould_data)
        print("------")
        if self.mould_data is None: 
            return count 
        for mould in self.mould_data: 
            count = count + mould.count_increment 
        return count 
    
    def count_g_clean(self):
        if self.mould_cleaning_data is None: 
            return 0 
        return len(self.mould_cleaning_data) # mould cleaning data. 

    
    def count_p_main(self): 
        if self.p_main_data is None: 
            return 0 
        return len(self.p_main_data)

        



