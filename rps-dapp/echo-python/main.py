from os import environ
import logging
import requests
from util import str2hex, hex2str
from challenge import Challenge, Move
import json

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

def add_notice(data):
    logger.info(f"Adding notice {data}")
    notice = {"payload": str2hex(data)}
    response = requests.post(rollup_server + "/notice", json=notice)
    logger.info(f"Received notice status {response.status_code} body {response.content}")

def add_report(output=""):
    logger.info("Adding report" + output)
    report = {"payload": str2hex(output)}
    response = requests.post(rollup_server + "/report", json=report)
    logger.info(f"Received report status {response.status_code}")

def handle_advance(data):
    try:
        payload = json.loads(hex2str(data["payload"]))
    except:
        return "reject"
    
    method = payload.get("method")
    sender = data["metadata"]["msg_sender"]
    logger.info(f"Received advance request - {payload}")

    handler = advance_method_handlers.get(method)
    if not handler:
        add_report("invalid methof")
        return "reject"
    
    return handler(payload, sender)

def handle_inspect(data):
    try:
        payload = json.loads(hex2str(data["payload"]))
    except:
        return "reject"
    
    method = payload.get("method")
    sender = data["metadata"]["msg_sender"]
    logger.info(f"Received inspect request - {payload}")

    handler = inspect_method_handlers.get(method)
    if not handler:
        add_report("invalid methof")
        return "reject"
    
    return handler()

def create_challenge(payload, sender):
    add_report("create challenge")
    return "accept"

def accept_challenge(payload, sender):
    add_report("accept challenge")
    return "accept"

def reveal(payload, sender):
    add_report("reveal challenger")
    return "accept"

def get_challenges():
    add_report("get challenges")
    return "accept"


handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

advance_method_handlers = {
    "create_challenge": create_challenge,
    "reveal": reveal,
    "accept_challenge": accept_challenge,
}

inspect_method_handlers = {
    "get_challenges": get_challenges,
}

finish = {"status": "accept"}

{"method": "create_challenge"}

while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]
        
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
