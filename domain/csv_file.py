import pandas as pd

class CsvFile:
 
    def __init__(self, file_path:str) -> None:
        self._data_frame = pd.read_csv(file_path)
