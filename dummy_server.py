#!/usr/bin/python

import socket
import signal
import urllib
import json
import pyautogui
import time

class Server:
 """ Class describing a simple HTTP server objects."""

 def __init__(self, port = 8000):
     """ Constructor """
     self.host = ''   # <-- works on all avaivable network interfaces
     self.port = port
     self.www_dir = 'www' # Directory where webpage files are stored

 def activate_server(self):
     """ Attempts to aquire the socket and launch the server """
     self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     try: # user provided in the __init__() port may be unavaivable
         self.socket.bind((self.host, self.port))

     except Exception as e:
         # store to user provideed port locally for later (in case 8080 fails)
         user_port = self.port
         self.port = 8080

         try:
             self.socket.bind((self.host, self.port))

         except Exception as e:
             self.shutdown()
             import sys
             sys.exit(1)

     self._wait_for_connections()

 def shutdown(self):
     """ Shut down the server """
     try:
         print("Shutting down the server")
         s.socket.shutdown(socket.SHUT_RDWR)

     except Exception as e:
         print("Warning: could not shut down the socket. Maybe it was already closed?",e)

 def _gen_headers(self,  code):
     """ Generates HTTP response Headers. Ommits the first line! """

     # determine response code
     h = ''
     if (code == 200):
        h = 'HTTP/1.1 200 OK\n'
     elif(code == 404):
        h = 'HTTP/1.1 404 Not Found\n'

     # write further headers
     current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
     h += 'Date: ' + current_date +'\n'
     h += 'Server: Simple-Python-HTTP-Server\n'
     h += 'Connection: close\n\n'  # signal that the conection wil be closed after complting the request

     return h

 def _wait_for_connections(self):
     """ Main loop awaiting connections """
     while True:
         self.socket.listen(3) # maximum number of queued connections

         conn, addr = self.socket.accept()
         # conn - socket to client
         # addr - clients address


         data = conn.recv(1024) #receive data from client
         string = bytes.decode(data) #decode it to string

         #determine request method  (HEAD and GET are supported)
         request_method = string.split(' ')[0]

         try:
             s = urllib.unquote(string.split()[1]).decode('utf8')
             ss = s.split('param=')[1]
             sss = json.loads(ss)
             print(sss)
             try:
                 w, h = pyautogui.size()
                 pyautogui.moveTo(int(sss["x"] * (float(w) / float(sss["w"]))),
                                  int(sss["y"] * (float(h) / float(sss["h"]))))
                 pyautogui.click()
             except:
                try:
                    pyautogui.press(sss["key"])
                except Exception as e:
                    print(e)
         except:
             pass


         #if string[0:3] == 'GET':
         if (request_method == 'GET') | (request_method == 'HEAD'):
             #file_requested = string[4:]

             # split on space "GET /file.html" -into-> ('GET','file.html',...)
             file_requested = string.split(' ')
             file_requested = file_requested[1] # get 2nd element

             #Check for URL arguments. Disregard them
             file_requested = file_requested.split('?')[0]  # disregard anything after '?'

             if (file_requested == '/'):  # in case no file is specified by the browser
                 file_requested = '/index.html' # load index.html by default

             file_requested = self.www_dir + file_requested

             ## Load file content
             try:
                 file_handler = open(file_requested,'rb')
                 if (request_method == 'GET'):  #only read the file when GET
                     response_content = file_handler.read() # read file content
                 file_handler.close()

                 response_headers = self._gen_headers( 200)

             except Exception as e: #in case file was not found, generate 404 page
                 response_headers = self._gen_headers( 404)

                 if (request_method == 'GET'):
                    response_content = b"<html><body><p>Error 404: File not found</p><p>Python HTTP server</p></body></html>"

             server_response =  response_headers.encode() # return headers for GET and HEAD
             if (request_method == 'GET'):
                 server_response +=  response_content  # return additional conten for GET only

             conn.send(server_response)
             conn.close()

         else:
             pass

def graceful_shutdown(sig, dummy):
    """ This function shuts down the server. It's triggered
    by SIGINT signal """
    s.shutdown() #shut down the server
    import sys
    sys.exit(1)

###########################################################
# shut down on ctrl+c
signal.signal(signal.SIGINT, graceful_shutdown)

print ("Starting web server")
s = Server(80)  # construct server object
s.activate_server() # aquire the socket