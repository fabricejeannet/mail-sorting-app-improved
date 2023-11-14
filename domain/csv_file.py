import pandas as pd
from utils.string_cleaner import StringCleaner
from utils.config import ConfigImporter

class CsvFile:

    config = ConfigImporter()

    def __init__(self, file_path:str) -> None :
        self._data_frame =  self._clean_dataframe(pd.read_csv(file_path))
        

    def _clean_dataframe(self, source_dataframe) -> pd.DataFrame :
        sc = StringCleaner()
        df = pd.DataFrame(data={self.config.data["csv_headers"]["id"]:[], \
                                self.config.data["csv_headers"]["status"]:[], \
                                self.config.data["csv_headers"]["company_name"]:[], 
                                self.config.data["csv_headers"]["trademark"]:[], \
                                self.config.data["csv_headers"]["owner"]:[], \
                                self.config.data["csv_headers"]["domiciliary"]:[]})
        for column in source_dataframe.columns :
            column_values = []
            for value in source_dataframe[column]:
                column_values.append(sc.clean(str(value)))
            
            df[column] = column_values

        return df
    

    def get_dataframe(self) -> pd.DataFrame:
        return self._data_frame

