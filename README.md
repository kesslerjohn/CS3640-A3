CS:3640 Assignment 3
====================
Members: Kessler, McKay, Scudiero, Singh
----------------------------------------

This repository is for the collaboration and submission of Assignment 3 for
Introduction to Networks and Their Applications. The assignment involves
reimplementation of simple programs to mimic the basic functionality of widely
used programs such as **ping** and **traceroute**.

Functions to implement:
-----------------------
* make_icmp_socket(ttl, timeout):
    + `Description to be added`.
    + Resources:
        - [introduction to socket programming](https://realpython.com/python-sockets/#background)
            * It may be worth the time to look through this tutorial and perhaps
            implement a chunk of it as practice. It seems to provide a means
            of gaining some experience in terms of working with the objects
            required for this assignment.
            * [Berkley sockets | Wikipedia](https://en.wikipedia.org/wiki/Berkeley_sockets#bind)
        - [socket API (creating sockets)](https://docs.python.org/3/library/socket.html#creating-sockets)
        - [setting socket options](https://www.ibm.com/docs/en/i/7.2?topic=ssw_ibm_i_72/apis/ssocko.htm)
* send_icmp_echo(socket,payload,id,seq,destination):
    + `Description to be added`.
    + Resources:
        - [ICMP echo dpkt](https://jon.oberheide.org/blog/2008/08/25/dpkt-tutorial-1-icmp-echo/)
        - [socket.sendto()](https://docs.python.org/3/library/socket.html#socket.socket.sendto)
* recv_icmp_response():
    + `Description to be added`.
    + Resources:
        - [socket.recvfrom()](https://docs.python.org/3/library/socket.html#socket.socket.recvfrom)

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