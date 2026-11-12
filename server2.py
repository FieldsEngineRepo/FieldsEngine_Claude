from SimpleHTTPServer import SimpleHTTPRequestHandler
from CGIHTTPServer import CGIHTTPRequestHandler
import SocketServer
import os
import sys

server_dir = sys.argv[1]
os.chdir(server_dir)

def start_server(port=8000, bind="", cgi=True):
    if cgi:
        Handler = CGIHTTPRequestHandler
    else:
        Handler = SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer((bind, port), Handler)
    print "serving at port", port
    httpd.serve_forever()

start_server()
