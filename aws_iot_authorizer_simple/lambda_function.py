import logging.handlers
import base64
import os

ALLOW_ACTION = 'Allow'
DENY_ACTION = 'Deny'
USERNAME = "TestUserName"
PASSWORD = "TestPassword"
REGION = "eu-central-1"
ACCOUNT_ID = "123456789012"


def init_logger(logger):
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s', '%Y-%m-%d %H:%M:%S')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.propagate = False


def generate_auth_response(effect, client_id):
    arn_prefix = "arn:aws:iot:{}:{}".format(REGION, ACCOUNT_ID)
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
        user_name = event["protocolData"]["mqtt"]["username"].split("?")[0]
        password = base64.b64decode(event["protocolData"]["mqtt"]["password"]).decode()
        client_id = event["protocolData"]["mqtt"]["clientId"]
        logger.info("Authenticating:{}:{}".format(user_name, client_id))
        if USERNAME == user_name and PASSWORD == password:
            logger.info("Access Granted")
            answer = generate_auth_response(ALLOW_ACTION, client_id)
        else:
            logger.info("Access Denied")
            answer = generate_auth_response(DENY_ACTION, client_id)
        logger.debug(answer)
        return answer
    except Exception as e:
        logger.error(f"Caught an exception:\n{e}")
    finally:
        logger.info("Finished")
