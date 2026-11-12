from http.server import CGIHTTPRequestHandler
from http.server import SimpleHTTPRequestHandler
from http.server import test
import os
import sys

server_dir = sys.argv[1]
os.chdir(server_dir)


def start_server(port=8000, bind="", cgi=True):
    if cgi:
        test(HandlerClass=CGIHTTPRequestHandler, port=port, bind=bind)
    else:
        test(HandlerClass=SimpleHTTPRequestHandler, port=port, bind=bind)

start_server()
