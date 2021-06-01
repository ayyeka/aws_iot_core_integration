from proto import SamplesMessage_pb2
import base64
from google.protobuf.json_format import MessageToDict
import json
import logging.handlers
import boto3


def init_logger(logger):
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s', '%Y-%m-%d %H:%M:%S')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.propagate = False


def extract_samples(logger, msg):
    data = {"reportId": None, "totalSamples": 0, "samples": []}
    total_samples = 0
    if "reportId" in msg.keys():
        data.update({'reportId': msg["reportId"]})
    for batch in msg["samplesBatch"]:
        if "sparse" in batch.keys():
            for sample in batch["sparse"]["samples"]:
                sample_data = {"timestamp": sample["timestamp"], "value": list(sample["data"].values())[0]}
                sample_data.update(batch["typeAndNumber"])
                data["samples"].append(sample_data)
                total_samples += 1
        if "periodic" in batch.keys():
            ts = int(batch["periodic"]["firstTimestamp"])
            interval = int(batch["periodic"]["interval"])
            for sample in batch["periodic"]["data"]:
                sample_data = {"timestamp": str(ts), "value": list(sample.values())[0]}
                sample_data.update(batch["typeAndNumber"])
                data["samples"].append(sample_data)
                ts += interval
                total_samples += 1

    data["totalSamples"] = total_samples
    return data


def lambda_handler(event, context):
    logger = logging.getLogger(__name__)
    init_logger(logger)
    logger.info("Starting")
    logger.info(event)

    topic = event["topic"]
    base64_msg = event["data"]
    client_id = event["client_id"]

    if 'samp' not in topic:
        logger.info(f"Message does contain data samples (topic={topic}")
        return

    logger.debug("{}:Decoding msg:{}".format(client_id, base64_msg))
    binary_msg = base64.b64decode(base64_msg)
    proto_msg = SamplesMessage_pb2.SamplesBatchMessage()
    proto_msg.ParseFromString(binary_msg)
    msg = MessageToDict(proto_msg, including_default_value_fields=True)

    data_samples = extract_samples(logger, msg)

    thing_metadata = dict()
    thing_metadata["mqtt_clientid"] = client_id
    try:
        client = boto3.client('iot', region_name='eu-central-1')
        things_info = client.list_things(maxResults=1, attributeName='UUID', attributeValue=client_id)

        if (things_info["ResponseMetadata"]["HTTPStatusCode"] == 200) and (len(things_info["things"]) > 0):
            thing = things_info["things"][0]
            thing_metadata["thingName"] = thing["thingName"]
            thing_metadata["thingTypeName"] = thing["thingTypeName"]
            thing_metadata["thingArn"] = thing["thingArn"]
        else:
            thing_metadata["ERROR"] = f"Could not find a thing with attribute UUID=='{client_id}'"
    except Exception as e:
        logger.error(f"Caught an exception while accessing AWS IoT using boto3:\n{e}")

    response = dict()
    response["thingMetadata"] = thing_metadata
    response["data_samples"] = data_samples

    json_response = json.dumps(response)

    logger.info("{}:Lambda Output:{}".format(client_id, json_response))

    #############################################################################
    # Here you can send json_response for further processing with any AWS service
    #############################################################################
