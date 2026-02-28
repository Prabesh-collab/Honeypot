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
    #!/usr/bin/env python3
import socket
import threading
import logging

# Ports to listen on
LISTEN_PORTS = [21, 22, 23, 8080]

def start_honeypot(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", port))
    s.listen(5)
    logging.info(f"Honeypot listening on port {port}")
    while True:
        conn, addr = s.accept()
        data = conn.recv(1024).decode("utf-8", errors="ignore")
        logging.info(f"Data from {addr} on port {port}: {data}")
        conn.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    for port in LISTEN_PORTS:
        threading.Thread(target=start_honeypot, args=(port,), daemon=True).start()

    # Keep the main thread alive
    while True:
        pass
