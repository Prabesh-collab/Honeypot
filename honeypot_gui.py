
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading

class HoneypotGUI:
    def __init__(self, master, log_callback):
        self.master = master
        self.log_callback = log_callback
        self.master.title("Basic Honeypot Control")
        self.master.geometry("600x400")

        # Register this GUI with the callback
        self.log_callback.gui_ref = self

        # UI Widgets
        frame = tk.Frame(master)
        frame.pack(pady=5)
        
        tk.Label(frame, text="Port to listen on:").grid(row=0, column=0, padx=5)
        self.port_var = tk.StringVar(value="12345")
        self.port_entry = tk.Entry(frame, textvariable=self.port_var, width=8)
        self.port_entry.grid(row=0, column=1)

        self.btn_start = tk.Button(frame, text="Start Honeypot", command=self.start_honeypot)
        self.btn_start.grid(row=0, column=2, padx=5)
        self.btn_stop = tk.Button(frame, text="Stop", command=self.stop_honeypot, state=tk.DISABLED)
        self.btn_stop.grid(row=0, column=3, padx=5)

        self.log_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, state=tk.DISABLED)
        self.log_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Internal state
        self.stop_event = threading.Event()
        self.honeypot_thread = None
