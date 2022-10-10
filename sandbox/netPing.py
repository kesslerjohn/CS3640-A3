import socket
import dpkt

'''
pseudocode for sending icmp echo

def send_icmp_echo(socket, payload, id, seq, destination):
    echo = dpkt.icmp.ICMP.Echo()
    echo.id = id
    echo.seq = seq
    echo.data = payload
    socket.send

'''

def send_icmp_echo(socket, payload, id, seq, destination):
    echo = dpkt.icmp.ICMP.Echo()
    echo.id = id
    echo.seq = seq
    echo.data = payload
    socket.sendto(str.encode(payload), destination)