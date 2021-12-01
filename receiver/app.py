import connexion
from connexion import NoContent
import requests
import yaml
import logging
from logging import config
from pykafka import KafkaClient
import json
import datetime

HEADERS = {"Content-Type": "application/json"}


with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())
with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    logger = logging.getLogger('basicLogger')



def place_Shipment(body):
    # logger.info("Received event %s request with a unique id of %s"
    #             % ("Orders received", body["device_id"]))
    # response = requests.post(app_config["eventstore2"]["url"],
    #                          json=body, headers=HEADERS)

    # logger.info("Returned event %s response %s with status %s"
    #             % ("Orders received", body["device_id"], response.status_code))
    # return NoContent, response.status_code
    hostname = "%s:%d" % (app_config["events"]["hostname"],
                          app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode("events")]
    producer = topic.get_sync_producer()
    msg = {"type": "pv", "datetime": datetime.datetime.now().strftime(
    "%Y-%m-%dT%H:%M:%S"), "payload": body }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode("utf-8"))
    return NoContent, 201


def search_Inventory(body):
    # print("test")
    # print(app_config["eventstore1"]["url"])
    # print(HEADERS)
    # print("end test")
    # logger.info(body)
    # logger.info("Received event %s request with a unique id of %s"
    #             % ("Item Names", body["device_id"]))
    # response = requests.post(app_config["eventstore1"]["url"], json=body, headers=HEADERS)


    # logger.info("Returned event %s response %s with status %s"
    #             % ("Item Names", body["device_id"], response.status_code))
    # return NoContent, response.status_code
    hostname = "%s:%d" % (app_config["events"]["hostname"],
                          app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)

    topic = client.topics[str.encode("events")]
    producer = topic.get_sync_producer()

    msg = {"type": "wt", "datetime": datetime.datetime.now().strftime(
        "%Y-%m-%dT%H:%M:%S"), "payload": body}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode("utf-8"))
    return NoContent, 201







app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080, debug=True)
