import json
import socket
import sys
import threading
import time

from chatui import init_windows, read_command, print_message, end_windows

so = socket.socket()

def runner():
    buffer = b''

    def get_next_packet() -> dict:
        nonlocal buffer
        if len(buffer) >= 2:
            json_len = int.from_bytes(buffer[:2])
            if len(buffer) >= json_len + 2:
                json_str = buffer[2:2+json_len]
                buffer = buffer[2+json_len:]
                return json.loads(json_str.decode())
        return None

    def handle_packets():
        while True:
            packet = get_next_packet()
            if not packet:
                return
            type = packet["type"]
            if type == "chat":
                print_message(f"{packet["nick"]}: {packet["message"]}")
            elif type == "join":
                print_message(f"*** {packet["nick"]} has joined the chat")
            elif type == "leave":
                print_message(f"*** {packet["nick"]} has left the chat")
            else:
                assert False

    while True:
        data = so.recv(1024)
        buffer += data
        handle_packets()

def send_packet(msg):
    data = json.dumps(msg).encode()
    buffer = b''
    buffer += len(data).to_bytes(2)
    buffer += data
    so.sendall(buffer)

def main(argv):
    try:
        nickname = argv[1]
        host = argv[2]
        port = int(argv[3])
    except:
        usage()
        return 1

    so.connect((host, port))
    send_packet({"type": "hello", "nick": nickname})

    init_windows()

    t1 = threading.Thread(target=runner, daemon=True)
    t1.start()

    while True:
        try:
            command = read_command("Enter message > ")
            if command:
                if command == "\q":
                    so.close()
                    return 0
                send_packet({"type":"chat", "nick": nickname, "message": command})
                print_message(f">>> {command}")
        except:
            break


    end_windows()

def usage():
    print("usage: chat_client.py nickname server port", file=sys.stderr)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
