import socket as socket
from sys import argv
import argparse

#this will be checked and created if hostname and addres is not inTable in rs

argParser = argparse.ArgumentParser(description="Top level DNS")
argParser.add_argument('port', type=int, help='Port to SERVER', action='store')
args = argParser.parse_args()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("[S]: Server connection established")


address = ('', args.port)
s.bind(address)
s.listen(5)

host = socket.gethostname()
print("[S]: Server's hostname: {}".format(host))
IP_LOCAL_HOST = (socket.gethostbyname(host))
print("[S]: Server's IP: {}".format(IP_LOCAL_HOST))

c, addr = s.accept()
print("[S]: Got a client from: {}".format(addr))

inTable = False

with c:

    while True:
        
        temp = c.recv(512)
        temp = temp.decode('utf-8')
        
        if not temp:
            break


        for query in open("PROJI-DNSTS.txt", 'r'):
            parse_query = query.split()
            if parse_query[0].lower() == temp.lower():
                c.sendall(query.encode('utf-8'))
                inTable = True
                break


        if not inTable:
            response = temp + " - Error:HOSTNOTinTable"
            c.sendall(response.encode('utf-8'))
        inTable = False


#close server
s.close()
exit()