# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select

def run_server(port):
    listener_so = socket.socket()
    listener_so.bind(('', port))
    listener_so.listen()

    read_set = {listener_so}
    while True:
        read, _, _ = select.select(read_set, {}, {})
        for r in read:
            if r == listener_so:
                so, connection_info = r.accept()
                read_set.add(so)
                print(f"{connection_info}: connected")
            else:
                data = r.recv(1024)
                if len(data) == 0:
                    print(f"{connection_info}: disconnected")
                    read_set.remove(r)
                else:
                    print(f"{connection_info}: {data}")


#--------------------------------#
# Do not modify below this line! #
#--------------------------------#

def usage():
    print("usage: select_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
