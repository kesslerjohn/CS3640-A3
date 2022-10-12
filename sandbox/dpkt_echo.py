import socket
import dpkt

echo = dpkt.icmp.ICMP.Echo()
echo.id = 0x81
echo.seq = 0x7E

echo.data = str.encode('hello world')

print(echo)

icmp = dpkt.icmp.ICMP()
icmp.type = dpkt.icmp.ICMP_ECHO

icmp.data = echo

print(icmp)

s = socket.socket(socket.AF_INET, socket.SOCK_RAW, dpkt.ip.IP_PROTO_ICMP)
s.connect(('127.0.0.1',1))
s.send(str.encode(str(icmp)))
