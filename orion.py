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
orion_host = '10.7.40.62'
orion_port = '1026'

# definição do diretório do dispositivo
DEVICE_FILE_ROOT = './devices/'
# id do dispositivo que se deseja enviar medições
DEVICE_TYPE = "DoorControl"
# id da entidade que está ligada ao dispositivo
DEVICE_ID = "door01"
# dispositivo que vai ser utilizado na aplicação
Device = "DOOR.json"
# diretório completo do dispositivo
DOOR_FILE_PATH = DEVICE_FILE_ROOT + Device


def update_context(entity_id, entity_type, value):
    logging.info("Update entity with ID:{} and Type:{}".format(
        entity_id, entity_type))
    url = "http://{}:{}/{}/{}/attrs".format(
        orion_host, orion_port, VERSION, entity_id)

    data = {"status": {"type": "Boolean", "value": value}}
    headers = {'Content-Type': 'application/json'}

    r = requests.patch(url, data=json.dumps(data), headers=headers)
    status_code = r.status_code
    logging.info("Status Code: {}".format(str(status_code)))

    response = json.loads(r.text) if r.text != '' else {}

    logging.info("Response: ")
    logging.info(json.dumps(response, indent=4))


def delete_entity(entity_id, entity_type):
    logging.info("Delete entity with ID:{} and Type:{}".format(
        entity_id, entity_type))
    url = "http://{}:{}/{}/{}?type={}".format(
        orion_host, orion_port, VERSION, entity_id, entity_type)

    r = requests.delete(url)
    status_code = r.status_code
    logging.info("Status Code: {}".format(str(status_code)))

    response = json.loads(r.text) if r.text != '' else {}

    logging.info("Response: ")
    logging.info(json.dumps(response, indent=4))


def get_entities_by_id(entity_id):
    logging.info("Getting entities by ID '{}'".format(entity_id))

    url = "http://{}:{}/{}/{}".format(
        orion_host, orion_port, VERSION, entity_id)

    r = requests.get(url)
    status_code = r.status_code
    logging.info("Status Code: {}".format(str(status_code)))

    response = json.loads(r.text) if r.text != '' else {}

    logging.info("Response: ")
    logging.info(json.dumps(response, indent=4))


def get_entities_by_type(entity_type):
    logging.info("Getting entities by type '{}'".format(entity_type))

    url = "http://{}:{}/{}?type={}".format(
        orion_host, orion_port, VERSION, entity_type)

    r = requests.get(url)
    status_code = r.status_code
    logging.info("Status Code: {}".format(str(status_code)))

    response = json.loads(r.text) if r.text != '' else {}

    logging.info("Response: ")
    logging.info(json.dumps(response, indent=4))


def register_entity(device_schema, device_type, device_id, endpoint):
    """
    Register a new entity.
    """
    logging.info("Registering device")

    device_schema = json.dumps(device_schema)
    device_schema = device_schema.replace('[DEVICE_TYPE]', str(device_type)) \
        .replace('[DEVICE_ID]', str(device_id))

    logging.info(device_schema)

    url = "http://{}:{}/{}".format(orion_host, orion_port, VERSION)

    headers = {'Content-Type': 'application/json'}

    if '"endpoint"' in device_schema:
        endpoint_split = endpoint.split(':')
        device_ip = endpoint_split[0]
        device_port = endpoint_split[1]
        device_schema = device_schema.replace('[DEVICE_IP]', str(device_ip)) \
            .replace('[PORT]', str(device_port))

    payload = json.loads(device_schema)

    r = requests.post(url, data=device_schema, headers=headers)

    status_code = r.status_code
    logging.info("Status Code: {}".format(str(status_code)))

    response = json.loads(r.text) if r.text != '' else {}

    logging.info("Response: ")
    logging.info(json.dumps(response, indent=4))


with open(DOOR_FILE_PATH) as json_file:
    data = json.load(json_file)

# register_entity(data, DEVICE_TYPE, DEVICE_ID, '0.0.0.0:4000')
# get_entities_by_type(DEVICE_TYPE)
get_entities_by_id(DEVICE_ID)
update_context(DEVICE_ID, DEVICE_TYPE, "false")
get_entities_by_id(DEVICE_ID)
