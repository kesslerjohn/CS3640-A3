import socket
import sys

#!! Defaults:
MESSAGE = "Hello World"
PORT = 65432
HOST = "127.0.0.1"

if len(sys.argv) >= 2:
    MESSAGE = sys.argv[1]
if len(sys.argv) >= 3:
    PORT = str(sys.argv[2])
if len(sys.argv) >= 4:
    HOST = sys.argv[3]

def echo_client(host,port,message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data = None
    try:
        s.connect((host,port))
        s.sendall(str.encode(message)) #need to encode the message as bytes
        data = s.recv(1024).decode() #need to decode the return message into a string
    except OSError as msg:
        #print(msg)
        data = msg
        s.close()
    finally:
        s.close()
        s = None
    return data

print(echo_client(HOST,PORT,MESSAGE))