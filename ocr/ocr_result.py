class OcrResult:

    def __init__(self, lines, bounding_box) -> None:
        self.lines = lines
        self.bounding_box = bounding_box