#!/usr/bin/python
# coding=utf-8

import cgi
import cgitb
import json
import os
import shelve
import sys
import textwrap
import urllib

import feedparser
import time
import thingspeak

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from conf.settings import *

__author__ = 'Tomasz Ceszke'

cgitb.enable()

form = cgi.FieldStorage()
battery = form.getvalue('bat')


def get_battery():
    if battery:
        return battery


def get_time():
    now = time.localtime()
    return time.strftime("%H:%M", now)


def get_temp(field):
    d = shelve.open(database)
    minutes = time.strftime("%M", time.localtime())
    if minutes == "59" or minutes == "29" or str(field) not in d:
        temp_json = json.loads(thingspeak.Channel(temperature_channel_id).get_field_last(field))
        temp = float(temp_json[field])
        if not isinstance(temp, float):
            sys.stderr.write("Error getting value for sensor " + str(field) + "\n")
            if field in d:
                temp = d[str(field)]
        else:
            d[str(field)] = temp
    else:
        temp = d[str(field)]
    d.close()
    if isinstance(temp, float):
        return int(round(temp))


def get_forecast():
    d = shelve.open(database)
    if time.strftime("%M", time.localtime()) == "59" or 'forecast' not in d:
        response = urllib.urlopen(openweathermap_url)
        data = json.loads(response.read())
        forecast = data['list'][1]['weather'][0]['description']
        d['forecast'] = forecast
    else:
        forecast = d['forecast']
    d.close()
    return forecast


def get_feeds(amount=2):
    feeds = ''
    wrapper = textwrap.TextWrapper(width=feed_wrapping, initial_indent="> ")
    rss_feeds = feedparser.parse(feed_url)
    i = 0
    for raw_feed in rss_feeds.entries:
        encoded_feed = raw_feed.title.encode('utf-8').strip()
        # if (len(encoded_feed)) > FEED_LENGTH:
        #     encoded_feed = encoded_feed[:FEED_LENGTH] + "..."
        formatted_feed = wrapper.fill(encoded_feed)
        feeds += formatted_feed
        i += 1
        if i == amount:
            break
    return feeds


def png_render():
    # forecast = get_forecast()
    # image over 0,0 0,0 '/tmp/09d.png' \

    cmd = "convert -size 600x800 xc:white -draw \" \
        font-size 160 text 100,300 '{1}' \
        line   30,335 570,335 \
        font-size 140 text 160,480 '{2}°C' \
        line   30,530 570,530 \
        font-size 90 text 170,630 '{3}°C' \
        \" -depth 8 -type GrayScale {0}".format(png_file, get_time(), get_temp(temperature_out_field), get_temp(temperature_bedroom_field))
    os.popen(cmd)


def main():
    png_render()


if __name__ == '__main__':
    main()

print "Content-type: image/png\n"
print file(png_file, "rb").read()
