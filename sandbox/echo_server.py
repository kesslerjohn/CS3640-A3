import socket

HOST = "127.0.0.1"
PORT = 65432

def echo_server(host,port):
    #context manager type:
    # https://docs.python.org/3/reference/datamodel.html#context-managers
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print("Connected by " + str(addr))
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)

''' Note that the context manager type, above, can sometimes be too rigid in
this context. Should an error in the code within the block be present the
socket may not be closed once the code fails to be interpreted/compiled. Any
subsequent runs of the file will fail on account of this socket being open.
Thus, after a failed run, be sure to add the code s.close() near the top of the
block in question, where s is the name of the instantiated socket.'''

#Same function without the context manager syntactic abstraction:
def echo_server(host,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    response = None
    try:
        s.bind((host,port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print("Connected by " + str(addr))
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                else:
                    response = data.decode()
                    response = "Data received: " + response
                    conn.sendall(response.encode())
                #conn.sendall(data)
    except OSError as msg:
        response = msg
        s.close() #may be redundant; "finally" may run regardless of exception.
    finally:
        s.close()
        s = None
    return response

'''The above implementation is equivalent to the first. Some research needs to
be put into what happens with the conn object created in the tuple of the
return of s.accept() with respect to it's usage with the "with" keyword:
- https://docs.python.org/3/library/socket.html#socket.socket.accept
- https://docs.python.org/3/whatsnew/2.6.html#pep-343-the-with-statement
'''

'''All if this is to say, should there be some error, such as a mispelling of
"data" within the method call conn.sendall(data), the socket will be occupied
for subsequent code runs for a certain duration. Calling s.close() at the top
of the block will expediate this process.'''

#Could also be shortcutted with a call to some function that simply closes
#the relevant socket.

def close_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return s.close()

close_server()
print(echo_server(HOST,PORT))