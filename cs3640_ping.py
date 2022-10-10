import socket
import dpkt

'''
Some additional code pieces:
for setting socket ttl: 
    sock.IP_TTL = ttl

for creating a socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, dpkt.ip.IP_PROTO_ICMP)
'''

def make_icmp_socket(ttl, timeout):
    s1 = socket.AF_INET
    s2 = socket.SOCK_RAW
    s3 = dpkt.ip.IP_PROMO_ICMP
    sock = socket.socket(s1, s2, s3)

def send_icmp_echo(sock, payload, id, seq, destination):
    echo = dpkt.icmp.ICMP.Echo()
    echo.id = id
    echo.seq = seq
    echo.data = payload

    icmp = dpkt.icmp.ICMP()
    icmp.type = dpkt.icmp.ICMP_ECHO
    icmp.data = echo

    #sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, dpkt.ip.IP_PROTO_ICMP)
    sock.connect(destination, 1)
    sent = sock.send(str(icmp))
