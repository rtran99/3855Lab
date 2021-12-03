
import logging, logging.config
import json
import connexion
from connexion import NoContent
import logging
import logging.config
import yaml
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import requests
import os
from flask_cors import CORS, cross_origin

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())
    data_file = app_config["datastore"]["filename"]

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    logger = logging.getLogger('basicLogger')

def get_stats():
    logger.info('Get stats request started')
    if os.path.isfile('data.json'):
        with open(app_config['datastore']['filename']) as f:
            logger.info('Request has ended')
            return json.load(f), 200
    else:
        logger.error('file does not exist')
        msg = 'file does not exist'
        return msg, 404

def populate_stats():
    """ Periodically update stats """
    logger.info(f"Start Periodic Processing")
    current_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(data_file, "r") as f:
        last_update = json.load(f)["last_updated"]

    response_search_item = requests.get(app_config["searchitem"]["url"], params={'timestamp': last_update})
    response_shipping = requests.get(app_config["shiporders"]["url"], params={'timestamp': last_update})
    if len(response_search_item.json()) != 0 and len(response_shipping.json()) != 0:
        temp_list = []
        for tmd in response_search_item.json():
            temp_list.append(tmd['quantity'])

        max_inv_reading = max(temp_list)
        num_inv_readings = len(response_search_item.json())

        ph_value_list = []
        for ph_value in response_shipping.json():
            ph_value_list.append(ph_value['ordersreceived'])
        max_order_reading = max(ph_value_list)
        num_order_readings = len(response_shipping.json())

        data = json.dumps({
            "num_inv_readings": num_inv_readings,
            "max_inv_reading": max_inv_reading,
            "num_order_readings": num_order_readings,
            "max_order_reading": max_order_reading,
            "last_updated": current_time
        })

        with open('data.json', 'w') as f:
            f.write(data)

        logger.debug(data)

def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats,
                  'interval',
                  seconds=app_config['scheduler']['period_sec'])
    sched.start()

app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app) 
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yaml",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":# run our standalone gevent server#
    init_scheduler()
    app.run(port=8100, use_reloader=False)