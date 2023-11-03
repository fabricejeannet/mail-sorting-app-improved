import json

class ConfigImporter:
    
    __instance = None

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = super(ConfigImporter, cls).__new__(cls)
        return cls.__instance


    def __init__(self):
        with open("../config.json") as config_file:
            self.data  = json.load(config_file)
        
