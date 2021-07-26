# EQUINIX MESSAGING GATEWAY SHIPMENT TEMPLATE

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

import urllib.request
import base64
import json
import asyncio
from azure.servicebus import ServiceBusClient
from config.config import (EQUINIX_OUTGOING_QUEUE,
                           EQUINIX_OUTGOING_QUEUE_CONNECTION_STRING,FILE_STORAGE_DOWNLOAD_KEY)

async def receiveMessage():
    with ServiceBusClient.from_connection_string(EQUINIX_OUTGOING_QUEUE_CONNECTION_STRING) as client:
        # max_wait_time specifies how long the receiver should wait with no incoming messages before stopping receipt.  
        # Default is None; to receive forever.
        with client.get_queue_receiver(EQUINIX_OUTGOING_QUEUE) as receiver:
            for msg in receiver:  # ServiceBusReceiver instance is a generator.
                task = json.loads(json.loads(str(msg))['Task'])
                body = task["Body"]
                if 'Attachments' in body and len(body['Attachments'])>0:
                    body['Attachments'] = await downloadAllAttachments(body['Attachments'])
                # Complete the message 
                # receiver.complete_message(msg)
                print(body)

async def downloadFile(url):
    try:
        response = urllib.request.urlopen(url+'?'+FILE_STORAGE_DOWNLOAD_KEY)
        data = response.read()
        return base64.encodebytes(data)
    except Exception as e:
        print(e)

async def downloadAllAttachments(attachments):
    newAttachments = []
    for attachment in attachments:
        if('Url' not in attachment):
            newAttachments.append(attachment)
            continue
        base64 = await downloadFile(attachment['Url'])
        newAttachment = {"Name": attachment['Name'], "Data": base64}
        newAttachments.append(newAttachment)
    return newAttachments

if __name__ == "__main__":
    asyncio.run(receiveMessage()) 
