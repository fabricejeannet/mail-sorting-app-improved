class OcrResult:

    def __init__(self, read_text, x, y, w, h) -> None:
        self.read_text = read_text
        self.x = x
        self.y = y
        self.width = w
        self.height = h