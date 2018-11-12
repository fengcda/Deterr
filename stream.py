#!/usr/bin/env python
from flask import Flask, render_template, Response

import sys
import psutil
import time
import winsound
from camera import get_frame
from sound import Sound
import ctypes

app = Flask(__name__)

@app.route('/')
def index():
    def sec2hours(secs):
        mm, ss = divmod(secs, 60)
        hh, mm = divmod(mm, 60)
        return "%d:%02d:%02d" % (hh, mm, ss)

    battery = psutil.sensors_battery()
    percent = battery.percent
    charging = battery.power_plugged
    sec = sec2hours(psutil.sensors_battery().secsleft)
    return render_template('index.html', percent = percent, charging = charging, sec = sec)

def status():


    return sec2hours(battery.secsleft)

@app.route('/alarm')
def alarm():
    duration = 3500  # millisecond
    freq = 8000# Hz
    if Sound.is_muted():
        Sound.mute()
    Sound.volume_max()
    winsound.Beep(freq, duration)
    return "alarm sounded"

@app.route('/calc')
def calc():
     return Response(get_frame(0),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/calc2')
def calc2():
     return Response(get_frame(1),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/hello')
def hello():
    return render_template('hello.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
