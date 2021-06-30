# Wavelet & AWS IoT Core Integration

<p align="center">
  <a href="https://www.ayyeka.com/">
  <img src="images/logo.png" />
  </a>
</p>

## Guide Overview

This guide will walk you through integrating a Wavelet device to AWS IoT core. At the end of this guide, your Wavelet will transmit its sensor data to AWS IoT Core and receive remote configuration commands from Ayyeka's FAI platform, as shown in the following figure:
![picture_2](images/picture_2.PNG)

The guide is structured as follows:
* AWS IoT Core Intro
* AWS IoT Core Configuration
* 

## AWS IoT Core Intro

**AWS IoT Core** provides building blocks for cloud-based IoT solutions. The key services of **AWS IoT Core** are:
* Device ("thing") registry 
* Device provisioning, authentication and authorization 
* Data ingestion over HTTPS or MQTTS
* Rule-based data routing

Other services  of **AWS IoT Core** are:
* Integration with popular AWS data processing tools (Lambda, S3, SNS, SQS etc.)
* Device shadows
* Jobs

### AWS IoT Core – Things Registry

IoT devices are called “things” in AWS IoT. Each thing has a "type", which defines certain properties. Possible type examples are:
* Datalogger4G has required fields: `display_name`, `serial_number` and `UUID`
* Datalogger3G has only one required field: `serial_number`
Types and things are created and managed by admin users. When creating a thing, it is registered in the `Things Registry`.
The `Things Registry` can be accessed by other AWS Services (e.g. Lambda functions) 

> **Note**: it is not mandatory to register your thing in the Things Registry. For example, data can be ingested from unregistered things as well.


### AWS IoT Core – Device Authentication
AWS IoT Core supports multiple authentication options: <br>

**Protocols, authentication, and port mappings**  

| Protocol | Operations supported | Authentication | Port | ALPN protocol name | 
| --- | --- | --- | --- | --- | 
|  MQTT over WebSocket  | Publish, Subscribe | Signature Version 4 | 443 |  N/A  | 
|  MQTT over WebSocket  | Publish, Subscribe | Custom authentication | 443 |  N/A  | 
|  MQTT  | Publish, Subscribe |  X\.509 client certificate  |  443†  |  'x-amzn-mqtt-ca'  | 
| MQTT | Publish, Subscribe | X\.509 client certificate | 8883 | N/A | 
| **MQTT**  | **Publish, Subscribe** |  **Custom authentication**  |  **443**†  |  **'mqtt'**  | 
|  HTTPS  | Publish only |  Signature Version 4  |  443  |  N/A  | 
|  HTTPS  | Publish only |  X\.509 client certificate  |  443†  |  'x-amzn-http-ca'  | 
| HTTPS | Publish only | X\.509 client certificate | 8443 | N/A | 
| HTTPS | Publish only | Custom authentication | 443 | N/A | 

Wavelet supports the “Custom authentication” option over MQTT. See `Custom authentication` option above. <br>
<br>
**Custom Authentication** requires an **Authorizer Lambda Function**:
* The **Authorizer Lambda** receives the device’s MQTT credentials and verifies them
* Verification can be done against AWS IoT things registry OR any other data source

### AWS IoT Core – Data Routing

Devices can publish their data over MQTT to AWS IoT Core
> **Note**: the device must be granted **permission to publish** to a certain topic. See Authorizer Lambda below.

Each received MQTT message is tested against a user-defined set of rules. A `rule` is defined by three elements:
* `Filter`: defines which MQTT topics and messages will be processed by this rule
* `Action`: defines the action that is triggered by this rule
* `Data extraction`: defines which data should be passed on if the rule is matched. <br>

With `rules` and `actions`, common IoT tasks can be handled:
* Decoding raw data from the devices, e.g. `convert Protobuf to JSON`
* Republishing data to other systems
* Storing the data in a database

### Wavelet & MQTT – The Fine Print

**MQTT User & Password:**
* Must be configured to a valid username and password, per the AWS IoT Core setup
* Note: empty `username` or empty `password` will force Wavelet to use its hardcoded defaults, which do not match the credentials defined by the Authorizer Lambda by default.

**MQTT ClientID:**
* Wavelet is sending its AKID as the MQTT Client ID. 
* The AKID can be retrieved on FAI Pro user interface or through the REST API

**MQTT Topics:**

| Protocol | Operations supported | Authentication | 
| --- | --- | --- |
| /wv/`<AKID>`/1/`samp`/p1 | Sensor data and device telemetry | Protobuf, see **SampleMessage.proto** for defenition |
| wv/`<AKID>`/1/`reportend`/p1 | Last will and session termination reason | Protobuf, see **ReportEnd.proto** for defenition |


## AWS IoT Core Configuration

![picture_5](images/picture_5.PNG)

### Configuration Process Overview

**Step 1**: Configure simple authentication process
* Create a Custom Authorizer Lambda function
* Create an Authorizer on AWS IoT Core
* Test authentication process

**Step 2**: (Optional) Configure custom device authentication process with `Things registry`
* Create a Custom Authorizer Lambda function
* Create an Authorizer on AWS IoT Core
* Register a device in the Things Registry
* Give the auth Lambda access to `Things registry` 
* Test Custom Authorizer

**Step 3**: Configure a data processing rule
* Create a data processing Lambda function
* Create a `rule` and an `action`
* Test Data Processing rule

# Intro and explaination

##### The main difference to note between simple and custom authentication process :

* aws_iot_authorizer_simple just checks the username and password sent by the device over MQTT against a constant USERNAME and PASSWORD, so basically there is only one master (username, password) pair and all devices should provide it and have it hard coded in their running code/script.

* aws_iot_authorizer_things_registry on the other hand gets a username, password pair and checks them on your aws iot thing registry to make sure you’ve registered this device as a “thing”, and compares username to UUID and password to SECRET_KEY.
Note that UUID and SECRET_KEY are “thing” attributes that you define when creating the thing.
So here each device has it’s own credentials that will be checked against the thing registry.
# **Step 1**
### Creating an Authorizer Lambda


1. Download the project from GitHub: [aws_iot_core_integration](http://github.com/ayyeka/aws_iot_core_integration)


2. Locate the file  `lambda_function.py` under the `aws_iot_authorizer_simple`

3. This Lambda will authorize devices with MQTT username and password that match certain constants in the Python code `aws_iot_authorizer_simple`
You can edit these constants in `lambda_function.py` code to match your setup:
    ```
    USERNAME = "TestUserName"
    PASSWORD = "TestPassword"
    ```

![picture_6](images/picture_6.PNG)

4. Upload the edited file to AWS Lambda and create a Lambda function called `simple-custom-iot-auth` in the same region of your AWS IoT Core


> **Note**: `USERNAME` and `PASSWORD` fields are hardcoded and are later used for the device validation step.

### Creating a Custom Authorizer

1. On AWS IoT Core, navigate to the ‘Secure’ menu and then choose ‘Authorizers’
2. Click the "Create" button and in the next screen configure the following:
* **Name**: `mySimpleAuth`
* **Authorizer Function**: pick the name of the Lambda you created `simple-custom-iot-auth`
* **Enable Token Signing**: `unticked`
* **Activate Authorizer**: `ticked`
3. Click the `Create Authorizer`

### Test authentication process
Testing the authentication process is the same for both `Step 1` and `Step 2`, check the `Test Custom Authorizer` section

# **Step 2**

### Creating an Authorizer Lambda


1. Download the project from GitHub: [aws_iot_core_integration](http://github.com/ayyeka/aws_iot_core_integration)


2. Locate the file  `lambda_function.py` under `aws_iot_authorizer_things_registry`

3. This Lambda will authorize devices with MQTT username and password that match certain attributes unique for each `Thing` registered in aws iot.


4. Upload the edited file to AWS Lambda and create a Lambda function called `aws_iot_authorizer_things_registry` in the same region of your AWS IoT Core

### Creating a Custom Authorizer

1. On AWS IoT Core, navigate to the ‘Secure’ menu and then choose ‘Authorizers’
2. Click the "Create" button and in the next screen configure the following:
* **Name**: `myThingAuth`
* **Authorizer Function**: pick the name of the Lambda you created `aws_iot_authorizer_things_registry`
* **Enable Token Signing**: `unticked`
* **Activate Authorizer**: `ticked`
3. Click the `Create Authorizer`

### Register a device in the Things Registry

We'll need to register things inside aws iot console, open `Manage > Things`

1. Click `Create` then `Create a single thing`
Give it a name, then add attributes under the `Set searchable thing attributes` section.

    | Attribute key | Value | 
    | --- | --- |
    | SECRET_KEY | device auth password |
    | UUID | device auth username |

2. Click `Create thing without certificate`
You should see the thing added under `Things`

### Give the auth Lambda access to `Things registry`

See referenced section bellow
> **Note**: See the “Authentication and Metadata from the Things Registry” section for details on how to allow this Lambda to retrieve authentication information from the Things Registry, **MAKE SURE that any lambda that needs to access the `thing registry` granted the ListThings policy, see the mentioned** “Authentication and Metadata from the Things Registry” **section for full details**

### Test Custom Authorizer
> **Note**: We'll be using [pub.py](#) for testing authorisation and data processing, please take a look at the `CONFIG` section inside the code and change the constants depending on your aws info, device username and password...

The [pub.py](#) script takes care of connecting to the authorizer over MQTT, and also publishing protobuf messages, but in this section we're only interested in testing the auth lambdas and the custom authorizer we created in aws iot are working.

So after running the script, you can open your lambda in aws lambda console 
Under `Lambda > Functions > aws_iot_authorizer_things_registry` for example 
Then open `Monitor > Logs`
You should see the routed auth requests sent by the custom authorizer to this lambda.
> **Note**: Note that there is a ~3 mins delay between running your script and aws lambda logs


# **Step 3**
### Creating a Data Processing Lambda

1. Download the project from GitHub: http://github.com/ayyeka/aws_iot_core_integration

2. Under the `aws_iot_data_processing_lambda` you’ll find `lambda_function.py`. This Lambda is has external package dependencies, hence it needs to be zipped together with its dependencies.

3. From the command line, navigate to the `aws_iot_data_processing_lambda` directory and execute the following command to collect all Python packages require by this Lambda:

```
pip install -r requirements.txt -t .
```

4. Zip all the content of the `aws_iot_data_processing_lambda` directory and upload it to AWS Lambda to create a new Lambda called `aws_iot_data_processing_lambda`

5. This Lambda will receive the Protobuf payloads from the device and decode it, and create a user friendly JSON response. 
> See the "Authentication and Metadata from the Things Registry" section for details on how to enhance this Lambda with more metadata

### Create a Rule and an Action

1. On AWS IoT Core, navigate to the ‘Act’ menu and then choose ‘Rules’
2. Click the ‘Create’ button and in the next screen configure the following:
* **Name**: `myrule`
* **SQL Version**: `no change`
* **Rule Query Statement**:
```
SELECT 	clientid() as client_id, topic() as topic, encode(*, 'base64') as data, timestamp() as timestamp FROM 'wv/#'
```

* **Action**: Send to Lambda -> Configure Action -> Select `aws_iot_data_processing_lambda` -> Add

3. This rule will match all the data published by the devices by subscribing to the topic “wv/#”
4. The devices’ protobuf binary payloads will be forwarded to the data processing lambda function as Base64 strings

## Test Data Processing rule
> **Note**: We'll be using pub.py for testing authorisation and data processing, please take a look at the `CONFIG` section inside the code and change the constants depending on your aws info, device username and password...

Using the defined protobuf message structures, we can test with an mqtt client using [awsiotsdk](https://aws.github.io/aws-iot-device-sdk-python-v2/).
Take a look at [protobuf docs for python](https://developers.google.com/protocol-buffers/docs/pythontutorial) and the starter [pub.py](#) script.

The script connects and authenticate to aws iot using the simple_authorizer, then publishes multiple protobuf `SamplesBatchMessage` to the `/wv/<AKID>/1/samp/p1` topic.
Message structures are defined under `proto` folder.

You can visualize published protobuf messages in you aws iot console, under `Act > Test` 
Enter the devices topic with it's `/wv/<AKID>/1/samp/p1` and click subscribe.

You should see the received messages but in protobuf encoded format so they won't be readable. 

On the data processing lambda side, you can consult the lambda logs and see messages routed by the aws iot `rule` on `'wv/#'` topics.

Under `Lambda > Functions > aws_iot_data_processing_lambda` 
Then click `Monitor` then `Logs` 
> **Note**: Note that there is a ~3 mins delay between running your script and aws lambda logs

Under logs you should see the decoded protobuf messages.

## Device Side Configuration
1. On the FAI platform, navigate to the ‘Advanced Device Configuration’ -> ‘GSM’ module configuration
2. To get the  `<AWS IoT Endpoint URL>` go to **AWS IoT Core** -> **Setting**. You will find your url under **Device data endpoint** tab
3. For `username` and `password` fields refer to **Creating an Authorizer Lambda** section above
3. Configure the following items: <br>


| Item Name | Value | Comments | 
| --- | --- | --- |
| MQTT Server Address | `<AWS IoT Endpoint URL>` Example: azyffu1i8-ats.iot.eu-west-1.amazonaws.com | Max length: 100 characters |
| MQTT Server Port | 443 | |
| mqtt_handler | AWS_IOT_PROTOBUF |This setting triggers the TLS SNI and ALPN extensions, and disables the MQTT retain flag |
| mqtt_client_id | | Leave empty |
| User_defined_mqtt_user | `<username>`?x-amz-customauthorizer-name=**myauth** | Note: `<username>` will be passed to the authorizer lambda that is connected to the **myauth** IoT Core Authorizer <br> **Firmware v2.394** Max length: 45 characters <br> **Firmware v2.395 and above** Max length: 100 characters |
| User_defined_mqtt_pass | `<password>` | **Note 1**: `<password>` will be passed to the authorizer lambda that is connected to the **myauth** IoT Core Authorizer <br> **Note 2**: do not leave empty, otherwise the user_defined_mqtt_user field will be ignored. <br> Max length: 25 characters |


> **Important note**: make sure the <username> and <password> configured here will be accepted by the Authorizer Lambda you configured in the previous steps
  
  
## Testing the work of Authorizer Lambda
  
1. Download and install mosquitto. Various installation tutorials are available [here](https://mosquitto.org/download/). Here is a [good Ubuntu installation tutorial](https://www.vultr.com/docs/how-to-install-mosquitto-mqtt-broker-server-on-ubuntu-16-04)
2. Download the AmazonRootCA1.pem file from [here](https://www.amazontrust.com/repository/AmazonRootCA1.pem) . We will need it later
3. To get the endpoint link go to **AWS IoT Core** -> **Settings**. You will find your endpoint url under **Device data endpoint** tab
4. Don't forget to include your AWS `<username>` , `<password>` , `<AWSLambdaAuth>`. Pay attention to `-t` and `--will-topic` params. The topics should have the following format to be accepted by the authorizer `wv/*`. Note that on the previous steps we set `<AWSLambdaAuth>=myauth` when setting up authorizers on IoT Core. `<myClientName>` can be any for now, as it is not validated in `aws_iot_authorizer_simple`, though you may want to include it, if you are using your custom authorizer.
5. Run the following command <br>
```mosquitto_pub -h "[MY_ENDPOINT]-ats.iot.ap-southeast-2.amazonaws.com" -p 443 -t "wv/sample" -m "Hello World" -i "<myClientName>" -u "<username>?x-amz-customauthorizer-name=<AWSLambdaAuth>" -P "<password>" --tls-alpn mqtt --cafile AmazonRootCA1.pem --will-payload "Goodbye" --will-topic "wv/lastwill" --will-qos 1 --repeat 10 --repeat-delay 1 --debug```
6. If you have done everything correctly, your client should get authorized and you will start recieving `PUBLISH` messages. 
7. Now you can go to the page with your `simple-custom-iot-auth` -> `Monitor` -> `Logs` and see that the recent invocation appeared!
  
 
![picture_8](images/picture_8.PNG)

  
## Authentication and Metadata from the Things Registry (OPTIONAL)
  
In case we use `aws_iot_authorizer_simple`, our Lambda functions were basic:
* The MQTT username & password were verified against constants in the Lambda’s code
* The data processing lambda merely translated the Protobuf to JSON

This is useful for integration PoC, but less so for production deployments. 
New objective:
* Verify the MQTT credentials devices against the Things Registry
* Add additional metadata to the response JSON of the data processing Lambda

The process:
* Create a thing `Type`, this will allow us to created multiple `Things` from the same type (same attributes)
* Create a `Thing` and populate its metadata fields (e.g. UUID, SECRET_KEY etc) under attributes section
* Create a new Authorizer in aws iot and add the `aws_iot_authorizer_things_registry` lambda to it while creating
* Grant the two lambdas that use the `thing registy` access, `aws_iot_authorizer_things_registry` and `aws_iot_data_processing_lambda`, go to your [IAM dashboard](https://console.aws.amazon.com/iam/home#/roles), here you'll find a predefined `role` given to each lambda, we need to make sure our lambdas can are allowed to access the `iot registery` : 
    * Click on the correponding role (example : aws_iot_authorizer_things_registry-role-4zaa3q3w, this can have different ending id in your case)
    * Click on `+ Add inline policy`
    * Enter "iot" in the `Service` field and select `IoT`
    * Expand the `List` dropdown under `Access level`
    * Choose `ListThings` then click the `Review policy` button
    * Give the policy name then click `Create Policy`
