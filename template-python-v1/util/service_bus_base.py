# EQUINIX MESSAGING GATEWAY TEMPLATE

# ************************************************************************
#
#  EQUINIX CONFIDENTIAL
# __________________
#
#   © 2020 Equinix, Inc. All rights reserved.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Terms of Use: https://www.equinix.com/company/legal/terms/
#
# ************************************************************************

# from azure.servicebus import Message, ServiceBusClient
from azure.servicebus import ServiceBusClient, ServiceBusMessage

from config.config import (EQUINIX_INCOMING_QUEUE,
                           EQUINIX_INCOMING_QUEUE_CONNECTION_STRING,
                           EQUINIX_OUTGOING_QUEUE,
                           EQUINIX_OUTGOING_QUEUE_CONNECTION_STRING)


# To use PROXY, please follow below steps
# Enter the proxy_hostname, proxy_port values to below HTTP_PROXY object.
# Sending Message Part: Pass the 3rd argument to "ServiceBusSender.from_connection_string" method as http_proxy=HTTP_PROXY 
# Receiving Message Part: Pass the 3rd argument to "ServiceBusReceiver.from_connection_string" method as http_proxy=HTTP_PROXY 
# This would pass all the traffic to service bus via the supplied proxy
HTTP_PROXY = {
    'proxy_hostname': '192.168.1.128',  # proxy hostname.
    'proxy_port': 8888  # proxy port.
}

def send_message_to_queue(payload):
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=EQUINIX_INCOMING_QUEUE_CONNECTION_STRING, logging_enable=True)
    with servicebus_client:
        sender = servicebus_client.get_topic_sender(topic_name=EQUINIX_INCOMING_QUEUE)
        with sender:
            message = ServiceBusMessage(payload)
            sender.send_messages(message)


def read_messages_from_queue():
    servicebus_receiver = ServiceBusClient.from_connection_string(conn_str=EQUINIX_OUTGOING_QUEUE_CONNECTION_STRING)
    return servicebus_receiver.get_queue_receiver(queue_name=EQUINIX_OUTGOING_QUEUE)
