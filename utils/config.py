import json
import os

class ConfigImporter:
    
    __instance = None

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = super(ConfigImporter, cls).__new__(cls)
        return cls.__instance


    def __init__(self):
        filepath = os.path.abspath(f"{os.getcwd()}/config.json")
        with open(filepath) as config_file:
            self.data  = json.load(config_file)
        
