CS:3640 Assignment 3
====================
Members: Kessler, McKay, Scudiero, Singh
----------------------------------------

This repository is for the collaboration and submission of Assignment 3 for
Introduction to Networks and Their Applications. The assignment involves
reimplementation of simple programs to mimic the basic functionality of widely
used programs such as **ping** and **traceroute**.


Ping
----

An implementation of the ping program will make use of the **time**, **dpkt**,
and **socket** python modules. The following methods will be constructed and
leveraged within a file labeled "**cs3640-ping.py**"

### Functions to implement:
* `make_icmp_socket(ttl, timeout)`:
    + A method that creates a raw socket for use with the ICMP protocol. The
    socket should have the `timeout` and `ttl` options set to the values of the
    input arguments. The method should return the created socket.
    + Resources:
        - [introduction to socket programming](https://realpython.com/python-sockets/#background)
            * It may be worth the time to look through this tutorial and perhaps
            implement a chunk of it as practice. It seems to provide a means
            of gaining some experience in terms of working with the objects
            required for this assignment.
            * [Berkley sockets | Wikipedia](https://en.wikipedia.org/wiki/Berkeley_sockets#bind)
        - [socket API (creating sockets)](https://docs.python.org/3/library/socket.html#creating-sockets)
        - [setting socket options](https://www.ibm.com/docs/en/i/7.2?topic=ssw_ibm_i_72/apis/ssocko.htm) 
        - [socket types](https://www.ibm.com/docs/en/aix/7.1?topic=protocols-socket-types)
* `send_icmp_echo(socket,payload,id,seq,destination)`:
    + A method which leverages the **dpkt** module to craft and send an ICMP
    echo packet. The packet should have it's `payload`, `id`, and `seq` set to
    the values of the corresponding input arguments. Use the input `socket` to
    send the created packet to the specified `destination`. Despite it's
    popularity, the documentation for **dpkt** isn't good. Be sure to consider
    the following resources.
    + Resources:
        - [ICMP echo dpkt](https://jon.oberheide.org/blog/2008/08/25/dpkt-tutorial-1-icmp-echo/)
        - [socket.sendto()](https://docs.python.org/3/library/socket.html#socket.socket.sendto)
* `recv_icmp_response()`:
    + A method that creates a new raw socket for use with the ICMP protocol.
    It should receive any incoming ICMP packets. This method will return any
    packet that arrives on this socket.
    + Resources:
        - [socket.recvfrom()](https://docs.python.org/3/library/socket.html#socket.socket.recvfrom)

Use these functions to build a program which takes some destination, number of
packets, and a time-to-live value as arguments.

#### The prompt input is as follows:
* `sudo python3 cs3640-ping.py -destination <ipv4 destination> -n <integer> -ttl <numeric>`

#### The output should be similar to:
* `destination = 8.8.8.8; icmp_seq = 0; icmp_id = 0; ttl = 100; rtt = 14.0 ms`
* `destination = 8.8.8.8; icmp_seq = 1; icmp_id = 1; ttl = 100; rtt = 14.2 ms`
* `destination = 8.8.8.8; icmp_seq = 2; icmp_id = 2; ttl = 100; rtt = 14.5 ms`
* `Average rtt: 14.2 ms; 3/3 successful pings.`


Traceroute
----------

Leverage the functions implemented in **ping** to create a traceroute of
addresses that are used to transfer communication to some destination. The
algorithm of discovery is as follows:

* The user invokes the program and specifies a destination IP
* The program sends a data packet towards the target with the TTL value set to
"1". When this happens, the first router in the path will decrement the value
by 1, which should trigger a TTL exceeded message that gets sent back to the
host on which the program is running. The program will record the IP of the
device which sent this TTL exceeded message. This device is the first hop on
the path to the destination IP
* With details of the first hop in hand, the program will increase the TTL
value to "2". That first router in the path will still decrement the value by
1, but because the TTL will no longer drop to zero right out of the gate, the
packet can live on for one more hop. Once the TTL value does hit zero (in this
case, at the second router in the path), another TTL exceeded message should be
generated and passed back to the program
* The process repeats itself, with the program increasing the TTL by 1 each
time, until the destination is reached or an upper limit of hops is hit
(specified by a `n_hops` command line argument).
* When finished, the program prints all the hops in the path, along with the
amount of time it took to each hop and back.

#### The program should be exeecuted by the following command:
* `sudo python3 cs3640-traceroute.py -destination 8.8.8.8 -n_hops 3`

#### The output should be similar to:
* `destination = 8.8.8.8; hop 1 = 128.255.44.1; rtt = 0.50 ms`
* `destination = 8.8.8.8; hop 2 = 128.255.2.67; rtt = 0.72 ms`
* `destination = 8.8.8.8; hop 3 = 198.49.182.135; rtt = 4.51 ms`

Extraneous Notes:
-----------------

Be sure to be thorough in git usage; adhere to quality standards in terms of
commit messages. If peer/pair programming, be sure to note who co-authored the
changes.

A sandbox folder has been created to house various tutorial and experimental
implementations. Currently a file named echo_server.py exists which is an
implementation of the echo_server function from the python socket tutorial.
It's worth taking a look at as some details and quirks are elaborated upon
within its code comments. To run and test the program, run echo_server.py
with Python, and run curl to connect to the localhost.
  i.e., `python3 echo_server.py; curl localhost:port` where the port is
  whatever is declared in the file.
