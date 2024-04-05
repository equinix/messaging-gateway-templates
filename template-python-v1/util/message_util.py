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

import base64
import datetime
import json
import time
import uuid
from datetime import timezone
from http import HTTPStatus
import urllib.request
import os
from urllib.parse import urlparse

from config.config import (EQUINIX_INCOMING_QUEUE, EQUINIX_OUTGOING_QUEUE,
                           EQUINIX_OUTGOING_QUEUE_CONNECTION_STRING, SOURCE_ID,FILE_STORAGE_DIRECTORY,FILE_STORAGE_URL,FILE_STORAGE_UPLOAD_KEY,FILE_STORAGE_DOWNLOAD_KEY)
from util.service_bus_base import read_messages_from_queue, send_message_to_queue
from azure.storage.blob import BlobServiceClient, upload_blob_to_url


FAILED_ESTABLISH_CONNECTION = "Please confirm target hostname exists"
INVALID_ENTITY = "Invalid connection string. Please check the target host"
INVALID_INCOMING_QUEUE_CONNECTION = "Invalid incoming queue connection string. Either NameSpace or Client Shared Key Name/Shared Key value is invalid."
INVALID_OUTGOING_QUEUE_CONNECTION = "Invalid outgoing queue connection string. Either Client Shared Key Name/Shared Key value is invalid."
INVALID_TOKEN_SIGNATURE = "CBS Token authentication failed"
INTERNAL_SERVER_ERROR = 'Internal Server Error'
ACK = "Ack"

CREATE_OPERATION = "Create"
UPDATE_OPERATION = "Update"
CANCEL_OPERATION = "Cancelled"
TICKET_TYPE_SHIPPING = "Shipping"
TICKET_TYPE_SMARTHANDS = "SmartHands"
TICKET_TYPE_WORKVISIT = "WorkVisit"
TICKET_TYPE_BREAKFIX = "BreakFix"
TICKET_TYPE_CROSSCONNECT = "CrossConnect"


def datetime_iso_format(date):
    return date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

async def message_processor(json_obj, action_verb, resource_type, client_id, client_secret, isOAuthType):
    verb = action_verb
    message_input = None
    if action_verb == "Cancelled":
        verb = "Update"
    
    if 'Attachments' in json_obj and len(json_obj['Attachments'])>0:
        json_obj['Attachments'] = await uploadAllAttachments(json_obj['Attachments'])

    if resource_type == TICKET_TYPE_CROSSCONNECT:
        try:
            if json_obj['ConnectionDetails'] and len(json_obj['ConnectionDetails']) > 0 :
                for details in json_obj["ConnectionDetails"]:
                    if details['ZSide'] and details['ZSide']['LOAAttachment'] and len(details['ZSide']['LOAAttachment']) > 0 :
                        LOAAttachment = await uploadAllAttachments([details['ZSide']['LOAAttachment']])
                        details['ZSide']['LOAAttachment'] = LOAAttachment[0]
        except:
            pass
    if(isOAuthType):
        message_input = create_payload_using_oauth(json_obj, verb, resource_type, client_secret)
    else:
        message_input = create_payload(json_obj, verb, resource_type, client_id, client_secret)
         
    message_input["Task"] = json.dumps(message_input["Task"])
    message_id = json.loads(message_input["Task"])["Id"]
    try:
       send_message_to_queue(json.dumps(message_input))
    except Exception as err:
        return process_error_response(err, "send", json.loads(message_input["Task"]))
    try:
        queue_msg = await read_from_queue(message_id, None)
        if queue_msg == None:
            return json.loads(json.dumps(format_error_response(HTTPStatus.NOT_FOUND, "Order is still Processing", message_input)))
        else:
            return queue_msg
    except Exception as err:
        return process_error_response(err, "receive", json.loads(message_input["Task"]))


def create_payload(json_obj, verb, resource_type, client_id, client_secret):
    authentication = {}
    message_input = {
        "Task": {
            "Id": str(uuid.uuid4()),
            "Verb": verb,
            "Source": SOURCE_ID,
            "Version": "1.0",
            "Resource": resource_type,
            "ContentType": "application/json",
            "CreateTimeUTC": str(datetime_iso_format(datetime.datetime.now(tz=timezone.utc))),
            "OriginationId": None,
            "OriginationVerb": None,
            "Body": json_obj
        }
    }

    authentication["Authentication"] = {
        "ClientId": client_id,
        "ClientSecret": client_secret
    }
    if client_id and client_secret:
        message_input.update(authentication)

    return message_input

def create_payload_using_oauth(json_obj, verb, resource_type, oauth_token):
    authentication = {}
    message_input = {
        "Task": {
            "Id": str(uuid.uuid4()),
            "Verb": verb,
            "Source": SOURCE_ID,
            "Version": "1.0",
            "Resource": resource_type,
            "ContentType": "application/json",
            "CreateTimeUTC": str(datetime_iso_format(datetime.datetime.now(tz=timezone.utc))),
            "OriginationId": None,
            "OriginationVerb": None,
            "Body": json_obj
        }
    }

    authentication["Authentication"] = {
        "AccessToken": oauth_token
    }
    if client_id and client_secret:
        message_input.update(authentication)

    return message_input


def format_error(status_code, description):

    return {
        "Body": {
            "StatusCode": status_code,
            "Description": description
        }
    }


def format_error_response(status_code, description, message_input):
    res = {
        "Id": str(uuid.uuid4()),
        "Body": {
            "StatusCode": status_code,
            "Description": description
        },
        "Verb": ACK,
        "Source": SOURCE_ID,
        "Version": "1.0",
        "Resource": message_input["Resource"],
        "ContentType": "application/json",
        "CreateTimeUTC": str(datetime_iso_format(datetime.datetime.now(tz=timezone.utc))),
        "OriginationId": None,
        "OriginationVerb": None
    }

    if message_input and "Task" in message_input:
        task_message = json.loads(message_input["Task"])

        if "Verb" in task_message:
            res["OriginationVerb"] = task_message["Verb"]

        if "Id" in task_message:
            res["OriginationId"] = task_message["Id"]

        if "Resource" in task_message:
            res["Resource"] = task_message["Resource"]

    if 'args' in description:
        res["Body"]["Description"] = description.args[0]
        return res
    return res


def process_error_response(error_obj, mode, message_input):
    # if FAILED_ESTABLISH_CONNECTION in str(error_obj.args[0]):
    #     return json.dumps(format_error_response(HTTPStatus.BAD_REQUEST, INVALID_INCOMING_QUEUE_CONNECTION, message_input))

    error = json.loads(json.dumps(format_error(
        HTTPStatus.BAD_REQUEST, error_obj.args[0])))
    if "Body" in error:
        if mode == 'send':
            if "Description" in error["Body"] and (FAILED_ESTABLISH_CONNECTION in error["Body"]["Description"]):
                return json.dumps(format_error_response(HTTPStatus.BAD_REQUEST, INVALID_ENTITY, message_input))
            elif "Description" in error["Body"] and (str(HTTPStatus.NOT_FOUND.value) in error["Body"]["Description"] or INVALID_TOKEN_SIGNATURE in error["Body"]["Description"]):
                return json.dumps(format_error_response(HTTPStatus.BAD_REQUEST, INVALID_INCOMING_QUEUE_CONNECTION, message_input))
            else:
                return json.dumps(format_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, INTERNAL_SERVER_ERROR, message_input))

        elif mode == 'receive':
            if "Description" in error["Body"] and FAILED_ESTABLISH_CONNECTION in error["Body"]["Description"]:
                return json.dumps(format_error_response(HTTPStatus.BAD_REQUEST, INVALID_ENTITY, message_input))
            elif "Description" in error["Body"] and INVALID_TOKEN_SIGNATURE in error["Body"]["Description"]:
                return json.dumps(format_error_response(HTTPStatus.BAD_REQUEST, INVALID_OUTGOING_QUEUE_CONNECTION, message_input))
            else:
                return json.dumps(format_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, INTERNAL_SERVER_ERROR, message_input))
    else:
        return json.dumps(format_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, INTERNAL_SERVER_ERROR, message_input))

async def read_from_queue(message_id, filters):
    res = []
    receiver = read_messages_from_queue()
    with receiver:
        count = 3
        # if filters != None:
        #     count = 1
        for i in range(count):
            if filters == None:
                time.sleep(5)
            received_msgs = receiver.receive_messages(
                max_message_count=25, max_wait_time=30)
            for message in received_msgs:
                if filters:
                    json_temp = json.loads(str(message))["Task"]
                    json_obj = json.loads(json_temp)
                    if json_obj:
                        result = filter_notification(json_obj, filters)
                        if len(result) > 0:
                            res.append(json_obj)
                            receiver.complete_message(message)
                            break
                else:
                    json_temp = json.loads(str(message))["Task"]
                    json_obj = json.loads(json_temp)
                    if json_obj["OriginationId"] == message_id and json_obj["Verb"] == ACK:
                        res.append(json_obj)
                        receiver.complete_message(message)
                        break
            if len(res) > 0:
                receiver.close()
                return res[0]   


def filter_notification(list_obj, filters):
    result = []
    all_filters = []
    if list_obj["Resource"]:
        f1 = lambda x: x["Resource"] == filters["ResourceType"]
        all_filters.append(f1)
    
    if filters:
        if not "State" in list_obj["Body"]:
            list_obj["Body"]["State"] =  ""
        if not "RequestorId" in list_obj["Body"]:
            list_obj["Body"]["RequestorId"] =  ""
        if not "ServicerId" in list_obj["Body"]:
            list_obj["Body"]["ServicerId"] =  ""
        if not "Activity" in list_obj["Body"]:
            list_obj["Body"]["Activity"] =  ""
        # filter by requestor id
        if "RequestorId" in filters:
            f2 = lambda x: x["Body"]["RequestorId"] == filters["RequestorId"] 
            all_filters.append(f2)
        # filter by servicer id
        if "ServicerId" in filters:
            f3 = lambda x: x["Body"]["ServicerId"] == filters["ServicerId"] 
            all_filters.append(f3)
        # filter by activity id
        if "Activity" in filters:
            f4 = lambda x: x["Body"]["Activity"] == filters["Activity"] 
            all_filters.append(f4)
        # filter by state
        if "State" in filters:
            f5 = lambda x: x["Body"]["State"] == filters["State"] 
            all_filters.append(f5)
    
    result = list(filter(lambda x : all([f(x) for f in all_filters]), [list_obj]))
    return result

async def uploadAllAttachments(attachments):
    newAttachments = []
    for attachment in attachments:
        if "Data" not in attachment:
            newAttachments.append(attachment)
            break
        data = base64.b64decode(attachment["Data"])
        newAttachment = await uploadFile(data,attachment["Name"])
        newAttachments.append(newAttachment)
    return newAttachments

async def uploadFile(data, originalFileName: str):
    try:
        lastSplitIndex = originalFileName.rindex(".")
        fileName = originalFileName[0: lastSplitIndex]
        fileExtension = originalFileName.split(".").pop()
        blobName = fileName+str(int(round(time.time() * 1000)))+'.'+fileExtension
        
        blobServiceClient =  BlobServiceClient(account_url=FILE_STORAGE_URL, credential=FILE_STORAGE_UPLOAD_KEY)
        containerClient = blobServiceClient.get_container_client(FILE_STORAGE_DIRECTORY)
        blockBlobClient = containerClient.get_blob_client(blobName)
        blockBlobClient.upload_blob(data)
        url = urlparse(blockBlobClient.url)
        return {"Name": blobName, "Url":url.scheme+"://"+url.netloc+url.path}
    except Exception as e:
        print(e)


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

def encodeFileToBase64(path):
    data = ""
    with open(path, "rb") as file:
        data =  base64.b64encode(file.read())
    print("encode")
    return data
