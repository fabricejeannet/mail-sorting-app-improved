from utils.constants import *

class Result:

    def __init__(self):
        self.id = -1
        self.status:str = None
        self.company_name:str = None
        self.trademark = []
        self.owner:str = None
        self.domiciliary:str = None
        self.matching_ratio = {}
        
        
    def __str__(self):
        string_to_return = str(self.id) + "\n" \
            + self.status  + "\n" \
            + self.company_name  + "\n" \
            + self.owner + "\n" \
            + self.domiciliary
        
        return string_to_return
    
    
   
