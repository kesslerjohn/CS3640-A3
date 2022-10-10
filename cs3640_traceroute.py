import socket
import dpkt
import cs3640_ping
import sys

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

if __name__ == "__main__":
    main()