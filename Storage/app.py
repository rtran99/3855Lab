import connexion
from connexion import NoContent
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
import datetime
from search_Inventory import SearchInventory
from place_Shipment import PlaceShipment
import logging
from logging import config
import yaml
import requests
import json
from pykafka import KafkaClient
from  pykafka.common import OffsetType
from threading import Thread


with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
logger = logging.getLogger("basicLogger")

DB_ENGINE = create_engine(f'mysql+pymysql://{app_config["datastore"]["user"]}:{app_config["datastore"]["password"]}@{app_config["datastore"]["hostname"]}:{app_config["datastore"]["port"]}/{app_config["datastore"]["db"]}')
print(DB_ENGINE)
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


logger.info(("Connecting to DB. Hostname {}, Port: {}").format(app_config['datastore']["hostname"],app_config['datastore']["port"]))




def get_shipping(timestamp):
    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp,"%Y-%m-%dT%H:%M:%SZ")
    readings = session.query(SearchInventory).filter(SearchInventory.date_created > timestamp_datetime)
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()
    logger.info("Query for order readings after %s returns %d results" % (timestamp, len(results_list)))
    return results_list, 200

def get_InventoryItem(timestamp):
    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp,"%Y-%m-%dT%H:%M:%SZ")
    readings = session.query(PlaceShipment).filter(PlaceShipment.date_created > timestamp_datetime)
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()
    logger.info("Query for inventory items readings after %s returns %d results" % (timestamp, len(results_list)))
    return results_list, 200


def place_Shipment(body):
    logger.info(body)
    print("test")

    session = DB_SESSION()

    ad = PlaceShipment(
        body['device_id'],
        body['shippingPriority'],
        body['shippingCompany'],
        body['address'],
        body['name'],
        body['deliveryDate'],
        body['ordersreceived']
    )
    session.add(ad)

    session.commit()
    session.close()

    logger.info("Stored event %s request with a unique id of %s" % ("Orders Received", body["device_id"]))

    return NoContent, 201


def search_Inventory(body):
    print("test")
    logger.info(body)
    session = DB_SESSION()
    at = SearchInventory(
        body['device_id'],
        body['trackingId'],
        body['Itemname'],
        body['manufacturer'],
        body['quantity'],
        body['weight'],
        body['wishlisted']
    )


    session.add(at)

    session.commit()
    session.close()

    logger.info("Stored event %s request with a unique id of %s" % ("Customer items", body["device_id"]))

    return NoContent, 201

def process_messages():
    """ Process event messages """
    hostname = "%s:%d" % (app_config["events"]["hostname"],
                          app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    # Create a consume on a consumer group, that only reads new messages
    # (uncommitted messages) when the service re-starts (i.e., it doesn't
    # read all the old messages from the history in the message queue).
    consumer = topic.get_simple_consumer(consumer_group=b'event_group',
                                         reset_offset_on_start=False,
                                         auto_offset_reset=OffsetType.LATEST)
    # This is blocking - it will wait for a new message
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: %s" % msg)
        payload = msg["payload"]
        if msg["type"] == "shipping":  # Change this to your event type
            # Store the event1 (i.e., the payload) to the DB
                session = DB_SESSION()
                ad = PlaceShipment(
                    payload['device_id'],
                    payload['shippingPriority'],
                    payload['shippingCompany'],
                    payload['address'],
                    payload['name'],
                    payload['deliveryDate'],
                    payload['ordersreceived']
    	        )
    	        session.add(ad)
                session.commit()
    	        session.close()
        elif msg["type"] == "InventoryItem":  # Change this to your event type
            # Store the event2 (i.e., the payload) to the DB
    	        session = DB_SESSION()
    	        at = SearchInventory(
                    payload['device_id'],
                    payload['trackingId'],
                    payload['Itemname'],
                    payload['manufacturer'],
                    payload['quantity'],
                    payload['weight'],
                    payload['wishlisted']
    	         )
    	        session.add(at)
    	        session.commit()
    	        session.close()
        # Commit the new message as being read
        consumer.commit_offsets()

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)
