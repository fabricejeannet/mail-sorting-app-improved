import pandas as pd
from utils.string_cleaner import StringCleaner
from utils.config import ConfigImporter
from utils.constants import *

class CsvFile:

    config = ConfigImporter()

    def __init__(self, file_path:str) -> None :
        self._data_frame =  self._clean_dataframe(pd.read_csv(file_path))
        

    def _clean_dataframe(self, source_dataframe) -> pd.DataFrame :
        sc = StringCleaner()
        df = pd.DataFrame(data={ID:[], \
                                STATUS:[], \
                                COMPANY_NAME:[], 
                                TRADEMARK:[], \
                                OWNER:[], \
                                DOMICILIARY:[]})
        

        df[ID] = source_dataframe.get(ID)
        df[DOMICILIARY] = source_dataframe.get(DOMICILIARY)
        
        for column in source_dataframe.columns :
            if column != ID and column != DOMICILIARY:
                column_values = []
                for value in source_dataframe[column]:
                    column_values.append(sc.clean(str(value)))

                df[column] = column_values
                
        return df
    

    def get_dataframe(self) -> pd.DataFrame:
        return self._data_frame

