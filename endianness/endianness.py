a = 3490
bigbytes = a.to_bytes(2, "big")
littlebytes=  a.to_bytes(2, "little")
for b in bigbytes:
    print(f"{b:02X}")
for b in littlebytes:
    print(f"{b:02X}")


b = 0x0102
bytes = b.to_bytes(2, "big")
print(bytes)
v = int.from_bytes(bytes, "big")
print(f"{v:04x}")
