import paho.mqtt.client as mqtt
from datetime import datetime
import time
import json
import group_2_data_generator as data_generator
import random

broker_address = "broker.emqx.io"
topic = "group2/temperature"


print("creating new instance")
client = mqtt.Client("Group 2 - Publisher")  # create new instance
print("connecting to broker")
client.connect(broker_address)  # connect to broker

# Setup the data
sample_set = data_generator.SampleSet(15)


while True:

    decision = random.randint(1, 100)

    if decision > 90:
        print("Random Error occurred")
        temperature = "String data"
        timestamp = datetime.timestamp(datetime.now())
        datadict = {
            'temp': temperature,
            'time': timestamp
        }
        data = json.dumps(datadict)
        info = client.publish(topic, data)

        info.wait_for_publish()
        print("Publishing to " + topic + " " + str(data))
        print(info.is_published())

    else:
        temperature = sample_set.get_data
        timestamp = datetime.timestamp(datetime.now())
        datadict = {
            'temp': temperature,
            'time': timestamp
        }
        data = json.dumps(datadict)
        info = client.publish(topic, data)

        info.wait_for_publish()
        print("Publishing to " + topic + " " + str(data))
        print(info.is_published())

    time.sleep(1)




