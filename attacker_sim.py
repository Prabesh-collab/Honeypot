import socket

def simulate_attack(host="127.0.0.1", port=8080, payload=b"GET /admin HTTP/1.1\n"):
    s = socket.socket()
    s.connect((host, port))
    s.send(payload)
    try:
        response = s.recv(1024)
        print("Response:", response.decode(errors="ignore"))
    finally:
        s.close()

if __name__ == "__main__":
    simulate_attack()










