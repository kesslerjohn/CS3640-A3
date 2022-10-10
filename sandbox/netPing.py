import socket
import dpkt
import sys

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
    args = sys.argv
    if (len(args) < 2):
        print("No command line arguments given")
        return 1
    else:
        try:
            dst = args[args.index("-destination")+1]
            ttl = args[args.index("-ttl")+1]
            num = args[args.index("-n")+1]
            print("Destination: {}\n".format(dst))
            print("Time to live: {}\n".format(ttl))
            print("Number of pings: {}\n".format(num))
        except ValueError:
            print("Error: some parameters missing.")


if __name__ == "__main__":
    main()