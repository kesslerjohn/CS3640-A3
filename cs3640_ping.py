import socket
import dpkt
import sys


def make_icmp_socket(ttl, timeout):
    s1 = socket.AF_INET
    s2 = socket.SOCK_RAW
    s3 = dpkt.ip.IP_PROMO_ICMP
    sock = socket.socket(s1, s2, s3)
    sock.setsockopt(socket.IP_TTL, ttl)

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

def main():
    n = len(sys.argv)
    if (n <= 1):
        print("")
    destination = n[2]
    payload = n[3]
    ttl = n[4] #todo check the indices of these command line args - John
    

    id = 0x81
    seq = 0x7E
    timeout = ttl*1000 #Is this right? - John
    skt = make_icmp_socket(ttl, timeout)
    send_icmp_echo(skt, payload, id, seq, destination)

if __name__ == "__main__":
    main()