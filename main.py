#!/usr/bin/env python
import subprocess
import threading
import argparse
import shlex
import time
import os

parser = argparse.ArgumentParser()
parser.add_argument('--port', help="The port to be used by the local server")
args = parser.parse_args()

if args.port:
    port = int(args.port)
else:
    port = 8000

os.chdir(os.path.join(os.getcwd(), 'www'))

try:
    import http.server as server
    from http.server import CGIHTTPRequestHandler
except:
    import BaseHTTPServer as server
    from CGIHTTPServer import CGIHTTPRequestHandler

cgi_dir = os.path.join(os.path.dirname(os.getcwd()), 'cgi-bin')

class RequestHandler(CGIHTTPRequestHandler):
    def translate_path(self, path):
        elts = path.split('/')
        if len(elts)>1 and elts[0]=='' and elts[1]=='cgi-bin':
            return os.path.join(cgi_dir,*elts[2:])
        return CGIHTTPRequestHandler.translate_path(self, path)

server_address, handler = ('127.0.0.1', port), RequestHandler
httpd = server.HTTPServer(server_address, handler)
threading.Thread(target=httpd.serve_forever).start()

def run_node_bridge(port=port, secret="xxx"):
    subprocess.Popen(shlex.split("node server.js %s %s" % (secret, port)), shell=False, stdout=subprocess.PIPE)

def run_ffmpeg_stream_service(port=port, secret="xxx"):
    subprocess.Popen(shlex.split('ffmpeg.exe -hwaccel dxva2 -f dshow -thread_queue_size 512 -rtbufsize 200M -i video="screen-capture-recorder" -f dshow -thread_queue_size 512 -i audio="virtual-audio-capturer" -f mpegts -codec:v mpeg1video -s 1920x1080 -b:v 1000k -bf 0 -codec:a mp2 -b:a 128k -muxdelay 0.01 -pix_fmt yuv420p -tune zerolatency -preset ultrafast -r 60 -threads 32 -maxrate 2048k -acodec copy -bufsize 256k -vf "format=yuv420p" -strict -2 -g 60 -c:a mp2 -b:a 128k -ar 44100 -crf 100 http://127.0.0.1:%s/%s' % (port, secret)), shell=True, stdout=subprocess.PIPE)

print("Hijack the server :) have fun !!!")


