#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import uniform
import json
import sys
import time
import random
import requests
import logging
logging.basicConfig(level=logging.INFO)

VERSION = "v2/entities"
cygnus_host = 'localhost'
cygnus_port = '1026'


def subscribe_attributes_change(device_type, device_id, attributes, notification_url):
    logging.info("Subscribing for change on attributes '{}' on device with id '{}'".format(
        attributes, device_id))

    url = "http://{}:{}/v1/subscribeContext".format(
        cygnus_host, cygnus_port)

    additional_headers = {'Accept': 'application/json',
                          'Content-Type': 'application/json'}

    payload = { "entities": 
        [{
            "type": device_type,
            "isPattern": "false",
            "id": device_id,
        }],
        "attributes": attributes,
        "notifyConditions": [{
            "type": "ONCHANGE",
            "condValues": attributes
        }],
        "reference": notification_url,
        "duration": "P1Y",
        "throttling": "PT1S"
    } 

    r = requests.post(url, data=payload, headers=headers)

    status_code = r.status_code
    logging.info("Status Code: {}".format(str(status_code)))

    response = json.loads(r.text) if r.text != '' else {}

    logging.info("Response: ")
    logging.info(json.dumps(response, indent=4))


def init(host, port):
    global cygnus_host, cygnus_port
    cygnus_host = host
    cygnus_port = port
