import sys
import socket
import time
import random
import threading

def usage():
    print("usage: select_client.py prefix host port", file=sys.stderr)

def random_string():
    """ Returns a random string of ASCII printable characters. """
    length = random.randrange(10, 20)
    s = ""
    for _ in range(length):
        codepoint = random.randint(97, 122)
        s += chr(codepoint)
    return s

def delay_random_time():
    delay_seconds = random.uniform(1, 5)
    time.sleep(delay_seconds)

def client_thread(prefix, host, port):
    """Thread function to handle a single client connection and sending."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        print(f"{prefix}: Connected to {host}:{port}")
    except Exception as e:
        print(f"{prefix}: Could not connect to {host}:{port} - {e}")
        return

    try:
        while True:
            string_to_send = f"{prefix}: {random_string()}"
            string_bytes = string_to_send.encode()

            # Send data in chunks if necessary
            bytes_sent = 0
            while bytes_sent < len(string_bytes):
                try:
                    chunk = string_bytes[bytes_sent:]
                    sent = s.send(chunk)
                    bytes_sent += sent
                except Exception as e:
                    print(f"{prefix}: Error sending message - {e}")
                    s.close()
                    return

            delay_random_time()
    except KeyboardInterrupt:
        print(f"{prefix}: Client shutting down...")
    finally:
        s.close()

def main(argv):
    try:
        prefix = argv[1]
        host = argv[2]
        port = int(argv[3])
        num_clients = int(argv[4]) if len(argv) > 4 else 1
    except:
        usage()
        return 1

    # Generate unique prefixes for multiple clients
    prefixes = [f"{prefix}_{i}" for i in range(num_clients)]

    # Create and start a thread for each client
    threads = []
    for p in prefixes:
        thread = threading.Thread(target=client_thread, args=(p, host, port))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
