#!/usr/bin/env python

#la ligne supérieur permet quand on lance le programme de le charger
#dans python. (en plus comme ça on sait que c'est du python directement)

#voir docu détaillée dans le word réseau_2 - proxy

import socket, sys
from _thread import *
import time


try:
    listening_port = int(input("[*] Enter listening port number: "))
except KeyboardInterrupt:
    print("\n Manual shutdown, application exiting")
    sys.exit()

max_conn = 5
buffer_size = 4096 #pour la fonction .recv(bufferSize)

def start():
    try:
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #initiate socket
        s.bind(('',listening_port)) #bind socket for listen
        s.listen(max_conn) #start listening for incomming coonnections
        print("socket initialisé \n serveur démarré [ %d]\n", listening_port)
    except Exception as e:
            print("Echec de l'initialisation du socket ")
            sys.exit(2)

    while 1:
        try:
            conn, addr = s.accept() #accept connection from client browser
            data = conn.recv(buffer_size)#receive client data
            print(data)
            start_new_thread(conn_string, (conn, data, addr)) #start a thread
        except KeyboardInterrupt:
            s.close()
            print("\n proxy server shutting down as requested")
            sys.exit(1)


def conn_string(conn, data, addr):
    
    try:
        data_str = data.decode()
        first_line = data_str.split('\n')[0]
        print(first_line) #debug
        
        url = first_line.split(' ')[1]
        print(url) #debug
        http_pos = url.find("://") #find position of ://
        if (http_pos==-1):
            temp = url
        else:
            temp = url[(http_pos+3):] #get the rest of the url
        port_pos = temp.find(":") #find position of the port (if any)
        webserver_pos = temp.find("/") #find the end of webserver
        if (webserver_pos == -1):
            webserver_pos = len(temp)
        else:
            pass

        #this block is for getting the port and webserver
        webserver = ""
        port= -1
        if (port_pos==-1 or webserver_pos < port_pos):
            port = 80
            webserver =temp[:webserver_pos]
        else:
            port = int(temp[(port_pos+1):]) #ici j'ai du supprimer une position de liste qui n'avait pas de sens
            webserver = temp[:port_pos]


        proxy_server(webserver, port, conn, addr, data)
    except Exception as e:
        print("error occured in Function 2") #debug
        pass


def proxy_server(webserver, port, conn, addr, data):
    print("fct 3")
    print(type(data))
    #print("webserver = ",webserver, ", port = ", port, ", conn = ",conn,", addr = ",addr,", data = ",data)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((webserver, port))
        s.send(data)

        while 1:
            reply = s.recv(buffer_size)
            print("reply = ",reply)
            
            print(type(reply), len(reply)) #debug
            
            if(len(reply)> 0):
                conn.send(reply)

                #dar= float(len(reply))
                #dar= float(dar / 1024)
                #dar= "%.3s" % (str(dar))
                #dar = "%s KB" % (dar)
                print("request Done")
            else:
                print("break in Function 3") #debug
                break
        s.close()

        conn.close()
    except socket.error:
        print("socket error in Function 3") #debug
        s.close()
        conn.close()
        sys.exit(1)

start()




















            
