class OcrResult:

    def __init__(self, read_text:str, x:int=0, y:int=0, w:int=0, h:int=0) -> None:
        self.read_text:str = read_text
        self.clean_text:str = None
        self.x:int = x
        self.y:int = y
        self.width:int = w
        self.height:int = h
        self._discarded:bool = False
    
    
    def is_discarded(self) -> bool :
        return self._discarded
    
    
    def discard(self) -> None :
        self._discarded = True