import logging.handlers
import base64
import boto3
import os

ALLOW_ACTION = 'Allow'
DENY_ACTION = 'Deny'


def init_logger(logger):
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s', '%Y-%m-%d %H:%M:%S')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.propagate = False


def get_environment_variables():
    environment_variables = dict(
        region=os.environ["region"],
        account_id=os.environ["account_id"]
        )
    return environment_variables


def generate_auth_response(effect, client_id, ev):
    arn_prefix = "arn:aws:iot:{}:{}".format(ev["region"], ev["account_id"])
    client_arn = "{}:client/{}".format(arn_prefix, client_id)
    publish_statement = dict(
        Action=["iot:Publish"],
        Effect=effect,
        Resource=["{}:topic/wv/*".format(arn_prefix)]
    )
    connect_statement = dict(
        Action=["iot:Connect"],
        Effect=effect,
        Resource=[client_arn]
    )
    policy_document = dict(
        Version='2012-10-17',
        Statement=[connect_statement, publish_statement]
    )
    auth_response = dict(
        isAuthenticated=True,
        principalId=client_id,
        policyDocuments=[policy_document],
        disconnectAfterInSeconds=3600,
        refreshAfterInSeconds=300
    )
    return auth_response


def lambda_handler(event, context):
    logger = logging.getLogger(__name__)
    init_logger(logger)
    logger.info("Starting")
    logger.debug(event)
    try:
        ev = get_environment_variables()
        user_name = event["protocolData"]["mqtt"]["username"].split("?")[0]
        password = base64.b64decode(event["protocolData"]["mqtt"]["password"]).decode()
        client_id = event["protocolData"]["mqtt"]["clientId"]
        logger.info("Authenticating:{}:{}".format(user_name, client_id))
        client = boto3.client('iot', region_name=ev["region"])
        things_info = client.list_things(maxResults=1, attributeName='UUID', attributeValue=client_id)
        thing = things_info["things"][0]
        if thing:
            attributes = thing["attributes"]
            if attributes["SECRET_KEY"] == password and thing["thingName"] == user_name:
                logger.info("Access Granted")
                answer = generate_auth_response(ALLOW_ACTION, client_id, ev)
            else:
                logger.info("Access Denied")
                answer = generate_auth_response(DENY_ACTION, client_id, ev)
            logger.debug(answer)
            return answer
        else:
            logger.info(f"Could not find a thing with attribute UUID=='{client_id}'")
    except Exception as e:
        logger.error(f"Caught an exception:\n{e}")
    finally:
        logger.info("Finished")
