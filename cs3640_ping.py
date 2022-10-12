import socket
import dpkt
import sys


def make_icmp_socket(ttl, timeout):
    s1 = socket.AF_INET
    s2 = socket.SOCK_RAW
    s3 = dpkt.ip.IP_PROTO_ICMP #why isn't socket.IPPROTO_ICMP being used here?
    sock = socket.socket(s1, s2, s3)
    sock.setsockopt(socket.IP_TTL, ttl)
    return sock

def send_icmp_echo(sock, payload, id, seq, destination):
    echo = dpkt.icmp.ICMP.Echo()
    echo.id = id
    echo.seq = seq
    echo.data = payload

    #https://dpkt.readthedocs.io/en/latest/_modules/dpkt/icmp.html
        #dpkt.icmp.ICMP() default headers are:
            #('type', 'B', 8),('code', 'B', 0),('sum', 'H', 0), which seem to be able
            #to be accessed and mutated as if class properties.

        #dpkt.icmp.ICMP.Echo() headers are defaulted to:
            #('id', 'H', 0), ('seq', 'H', 0)

    # Considering this much, I'm concerned as to where the payload is placed. I'm
    # also concerned that the payload received in this function, (and the argument given
    #to sock.send()), are being teated as strings as opposed to bytes.
    # --- Alan

    icmp = dpkt.icmp.ICMP()
    icmp.type = dpkt.icmp.ICMP_ECHO #this seems to change nothing; default is ICMP_ECHO!
    icmp.data = echo

    #sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, dpkt.ip.IP_PROTO_ICMP)
    sock.connect(destination, 1)
    sent = sock.send(str(icmp))

def recv_icmp_response(buffer_size = 1024):
    socket_family = socket.AF_INET
    socket_type = socket.SOCK_RAW #unsure why we are using raw...
    socket_protocol = socket.IPPROTO_ICMP
    s = socket.socket(socket_family,socket_type,socket_protocol)
    return s.recvfrom(buffer_size)

def main():
    args = sys.argv
    if (len(args) < 2):
        print("No command line arguments given")
        return 1
    else:
        try:
            dst = args[args.index("-destination")+1]
            ttl = args[args.index("-ttl")+1]
            num = args[args.index("-n")+1]
        except ValueError:
            print("Error: some parameters missing.") #todo add a while loop to ping forever if
                                                     #no value is given for n_hops. - John
            return 1
    id = 0x81
    seq = 0x7E 
    timeout = ttl*1000 #Is this right? - John
    for i in range(num):
        skt = make_icmp_socket(ttl, timeout)
        dst = recv_icmp_response()
        send_icmp_echo(skt, "Hello world", id, seq, dst)
    return 0

if __name__ == "__main__":
    main()
