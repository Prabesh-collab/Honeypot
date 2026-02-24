import socket
import threading
import logging
from honeypot_logger import get_logger

def banner_for_port(port):
    """Return a fake banner for the given port."""
    banners = {
        21: "220 FTP server ready.\r\n",
        22: "SSH-2.0-OpenSSH_7.4\r\n",
        23: "Welcome to Telnet service\r\n",
        8080: "HTTP/1.1 200 OK\r\n\r\n<html><body>Hello</body></html>\r\n",
    }
    return banners.get(port, "Welcome to the honeypot.\r\n")

def handle_client(conn, addr, stop_event):
    """Handle client connection - log everything they send."""
    logger = get_logger()
    try:
        logger.info(f"Connection from {addr}")
        conn.sendall(banner_for_port(addr[1]))
        
        while not stop_event.is_set():
            try:
                data = conn.recv(4096)
                if not data:
                    break
                decoded = data.decode("utf-8", errors="replace")
                logger.info(f"Data from {addr}: {decoded.strip()!r}")
            except socket.timeout:
                continue
    except Exception as ex:
        logger.error(f"Error handling {addr}: {ex}")
    finally:
        conn.close()
        logger.info(f"Closed connection from {addr}")

def start_honeypot(port, stop_event):
    """Bind a TCP socket, accept connections, and spawn a thread per client."""
    logger = get_logger()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("0.0.0.0", port))
            s.listen(5)
            s.settimeout(1.0)
            logger.info(f"Honeypot listening on port {port}")

            while not stop_event.is_set():
                try:
                    conn, addr = s.accept()
                    t = threading.Thread(
                        target=handle_client,
                        args=(conn, addr, stop_event),
                        daemon=True,
                    )
                    t.start()
                except socket.timeout:
                    continue
    except Exception as e:
        logger.error(f"Honeypot server error: {e}")
    finally:
        logger.info("Honeypot server stopped.")


def create_honeypot_thread(port, stop_event):
    """Convenience wrapper – returns a started daemon thread."""
    t = threading.Thread(target=start_honeypot, args=(port, stop_event), daemon=True)
    t.start()
    return t