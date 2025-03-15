import socket
import sys
from datetime import datetime, timezone

port = int(sys.argv[1])

so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "localhost"
so.bind((host, port))
print(f"Hosting on {host}:{port}")
so.listen(5)
so.settimeout(2)

body = '''<!doctype html>
<html>
<head>
</head>
<div>
    <h1>Example Domain</h1>
    <p>This domain is for use in illustrative examples in documents. You may use this
    domain in literature without prior coordination or asking for permission.</p>
    <p><a href="https://www.iana.org/domains/example">More information...</a></p>
</div>
</body>
</html>'''

try:
    while True:
        try:
            current_time = datetime.now(timezone.utc)
            # Format it as "Sat, 15 Mar 2025 06:21:56 GMT"
            formatted_date = current_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
            content = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nDate: {formatted_date}\r\nContent-Length: {len(body.encode())}\r\nConnection: close\r\n\r\n{body}"
            c, addr = so.accept()
            with c:
                print(f"Connection accepted from {repr(addr[1])}")
                c.recv(1024) # Read HTTP request
                c.sendall(content.encode())
        except socket.timeout:
            continue
        except socket.error as e:
            print(f"Socket error: {e}")

except KeyboardInterrupt:
    print("\nServer shutting down")
finally:
    so.close()

