#!/usr/bin/env python

import sys
sys.path.append("/home/pi/irweb/Flask-0.10/")
sys.path.append("/home/pi/irweb/Jinja2-2.7.2/")
sys.path.append("/home/pi/irweb/werkzeug-master/")
sys.path.append("/home/pi/irweb/itsdangerous-master/")

from lirc.lirc import Lirc
from flask import Flask
from flask import render_template
from flask import request, redirect, url_for

BASE_URL = ''

app = Flask(__name__)

# Initialise the Lirc config parser
lircParse = Lirc('/home/pi/lircd.conf')


@app.route("/")
@app.route("/<device>")
def index(device=None):
    # Get the devices from the config file
    devices = []
    for dev in lircParse.devices():
        d = {
            'id': dev,
            'name': dev,
        }
        devices.append(d)
    
    return render_template('remote.html', devices=devices)


@app.route("/device/<device_id>")
def device(device_id=None):
    d = {'id':device_id}        
    return render_template('control.html', d=d)


@app.route("/device/<device_id>/clicked/<op>")
def clicked(device_id=None, op=None):
    # Send message to Lirc to control the IR
    lircParse.send_once(device_id, op)
    
    return ""



if __name__ == "__main__":
    app.debug = True
    app.run('0.0.0.0')


