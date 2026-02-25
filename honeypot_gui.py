
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading

class HoneypotGUI:
    def __init__(self, master, log_callback):
        self.master = master
        self.log_callback = log_callback
        self.master.title("Basic Honeypot Control")
        self.master.geometry("600x400")

        
        self.log_callback.gui_ref = self

        
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

        
        self.stop_event = threading.Event()
        self.honeypot_thread = None
    
    
    def append_log(self, message):
        """Thread‑safe way to insert a line into the text widget."""
        self.log_area.after(0, self._do_append_log, message)

    def _do_append_log(self, message):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)

    def start_honeypot(self):
        """Validate port, create stop_event, launch the server thread."""
        try:
            port = int(self.port_var.get())
            if not (1 <= port <= 65535):
                raise ValueError("Port out of range")
        except Exception as e:
            messagebox.showerror("Invalid Port", str(e))
            return

        self.stop_event.clear()
        
        from honeypot_functions import create_honeypot_thread
        
        self.honeypot_thread = create_honeypot_thread(port, self.stop_event)

        self.btn_start.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        self.port_entry.config(state=tk.DISABLED)

def launch_gui(log_callback):
    """Entry point for the GUI."""
    root = tk.Tk()
    gui = HoneypotGUI(root, log_callback)
    root.mainloop()