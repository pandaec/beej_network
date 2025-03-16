def is_valid(n):
    with open(f"tcp_data/tcp_addrs_{n}.txt", "r") as fp:
        arr = fp.readline().split(" ")
        source_ip = b''.join([int(x).to_bytes(1) for x in arr[0].split(".")])
        target_ip = b''.join([int(x).to_bytes(1) for x in arr[1].split(".")])

    with open(f"tcp_data/tcp_data_{n}.dat", "rb") as fp:
        tcp_data = fp.read()
        tcp_length = len(tcp_data)
        tcp_file_cksum = int.from_bytes(tcp_data[16:18])
        tcp_zero_cksum = tcp_data[:16] + b'\x00\x00' + tcp_data[18:]
        if len(tcp_zero_cksum) % 2 == 1:
            tcp_zero_cksum += b'\x00'

    ip_header = b''
    ip_header += source_ip
    ip_header += target_ip
    ip_header += b'\x00\x06'
    ip_header += tcp_length.to_bytes(2)

    data = ip_header + tcp_zero_cksum
    total = 0
    offset = 0
    while offset < len(data):
        word = int.from_bytes(data[offset:offset+2])
        offset += 2
        total += word
        # &0xffff to convert it to 16-bit integer
        total = (total & 0xffff) + (total >> 16) # carry around
    cksum = (~total) & 0xffff # one's complement
    return cksum == tcp_file_cksum

for i in range(0, 10):
    print("PASS" if is_valid(i) else "FAIL")