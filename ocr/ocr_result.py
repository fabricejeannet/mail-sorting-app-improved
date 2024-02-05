class OcrResult:

    def __init__(self, line, x, y, w, h) -> None:
        self.line = line
        self.x = x
        self.y = y
        self.w = w
        self.h = h