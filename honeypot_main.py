#!/usr/bin/env python3
"""
honeypot_main.py – Entry point that ties the GUI and the core logic together.
"""

import sys

# Import logger setup first
from honeypot_logger import setup_logger

# Create a callable object that can hold a reference
class GUICallback:
    def __init__(self):
        self.gui_ref = None
    
    def __call__(self, msg):
        if self.gui_ref:
            self.gui_ref.append_log(msg)

# Create the callback and initialize the logger
gui_callback = GUICallback()
logger = setup_logger(log_callback=gui_callback)

def main():
    from honeypot_gui import launch_gui
    
    # Launch the GUI (it will set up gui_callback.gui_ref)
    launch_gui(gui_callback)
    
    logger.info("Application exiting.")
    sys.exit(0)

if __name__ == "__main__":
    main()