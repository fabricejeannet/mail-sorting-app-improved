from utils.constants import *

class Match:

    def __init__(self):
        self.id = -1
        self.status:str = None
        self.company_name:str = None
        self.trademark = []
        self.owner:str = None
        self.domiciliary:str = None
        self.matching_ratio = {}
    

    def get_max_ratio(self) -> int :
        max_ratio:int = 0
        for ratio in self.matching_ratio.values():
            if ratio > max_ratio:
                max_ratio = ratio
        return max_ratio
        

    def __str__(self):
        string_to_return = f"[{self.id}] Company : {self.company_name}\tTrademark : {self.trademark}\tOwner : {self.owner}\nDomiciliary : {self.domiciliary}"
       
        '''
        string_to_return = str(self.id) + "\n" \
            + self.status  + "\n" \
            + self.company_name  + "\n" \
            + self.owner + "\n" \
            + self.domiciliary 
        '''       
        
        return string_to_return
    
    
   
