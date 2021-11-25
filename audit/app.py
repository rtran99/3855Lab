import connexion
from connexion import NoContent
import datetime
from search_Inventory import SearchInventory
from place_Shipment import PlaceShipment
import logging
from logging import config
import yaml
import requests
import query
import json
from pykafka import KafkaClient
from  pykafka.common import OffsetType
from threading import Thread
logger = logging.getLogger('basicLogger')

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())
    data_file = app_config["datastore"]["filename"]

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    logger = logging.getLogger('basicLogger')

def get_search_Inventory(index):
    hostname = "%s:%d" % (app_config["events"]["hostname"],app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    # Here we reset the offset on start so that we retrieve
    # messages at the beginning of the message queue. 
    # To prevent the for loop from blocking, we set the timeout to
    # 100ms. There is a risk that this loop never stops if the
    # index is large and messages are constantly being received!
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=1000)
    logger.info("Retrieving BP at index %d" % index)
    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
    # Find the event at the index you want and 
    # return code 200
    # i.e., return event, 200
    except:
        logger.error("No more messages found")
    logger.error("Could not find BP at index %d" % index)
    return { "message": "Not Found"}, 404


def get_place_Shipment(index):
    hostname = "%s:%d" % (app_config["events"]["hostname"],app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    # Here we reset the offset on start so that we retrieve
    # messages at the beginning of the message queue. 
    # To prevent the for loop from blocking, we set the timeout to
    # 100ms. There is a risk that this loop never stops if the
    # index is large and messages are constantly being received!
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, 
    consumer_timeout_ms=1000)
    logger.info("Retrieving BP at index %d" % index)
    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
    # Find the event at the index you want and 
    # return code 200
    # i.e., return event, 200
    except:
        logger.error("No more messages found")
    logger.error("Could not find BP at index %d" % index)
    return { "message": "Not Found"}, 404