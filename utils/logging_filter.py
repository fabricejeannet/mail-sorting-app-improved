import logging

class MyFilter(logging.Filter):
    def filter(self, record):
        return not record.getMessage().startswith('picamera2')