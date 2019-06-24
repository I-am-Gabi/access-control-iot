import json

import orion
import cygnus

from utils import read_config_file

config = read_config_file('config.ini')
with open(config.get('device_schema_path')) as json_file:
    data = json.load(json_file)

orion.init(config.get('orion_host'), config.get('orion_port'))

orion.register_entity(data, config.get('device_type'), config.get('device_id'), '0.0.0.0:4000')
orion.get_entities_by_type(config.get('device_type'))
#orion.get_entities_by_id(config.get('device_id'))
#orion.update_context(config.get('device_id'),
#                     config.get('device_type'), "true")
#orion.get_entities_by_id(config.get('device_id'))


#cygnus.init(config.get('cygnus_host'), config.get('cygnus_port'))
#cygnus.subscribe_attributes_change(config.get('device_type'), config.get('device_id'), ["status"], config.get('')