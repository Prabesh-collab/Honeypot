#!/usr/bin/env python3
#!/usr/bin/env python3
import socket
import threading
import logging
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Ports to use when "all" is selected
DEFAULT_PORTS = [21, 22, 23, 8080]

def start_honeypot(port, stop_event):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("0.0.0.0", port))
        s.listen(5)
        logging.info(f"Honeypot listening on port {port}")
        while not stop_event.is_set():
            try:
                conn, addr = s.accept()
                data = conn.recv(1024).decode("utf-8", errors="ignore")
                logging.info(f"Data from {addr} on port {port}: {data}")
                conn.close()
            except Exception as e:
                logging.error(f"Error on port {port}: {e}")
    except Exception as e:
        logging.error(f"Failed to bind port {port}: {e}")
    finally:
        s.close()

def start_honeypot_gui():
    port_input = port_entry.get().strip()
    if port_input.lower() == "all":
        ports = DEFAULT_PORTS
    else:
        try:
            ports = [int(port_input)]
        except ValueError:
            messagebox.showerror("Invalid Port", "Please enter a number or 'all'")
            return

    global stop_event
    stop_event = threading.Event()

    for port in ports:
        threading.Thread(target=start_honeypot, args=(port, stop_event), daemon=True).start()

    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

def stop_honeypot_gui():
    if stop_event:
        stop_event.set()
        logging.info("Honeypot stopped.")
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

# GUI setup
root = tk.Tk()
root.title("Basic Honeypot Control")

logging.basicConfig(level=logging.INFO)

tk.Label(root, text="Port to listen on:").pack()
port_entry = tk.Entry(root)
port_entry.pack()

start_button = tk.Button(root, text="Start Honeypot", command=start_honeypot_gui)
start_button.pack()

stop_button = tk.Button(root, text="Stop", command=stop_honeypot_gui, state=tk.DISABLED)
stop_button.pack()

stop_event = None

root.mainloop()

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

    def stop_honeypot(self):
        """Signal the server thread to exit."""
        self.stop_event.set()
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        self.port_entry.config(state=tk.NORMAL)

def launch_gui(log_callback):
    """Entry point for the GUI."""
    root = tk.Tk()
    gui = HoneypotGUI(root, log_callback)
    root.mainloop()

