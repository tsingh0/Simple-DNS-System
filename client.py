import socket as socket
from sys import argv
import argparse


class table:
    def __init__(self, hostname, IP_address, flag):
        self.hostname = hostname
        self.IP_address = IP_address
        self.flag = flag


#use argparse to parse the aruments so it easier to understand and use
argParser = argparse.ArgumentParser()

argParser.add_argument('-f',type=str, help='Source file where hostname strings will be queried',
                    default='PROJI-HNS.txt', action='store', dest='inputFile')

argParser.add_argument('-o',type=str, help='Destination file for results', default='RESOLVED.txt',
                    action='store', dest='outputFile')



#the following three are the command line arguments
argParser.add_argument('rsHostname', type=str, help='The domain/ip address of machine running RS', action='store')

argParser.add_argument('rs_listenport', type=int, help='The port number to connect the rs server', action='store')

argParser.add_argument('ts_listenport', type=int, help='The port number to connect the ts server', action='store')

args = argParser.parse_args() 

#here we will open the rs server 
######################################################################rs server code
try:
    RS_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[C]: RS socket connection established")

except socket.error as error:
    print('socket error: {} \n'.format(error))
    exit()

RS_address = (args.rsHostname, args.rs_listenport)
RS_SOCKET.connect(RS_address)
# it should now be connected
####################################################################

#at this point we dont need a connection for TS so we are going to make a flag and make it false 
TS_flag = False

#starting reading from queries files
with open(args.outputFile, 'w') as writeOutToFile: #we will write to outputFile

    for line in open(args.inputFile, 'r'):  #we willl read from inputFile

        line = line.strip() #cleans up the lines 

        if line:
            RS_SOCKET.sendall(line.encode('utf-8'))

            response = RS_SOCKET.recv(512)
            response = response.decode('utf-8')

            parse_responses = response.split()
            temp_table = table(parse_responses[0], parse_responses[1], parse_responses[2])

            if temp_table.flag == "NS":

                ###########################################################ts server code
                #now we will connect to the ts server
                if not TS_flag:
                    try:
                        TS_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        print("[C]: TS socket connection established")
                    except socket.error as error:
                        print('socket error: {} \n'.format(error))
                        exit()

                    TS_address = (temp_table.hostname, args.ts_listenport)
                    TS_SOCKET.connect(TS_address)
                ##################################################################


                    TS_flag = True #established connection so flag is now true


                TS_SOCKET.sendall(line.encode('utf-8')) #sends info to server
                response = TS_SOCKET.recv(512)           #holds response from server
                response = response.decode('utf-8')             #decodes response

                #following lines split the reponse stores in respective place in table
                parse_responses = response.split()              
                temp_table.hostname = parse_responses[0]
                temp_table.IP_address = parse_responses[1]
                temp_table.flag = parse_responses[2]


            writeOutToFile.write(temp_table.hostname + ' ')
            writeOutToFile.write(temp_table.IP_address + ' ')
            if temp_table.flag == "Error:HOSTNOTFOUND": temp_table.flag = "Error:HOST NOT FOUND"
            writeOutToFile.write(temp_table.flag + '\n')

TS_SOCKET.close()
RS_SOCKET.close()
exit()