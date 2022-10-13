import socket
import dpkt
import sys
import threading
import time

def make_icmp_socket(ttl, timeout):
    s1 = socket.AF_INET
    s2 = socket.SOCK_RAW
    s3 = socket.IPPROTO_ICMP #why isn't socket.IPPROTO_ICMP being used here? #
    sock = socket.socket(s1, s2, s3)
    sock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
    #sock.setsockopt(socket.IP_TTL, ttl) # !! This method needs three arguments.
    return sock

def send_icmp_echo(sock, payload, id, seq, destination):
    echo = dpkt.icmp.ICMP.Echo()
    echo.id = id
    echo.seq = seq
    if type(payload) == str:
        payload = str.encode(payload)
    elif type(payload) != bytes:
        return False

    echo.data = payload

    icmp = dpkt.icmp.ICMP()
    icmp.type = dpkt.icmp.ICMP_ECHO #this seems to change nothing; default is ICMP_ECHO!
    icmp.data = echo

    sock.connect((destination, 1)) #comment this line...
    sent = sock.send(bytes(icmp)) #... and this line...
    #sent = sock.sendto(str.encode(str(icmp)),(destination,443)) # ... and uncomment this...
    # ... To allow a means to define a port.
    return sent

def recv_icmp_response(buffer_size = 1024):
    socket_family = socket.AF_INET
    socket_type = socket.SOCK_RAW
    socket_protocol = socket.IPPROTO_ICMP
    s = socket.socket(socket_family,socket_type,socket_protocol)
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
            print("Error: some parameters missing.") #todo add a while loop to ping forever if
                                                     #no value is given for n_hops. - John
            return 1
    id = 0x81
    seq = 0x7E
    timeout = ttl*1000 #Is this right? - John
    for i in range(num):
        skt = make_icmp_socket(ttl, timeout)
        thread1 = serverThread(1)
        thread2 = clientThread(2,skt,'Hello world', id, seq, dst)
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        #print(thread1.packet)
        print(thread1.packet)
        print(thread1.duration)
    return 0

if __name__ == "__main__":
    main()
