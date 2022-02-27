import socket as socket
from sys import argv
import argparse

#formats commandquery arguments
argParser = argparse.ArgumentParser(description="Root DNS")
argParser.add_argument('port', type=int, help='Port to onnect to server',action='store')
args = argParser.parse_args()

#create socket connection

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("[S]: Server connection established")

address = ('', args.port)
s.bind(address)
s.listen(5)

hostname = socket.gethostname()
print("[S]: The Server's hostname: {}".format(hostname))
IP_LOCAL_HOST = (socket.gethostbyname(hostname))
print("[S]: The Server's IP: {}".format(IP_LOCAL_HOST))

c, addr = s.accept()
print("[S]: Request from client from: {}".format(addr))

#initially set table to false
inTable = False

with c:
    while True:

        #temp variable to hold data
        temp = c.recv(512)
        temp = temp.decode('utf-8')

        #if found
        if not temp:
            break

        for query in open("PROJI-DNSRS.txt", 'r'):
            parse_query = query.split()
            if parse_query[0].lower() == temp.lower():
                c.sendall(query.encode('utf-8'))
                inTable = True
                break

        if not inTable:
            for query in open("PROJI-DNSRS.txt", 'r'):
                parse_query = query.split()
                if parse_query[2] == "NS":
                    c.sendall(query.encode('utf-8'))
                    break
        #reset inTable for next temp
        inTable = False

s.close()
exit()