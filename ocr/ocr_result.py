class OcrResult:

    def __init__(self, text, x, y, w, h) -> None:
        self.text = text
        self.x = x
        self.y = y
        self.w = w
        self.h = h