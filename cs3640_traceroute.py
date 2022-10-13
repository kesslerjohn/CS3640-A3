import socket
import dpkt
import cs3640_ping
import sys
import time

def main():
    args = sys.argv
    if (len(args) < 2):
        print("No command line arguments given")
        return 1
    else:
        try:
            dst = args[args.index("-destination")+1]
            num = args[args.index("-n_hops")+1]
        except ValueError:
            print("Error: some parameters missing.") #todo add a while loop to ping forever if
                                                     #no value is given for n_hops. - John
            return 1
    ttl = 1

    while (ttl <= int(num)):
        sock = cs3640_ping.make_icmp_socket(ttl, ttl*1000)
        startTime = time.time()
        cs3640_ping.send_icmp_echo(sock, "Hello World", 0x81, 0x7E, dst)
        recvr = cs3640_ping.recv_icmp_response()
        endTime = time.time()
        RTT = (endTime - startTime) * 1000
        round(RTT, 4)
        addr = recvr[1]
        print("destination = " + dst + "; hop " + ttl + " = " + addr + "; rtt = " + RTT + " ms")
        if (addr == dst):
            break
        else:
            ttl = ttl + 1

    return 0
if __name__ == "__main__":
    main()
