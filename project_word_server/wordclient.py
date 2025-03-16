import sys
import socket

# How many bytes is the word length?
WORD_LEN_SIZE = 2

def usage():
    print("usage: wordclient.py server port", file=sys.stderr)

packet_buffer = b''

def get_next_word_packet(s):
    """
    Return the next word packet from the stream.

    The word packet consists of the encoded word length followed by the
    UTF-8-encoded word.

    Returns None if there are no more words, i.e. the server has hung
    up.
    """

    global packet_buffer

    # TODO -- Write me!
    while True:
        if len(packet_buffer) > WORD_LEN_SIZE:
            n = int.from_bytes(packet_buffer[:WORD_LEN_SIZE], "big")
            if len(packet_buffer) >= n + WORD_LEN_SIZE:
                packet = packet_buffer[:n+WORD_LEN_SIZE]
                packet_buffer = packet_buffer[n+WORD_LEN_SIZE:]
                return packet

        data = s.recv(1)
        if len(data) == 0:
            return None
        packet_buffer = packet_buffer + data

# Alternative implementation
def get_next_word_packet_1(s):
    """
    Return the next word packet from the stream.

    The word packet consists of the encoded word length followed by the
    UTF-8-encoded word.

    Returns None if there are no more words, i.e. the server has hung
    up.
    """

    global packet_buffer

    # First, try to get the word length (2 bytes)
    while len(packet_buffer) < WORD_LEN_SIZE:
        chunk = s.recv(1)
        if not chunk:  # Server hung up
            return None
        packet_buffer += chunk

    # Extract the word length
    word_len = int.from_bytes(packet_buffer[:WORD_LEN_SIZE], "big")

    # Now make sure we have the complete word
    while len(packet_buffer) < WORD_LEN_SIZE + word_len:
        chunk = s.recv(1)
        if not chunk:  # Server hung up
            return None
        packet_buffer += chunk

    # Extract the complete packet (length + word)
    word_packet = packet_buffer[:WORD_LEN_SIZE + word_len]

    # Update the buffer to remove the packet we just processed
    packet_buffer = packet_buffer[WORD_LEN_SIZE + word_len:]

    return word_packet



def extract_word(word_packet):
    """
    Extract a word from a word packet.

    word_packet: a word packet consisting of the encoded word length
    followed by the UTF-8 word.

    Returns the word decoded as a string.
    """

    # TODO -- Write me!
    word = word_packet[WORD_LEN_SIZE:].decode()
    return word 

# Do not modify:

def main(argv):
    try:
        host = argv[1]
        port = int(argv[2])
    except:
        usage()
        return 1

    s = socket.socket()
    s.connect((host, port))

    print("Getting words:")

    while True:
        word_packet = get_next_word_packet(s)

        if word_packet is None:
            break

        word = extract_word(word_packet)

        print(f"    {word}")

    s.close()

if __name__ == "__main__":
    sys.exit(main(sys.argv))