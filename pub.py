from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json
import base64

from datetime import datetime
import random

# proto imports
import \
    SamplesMessage_pb2, ChannelType_pb2, PeriodicSamples_pb2, Sample_pb2

import json, uuid, sys

########################### CONFIG #############################

# Find this under your aws iot console, under settings
_ENDPOINT = 'a33uu6vttl7rcg-ats.iot.us-west-1.amazonaws.com'

# Requests need to have unique IDs, any connection with a duplicate id will be droped
_CLIENT_ID = uuid.uuid1()

# Amazon root certificate
_ROOT_CERT = '../certificates/root.pem'

# Device Username, Password
_USERNAME = 'TestUserName'
_PASSWORD = 'TestPassword'

# aws iot defined custom authorizer name
_CUSTOM_AUTHORIZER = 'simple_authorizer'

# Device topic 
DEVICE_AKID = 'AKID-0'
TOPIC = f'wv/{DEVICE_AKID}/1/samp/p1'

########################## SCRIPT #######################
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

tls_options = io.TlsContextOptions()
tls_options.alpn_list = ['mqtt']


tls_options.override_default_trust_store_from_path(
    ca_dirpath=None,
    ca_filepath=_ROOT_CERT
)
tls_ctx = io.ClientTlsContext(options=tls_options)
client = mqtt.Client(client_bootstrap, tls_ctx)


username = f'{_USERNAME}?x-amz-customauthorizer-name={_CUSTOM_AUTHORIZER}'

mqtt_connection = mqtt.Connection(
    client=client,
    host_name=_ENDPOINT,
    port=443,
    client_id=f'{_CLIENT_ID.int}',
    clean_session=True,
    # keep_alive_secs=10,
    username=username,
    password=_PASSWORD)



connect_future = mqtt_connection.connect()

# Future.result() waits until a result is available
print(mqtt_connection)
print("Connected!  :  ",connect_future.result())

print('Begin Publish')



MSG_RANGE = 1
SAMPLE_BATCH_RANGE = 3

for i in range(MSG_RANGE):
    # Each message is a samples_batch_message containing multiple periodic sample_data
    message = SamplesMessage_pb2.SamplesBatchMessage()
    message.report_id = i+1
    for j in range(SAMPLE_BATCH_RANGE):
        # message SamplesMessage
        # {
        #     oneof source {
        #         ChannelTypeAndNumber type_and_number = 2;
        #     }

        #     oneof samples
        #     {
        #         PeriodicSamples periodic = 3;
        #         SparseSamples sparse = 4;
        #     }
        # }

        # message SamplesBatchMessage
        # {
        #     int64 report_id = 1;
        #     repeated SamplesMessage samples_batch = 2;
        # }
        
        # message PeriodicSamples {
        # uint64 first_timestamp = 1;
        # uint64 interval = 2;
        # repeated SampleData data = 3;
        # }
        # Add a samples_message to the batch
        samples_message = message.samples_batch.add()
        
        type_and_number = SamplesMessage_pb2.ChannelTypeAndNumber()
        type_and_number.channel_type = ChannelType_pb2.TEMP_CHANNEL_TYPE

        samples_message.type_and_number.CopyFrom(type_and_number)

        periodic = PeriodicSamples_pb2.PeriodicSamples()

        periodic.first_timestamp = int(datetime.utcnow().timestamp() * 1000)# in ms ?
        periodic.interval = 500 # in ms ?
        
        sample_data = periodic.data.add()
        sample_data.uint64_value = random.randint(0, 10000)

        samples_message.periodic.CopyFrom(periodic)

    # protobuf byte encoding
    encoded_msg = message.SerializeToString()
    # bytes to base64 encoding
    # base64_encoded_msg = base64.b64encode(encoded_msg).decode("utf-8")

    mqtt_connection.publish(topic=TOPIC, payload=encoded_msg, qos=mqtt.QoS.AT_LEAST_ONCE)
    print(f"Published: {samples_message} to the topic: {TOPIC}")
    # print(f"Base64 msg : {base64_encoded_msg}")
    t.sleep(0.1)
    print()

print("\n##################")
print('Publish End')
print("\n##################")

disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()
