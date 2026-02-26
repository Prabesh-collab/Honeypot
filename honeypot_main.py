import sys
from honeypot_logger import setup_logger

class GUICallback:
    def __init__(self):
        self.gui_ref = None
    
    def __call__(self, msg):
        if self.gui_ref:
            self.gui_ref.append_log(msg)

gui_callback = GUICallback()
logger = setup_logger(log_callback=gui_callback)
