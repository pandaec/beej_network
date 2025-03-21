def string_to_number():
    x = "198.51.100.10"
    print([f'0x{int(x):02x}' for x in x.split(".")])
    y = (0xc6 << 24) | (0x33 << 16) | (0x64 << 8) | 0x0a
    print(f'0x{y:0x}')

def int_to_section():
    y = (0xc6 << 24) | (0x33 << 16) | (0x64 << 8) | 0x0a
    a = (y >> 24) & 0xff
    b = (y >> 16) & 0xff
    c = (y >> 8) & 0xff
    d = (y >> 0) & 0xff
    print(a,b,c,d)

def subnet_and_host():
    a = '198.51.100.10' # 198.51.100.10/24   Host 10 on subnet 198.51.100.0
    b = '10.121.2.17' # 10.121.2.17/16    Host 2.17 on subnet 10.121.0.0
    c = '10.121.2.68' # 10.121.2.68/28    Host 4 on subnet 10.121.2.64
    c_subnet = '10.121.2.64'

    ba = '.'.join([f'{int(x):08b}' for x in a.split('.')])
    bb = '.'.join([f'{int(x):08b}' for x in b.split('.')])
    bc = '.'.join([f'{int(x):08b}' for x in c.split('.')])
    bc_subnet = '.'.join([f'{int(x):08b}' for x in c_subnet.split('.')])

    print(ba)
    print(bb)
    print()
    print(bc)
    print(bc_subnet)

def subnet_mask():
    one_10 = (1 << 10) - 1
    print(len(f'{one_10:0b}'), f'{one_10:0b}')
    mask = (1 << 24) - 1
    print(len(f'{mask:0b}'), f'{mask:0b}')


def find_subnet_mask():
    # The left subnet will be 192.168.0.0/24. The right subnet will be 192.168.1.0/24.
    a = '192.168.0.0'
    b = '192.168.1.0'
    left = '.'.join([f'{int(x):08b}' for x in a.split('.')])
    right = '.'.join([f'{int(x):08b}' for x in b.split('.')])
    print(left)
    print(right)

string_to_number()
print("===")
int_to_section()
print("===")
subnet_and_host()
print("===")
subnet_mask()
print("===")
find_subnet_mask()