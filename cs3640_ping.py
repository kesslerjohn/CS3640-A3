import socket
import dpkt

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