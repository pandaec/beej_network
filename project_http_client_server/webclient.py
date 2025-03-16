import socket
import sys

host = sys.argv[1]
port = int(sys.argv[2]) if len(sys.argv) >= 2 else 80
req = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n".encode()

so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
so.settimeout(5)
try:
    so.connect((host, port))
    so.sendall(req)
    while True:
        try:
            d = so.recv(4096)
            if len(d) == 0:
                break
            resp = d.decode()
            print(resp)
        except socket.timeout:
            print("Receive timeout")
            break
except socket.error as e:
    print(f"Socket error: {e}")
finally:
    so.close()