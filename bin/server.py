#!/usr/bin/env python3
import json
import shelve
from http.server import BaseHTTPRequestHandler, HTTPServer

import time
import os
import sys
import thingspeak as thingspeak

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from conf.settings import *


def png_render():
    cmd = u"/usr/bin/convert -size 600x800 xc:white -draw \" \
        font-size 160 text 100,300 '{1}' \
        line 30,335 570,335 \
        font-size 140 text 160,480 '{2}°C' \
        line 30,530 570,530 \
        font-size 90 text 200,630 '{3}°C' \
        \" -depth 8 -type GrayScale {0}".format(png_file, get_time(), get_temp(out_channel_id), get_temp(in_channel_id))
    os.system(cmd)


def get_time():
    now = time.localtime()
    return time.strftime("%H:%M", now)


def get_temp(channel_id):
    d = shelve.open(database)
    minutes = time.strftime("%M", time.localtime())
    if minutes == "59" or minutes == "29" or str(channel_id) not in d:
        temp_json = json.loads(thingspeak.Channel(channel_id).get_field_last('field1'))
        temp = float(temp_json['field1'])
        if not isinstance(temp, float):
            sys.stderr.write("Error getting value for sensor " + str(channel_id) + "\n")
            if channel_id in d:
                temp = d[str(channel_id)]
        else:
            d[str(channel_id)] = temp
    else:
        temp = d[str(channel_id)]
    d.close()
    if isinstance(temp, float):
        return int(round(temp))


class PngRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        png_render()
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.end_headers()
        self.wfile.write(open(png_file, "rb").read())
        return

    def log_message(self, format, *args):
        return


def run():
    print('Server is starting...')
    server_address = ('', port)
    httpd = HTTPServer(server_address, PngRequestHandler)
    print('Server is listening on port ' + str(port))
    httpd.serve_forever()


if __name__ == "__main__":
    run()
