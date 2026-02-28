#!/usr/bin/env python3
"""
attacker_sim.py
Advanced attacker simulation for testing the honeypot.
Includes multiple scenarios: HTTP requests, brute-force attempts,
port scanning, and malformed payloads.
"""

import socket
import time
import logging

# Configure local logger for simulation output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
sim_logger = logging.getLogger("AttackerSim")

def simple_http_request(host="127.0.0.1", port=8080):
    """Send a basic HTTP request to test honeypot response."""
    try:
        s = socket.socket()
        s.connect((host, port))
        s.send(b"GET /admin HTTP/1.1\r\nHost: localhost\r\n\r\n")
        response = s.recv(1024).decode(errors="ignore")
        sim_logger.info(f"HTTP response from port {port}: {response.strip()}")
    except Exception as e:
        sim_logger.error(f"HTTP request failed: {e}")
    finally:
        s.close()

def brute_force_attempts(host="127.0.0.1", port=22):
    """Simulate repeated login attempts on SSH."""
    attempts = [b"root:1234", b"admin:password", b"user:qwerty"]
    try:
        s = socket.socket()
        s.connect((host, port))
        for attempt in attempts:
            s.send(attempt + b"\n")
            sim_logger.info(f"Sent brute-force attempt: {attempt.decode()}")
            time.sleep(0.5)
    except Exception as e:
        sim_logger.error(f"Brute-force simulation failed: {e}")
    finally:
        s.close()

def port_scan(host="127.0.0.1", ports=[21, 22, 23, 8080]):
    """Simulate scanning multiple ports."""
    for port in ports:
        try:
            s = socket.socket()
            s.settimeout(0.5)
            s.connect((host, port))
            s.send(b"SCAN TEST\n")
            sim_logger.info(f"Port {port} responded to scan.")
            s.close()
        except Exception:
            sim_logger.warning(f"Port {port} closed or filtered.")

def malformed_payload(host="127.0.0.1", port=23):
    """Send malformed binary data to test honeypot logging."""
    try:
        s = socket.socket()
        s.connect((host, port))
        s.send(b"\xff\xfe\xfd\xfcINVALID_PAYLOAD\n")
        sim_logger.info("Sent malformed payload to port 23.")
    except Exception as e:
        sim_logger.error(f"Malformed payload failed: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    sim_logger.info("Starting attacker simulations...")
    simple_http_request()
    brute_force_attempts()
    port_scan()
    malformed_payload()
    sim_logger.info("All simulations complete.")









