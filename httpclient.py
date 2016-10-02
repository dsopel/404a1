#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Daniel Sopel, Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
from urlparse import urlparse
import urllib

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):

    def connect(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        return s

    def get_code(self, data):
        return int(data.split(" ")[1])

    def get_body(self, data):
	return data.split("\r\n\r\n")[1]  

    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)    
            
    def GET(self, url, args=None):
        request = "GET " + urlparse(url).path + " HTTP/1.1\r\nHost: "+ urlparse(url).netloc.split(':')[0]+ "\r\n\r\n" 
        try:
		port = urlparse(url).netloc.split(':')[1]
	except:
		port = 80
	serversocket=self.connect(urlparse(url).netloc.split(':')[0], int(port))
        serversocket.send(request)
        serverresponse=self.recvall(serversocket)
	serversocket.close()
        code=self.get_code(serverresponse) 
        body=self.get_body(serverresponse)
        return HTTPRequest(code, body)

    def POST(self, url, args=None):
	if(args):
		querystring = urllib.urlencode(args)
	else:	
		querystring = ""
	request = "POST " + urlparse(url).path + " HTTP/1.1 \r\nHost: "+ urlparse(url).netloc.split(':')[0]+ "Content-Type:application/x-www-form-urlencoded\r\n"+"Content-Length: "+str(len(querystring))+"\r\n\r\n"
 	try:
		port = urlparse(url).netloc.split(':')[1]
	except:
		port = 80
	serversocket=self.connect(urlparse(url).netloc.split(':')[0], int(port))
        serversocket.send(request)
	serversocket.send(querystring)
        serverresponse=self.recvall(serversocket)
	serversocket.close()
        code=self.get_code(serverresponse) 
 	body=self.get_body(serverresponse)
	return HTTPRequest(code, body)


    def command(self, url, command="GET", args=None):
        if (command == "POST"):
        	return self.POST( url, args )
        else:
		return self.GET( url, args )


if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] ).body
    else:
	print client.command(sys.argv[1], command) 