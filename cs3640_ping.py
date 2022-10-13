import socket
import dpkt
import sys
import threading
import time

def make_icmp_socket_helper():
    socket_family = socket.AF_INET
    socket_type = socket.SOCK_RAW
    socket_protocol = socket.IPPROTO_ICMP
    return socket.socket(socket_family, socket_type, socket_protocol)

def make_icmp_socket(ttl, timeout):
    s = make_icmp_socket_helper()
    s.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
    s.settimeout(timeout)
    return s

def send_icmp_echo(sock, payload, id, seq, destination):
    #ICMP.Echo() extends the dpkt.icmp class by adding more header information:
    echo = dpkt.icmp.ICMP.Echo()
    #   New header content: (('id', 'H', 0), ('seq', 'H', 0))
    echo.id = id
    echo.seq = seq

    if type(payload) == str:
        payload = str.encode(payload)
    elif type(payload) != bytes:
        try:
            payload = str.encode(str(payload))
        except:
            raise ValueError("Incorrect payload datatype within \
                            send_icmp_echo() call")

    #It seems that the data attribute of this object is inherently an empty...
    #...bit string. Overwrite it with a new bit string:
    echo.data = payload

    #Create non-echo headers:
    icmp = dpkt.icmp.ICMP()
    #   New header content: ('type', 'B', 8),('code', 'B', 0),('sum', 'H', 0)
    icmp.type = dpkt.icmp.ICMP_ECHO #this seems to change nothing; defaulted

    #Once again, it seems that the data attribute here behaves as Echo()'s:
    icmp.data = echo

    #Connect the socket and send the packet. Following comments indicate how
    #...To extend this to allow port parameterization.
    sock.connect((destination, 1)) #comment this line...
    sent = sock.send(bytes(icmp)) #... and this line...
    #sent = sock.sendto(str.encode(str(icmp)),(destination,443)) # ... and uncomment this...
    # ... To allow a means to define a port.
    return sent

def recv_icmp_response(buffer_size = 1024):
    s = make_icmp_socket_helper()
    return s.recvfrom(buffer_size)


def main():
    class serverThread(threading.Thread):
        def __init__(self, threadID):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.packet = None
            self.duration = None
        def run(self):
            start_time = time.time()
            self.packet = recv_icmp_response()
            self.duration = (time.time() - start_time) * 1000

    class clientThread(threading.Thread):
        def __init__(self, threadID, sock, payload, id, seq, destination):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.packet = None
            self.socket = sock
            self.payload = payload
            self.id = id
            self.seq = seq
            self.destination = destination
        def run(self):
            self.packet = send_icmp_echo(self.socket, self.payload , self.id, self.seq, self.destination)

    args = sys.argv
    if (len(args) < 2):
        print("No command line arguments given")
        return 1
    else:
        try:
            dst = args[args.index("-destination")+1]
            ttl = int(args[args.index("-ttl")+1])
            num = int(args[args.index("-n")+1])
        except ValueError:
            print("Error: some parameters are incorrect or missing.")
            return 1
    id = 0x08
    seq = 0x0
    timeout = ttl*3 
    total_time = 0
    for i in range(num):
        skt = make_icmp_socket(ttl, timeout)
        thread1 = serverThread(1)
        thread2 = clientThread(2,skt,'Hello world', id, i, dst)
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        t = round(thread1.duration, 1)
        total_time += thread1.duration
        print("destination = {}, icmp_seq = {}, icmp_id = {}, ttl = {}, rtt = {} ms"
            .format(thread1.packet[1][0], i, id, ttl, t))
    avg_time = round((total_time/num), 3)
    print("Average rtt: " + str(avg_time))
    return 0

if __name__ == "__main__":
    main()
