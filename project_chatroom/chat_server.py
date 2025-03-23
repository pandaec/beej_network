# Example usage:
#
# python chat_server.py 3490

import sys
import socket
import select
import json

read_set = set()
write_set = set()
write_buffer = {}
read_buffer = {}
so_info = {}

def run_server(port):
    listener_so = socket.socket()
    listener_so.bind(('', port))
    listener_so.listen()
    read_set.add(listener_so)

    while True:
        read, write, _ = select.select(read_set, write_set, {}, 1)
        for r in read:
            try:
                if r == listener_so:
                    so, connection_info = r.accept()
                    read_set.add(so)
                    write_set.add(so)
                    read_buffer[so] = b''
                    write_buffer[so] = b''
                    print(f"{connection_info}: connected")
                else:
                    data = r.recv(1024)
                    if len(data) == 0:
                        print(f"{connection_info}: disconnected")
                        read_set.remove(r)
                        write_set.remove(r)
                        del so_info[so]
                    else:
                        print(f"{connection_info}: {data}")
                        read_buffer[r] += data
                        handle_packets(r)
            except socket.error as e:
                boardcast_packet({"type": "leave", "nick": so_info[r]["nick"]})
                remove_socket(r)
                continue

        for w in write:
            try:
                if w in write_buffer:
                    # Race condition here
                    buf = write_buffer[w]
                    if len(buf) > 0:
                        w.sendall(buf)
                        write_buffer[w] = b''
            except socket.error as e:
                boardcast_packet({"type": "leave", "nick": so_info[w]["nick"]})
                remove_socket(w)
                continue
                    

def get_next_packet(so) -> dict:
    if read_buffer[so]:
        buf = read_buffer[so]
        if len(buf) >= 2:
            json_len = int.from_bytes(buf[:2])
            if len(buf) >= json_len + 2:
                json_str = buf[2:2+json_len]
                read_buffer[so] = buf[2+json_len:]
                return json.loads(json_str.decode())
    return None

def handle_packets(so):
    while True:
        packet = get_next_packet(so)
        if not packet:
            return
        type = packet["type"]
        if type == "hello":
            nickname = packet["nick"]
            so_info[so] = {"nick": nickname}
            pkt = {"type": "join", "nick": nickname}
            boardcast_packet(pkt)
        elif type == "chat":
            message = packet["message"]
            pkt = {"type": "chat", "nick": so_info[so]["nick"], "message": message}
            boardcast_packet(pkt, {so})
        else:
            assert False

def boardcast_packet(msg, skip={}):
    data = json.dumps(msg).encode()
    for so, buf in write_buffer.items():
        if so in skip:
            continue
        buf += len(data).to_bytes(2)
        buf += data
        write_buffer[so] = buf

def remove_socket(so):
    read_set.remove(so)
    write_set.remove(so)
    del read_buffer[so]
    del write_buffer[so]
    del so_info[so]

def usage():
    print("usage: chat_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
