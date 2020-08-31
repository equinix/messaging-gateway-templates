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

import datetime
import json
import time
import uuid

from azure.servicebus.aio import ReceiveSettleMode, ServiceBusClient

from config.config import (EQUINIX_INCOMING_QUEUE, EQUINIX_OUTGOING_QUEUE,
                           EQUINIX_OUTGOING_QUEUE_CONNECTION_STRING, SOURCE_ID)
from util.service_bus_base import send_to_topic_message


def datetime_iso_format(date):
    return date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

async def create_workvisit_wrapper_helper(json_obj):
    visitor_array = []
    temp = {
        "FirstName":"Test FirstName",
        "LastName":"Test LastName",
        "CompanyName":"Test Company"
    }
    for visitor in json_obj["serviceDetails"]["visitors"]:
        temp["FirstName"] = visitor["firstName"]
        temp["LastName"] = visitor["lastName"]
        temp["CompanyName"] = visitor["company"]
        visitor_array.append(temp)

    res = {
        "CustomerContact": json_obj["contacts"][0]["userName"],
        "RequestorId": json_obj["customerReferenceNumber"],
        "RequestorIdUnique": False,
        "Location": json_obj["ibxLocation"]["cages"][0]["cage"],
        "Attachments": json_obj["attachments"],
        "Description": json_obj["serviceDetails"]["additionalDetails"],
        "ServiceDetails": {
            "StartDateTime": json_obj["serviceDetails"]["schedule"]["startDateTime"],
            "EndDateTime": json_obj["serviceDetails"]["schedule"]["endDateTime"],
            "OpenCabinet": json_obj["serviceDetails"]["openCabinet"],
            "Visitors": visitor_array
        }
    }
    return res

async def update_workvisit_wrapper_helper(json_obj):
    res = {
        "ServicerId": json_obj["orderNumber"] if "orderNumber" in json_obj else None,
        "RequestorId": json_obj["customerReferenceNumber"] if "customerReferenceNumber" in json_obj else None,
        "Attachments": json_obj["attachments"] if "attachments" in json_obj else None,
        "Description": json_obj["serviceDetails"]["additionalDetails"] if ("serviceDetails" in json_obj and "additionalDetails" in json_obj['serviceDetails']) else None,
        "ServiceDetails": {
            "StartDateTime": json_obj["serviceDetails"]["startDateTime"] if ("serviceDetails" in json_obj and "startDateTime" in json_obj["serviceDetails"]) else None,
            "EndDateTime": json_obj["serviceDetails"]["endDateTime"] if ("serviceDetails" in json_obj and "endDateTime" in json_obj["serviceDetails"]) else None,
            "OpenCabinet": json_obj["serviceDetails"]["openCabinet"] if ("serviceDetails" in json_obj and "openCabinet" in json_obj["serviceDetails"]) else None,
            "Visitors": json_obj["serviceDetails"]["visitors"] if ("serviceDetails" in json_obj and "visitors" in json_obj["serviceDetails"]) else None
        }
    }
    return res



async def cancel_workvisit_wrapper_helper(json_obj):
    res = {
        "State": "Cancelled",
        "RequestorId": json_obj["customerReferenceNumber"] if 'customerReferenceNumber' in json_obj else None,
        "ServicerId": json_obj["orderNumber"] if 'orderNumber' in json_obj else None,
        "Attachments": json_obj["attachments"] if 'attachments' in json_obj else None,
        "Description": json_obj["cancellationReason"] if 'cancellationReason' in json_obj else None
    }
    return res


async def message_processor(json_obj, action_verb, resource_type, client_id, client_secret):
    verb = action_verb
    null = None
    body_payload = ""

    if action_verb == "Cancelled":
        verb = "Update"

    if resource_type == "WorkVisit":
        if action_verb == "Create":
            body_payload = await create_workvisit_wrapper_helper(json_obj)
        elif action_verb == "Update":
            body_payload = await update_workvisit_wrapper_helper(json_obj)
        elif action_verb == "Cancelled":
            body_payload = await cancel_workvisit_wrapper_helper(json_obj)
        json_obj = body_payload

    message_input = get_payload(json_obj, verb, resource_type, client_id, client_secret)
    message_input["Task"] = json.dumps(message_input["Task"])
    message_id = json.loads(message_input["Task"])["Id"]
    message_to_send = json.dumps(message_input)
    try:
        await send_to_topic_message(EQUINIX_INCOMING_QUEUE, message_to_send, "IOMA-Message")
        queueMsg = await loop_read_queue( message_id, null)
        return queueMsg
    except Exception as err:
        if "Invalid authorization token signature" in err.args[0]:
             return exception_handler("Invalid incoming queue connection string. Either Client Shared Key Name/Shared Key value is invalid.", 400)
        if err.status_code == 404 or "AzureMissingResourceHttpError" in err.args[0]:
            return exception_handler("Invalid connection string. Invalid incoming queue name for {0}".format(EQUINIX_INCOMING_QUEUE), 400)
        


def get_payload(json_obj, verb, resource_type, client_id, client_secret):
    authentication = {}
    null = None
    message_input = {
        "Task": {
            "Id": str(uuid.uuid4()),
            "Verb": verb,
            "Source": SOURCE_ID,
            "Version": "1.0",
            "Resource": resource_type,
            "ContentType": "application/json",
            "CreateTimeUTC": str(datetime_iso_format(datetime.datetime.now())),
            "OriginationId": null,
            "OriginationVerb": null,
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


def response_message_success(response_json_obj):
    res = {
        "status": "Success",
        "Description": response_json_obj["Body"]["Description"],
        "errorCode": "",
        "errorMessage": ""
    }
    res["statusCode"] = response_json_obj["Body"]["StatusCode"]
    return res


def response_message_error(response_json_obj):
    res = {
        "errors": [{
            "code": response_json_obj["Body"]["StatusCode"],
            "message": response_json_obj["Body"]["Description"]
        }]
    }
    res["statusCode"] = response_json_obj["Body"]["StatusCode"]
    return res


def wv_response_message_error(response_json_obj):
    res = {
        "errors": [{
            "code": response_json_obj["Body"]["StatusCode"],
            "message": response_json_obj["Body"]["Description"]
        }]
    }
    return res


def create_wv_response_message_success(response_json_obj, request_json_obj):
    null = None
    res = {
        "successes": [
            {
                "ibxLocation": {
                    "ibxTime": null,
                    "timezone": null,
                    "ibx": null,
                    "region": null,
                    "address1": null,
                    "city": null,
                    "state": null,
                    "country": null,
                    "zipCode": null,
                    "cageDetails": [
                        {
                            "cage": request_json_obj["ibxLocation"]["cages"][0]["cage"],
                            "cageUSID": null,
                            "systemName": null,
                            "accountNumber": null,
                            "cabinets": [
                                {
                                    "cabinet": null
                                }
                            ],
                            "notes": [
                                {
                                    "noteDescription": null,
                                    "noteType": ""
                                }
                            ],
                            "multiCabinet": False
                        }
                    ]
                },
                "response": {
                    "OrderNumber": response_json_obj["Body"]["ServicerId"]
                }
            }
        ]}
    res["statusCode"] = response_json_obj["Body"]["StatusCode"]
    return res


def exception_handler(err, status_code):
    res = {
            "errors": [{
                "code": status_code,
                "message": err
            }]
        }
    if 'args' in err:
        res["errors"][0]["message"] = err.args[0]
    return res


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
    

async def loop_read_queue(message_id, filters):
    timeout = time.time() + 60*1   # 1 minutes 
    while 1:
        try:
            response = await read_from_destination_queue(EQUINIX_OUTGOING_QUEUE_CONNECTION_STRING, EQUINIX_OUTGOING_QUEUE, message_id, filters)
            if time.time() > timeout:
                return exception_handler("Could not find corresponding response message in the outgoing queue",400)
            if response:
                return response
        except Exception as err:
            return exception_handler("Error while reading outgoing queue", 400)
        

async def read_from_destination_queue(connection_string, queue_name, message_id, filters):
    res = []
    try:
        client = ServiceBusClient.from_connection_string(conn_str=connection_string)
        queue_client = client.get_queue(queue_name=queue_name)
        # Receive the message from the queue
        async with queue_client.get_receiver(mode=ReceiveSettleMode.PeekLock, prefetch=10) as receiver :
            batch = await receiver.fetch_next(max_batch_size=10)
            for message in batch:
                try:
                    message
                except NameError:
                    res.append("No msgs to read")
                    break
                if filters:
                    json_temp = json.loads(str(message))["Task"]
                    json_obj = json.loads(json_temp)
                    if json_obj:
                        result = filter_notification(json_obj, filters)                        
                        if len(result) > 0:
                            res.append(json_obj)
                            await message.complete()
                            break
                else:
                    json_temp = json.loads(str(message))["Task"]
                    json_obj = json.loads(json_temp)
                    if json_obj["OriginationId"] == message_id and json_obj["Verb"] == "Ack":
                        res.append(json_obj)
                        await message.complete()
                        break
        if len(res) > 0 :
            return json.dumps(res[0])
        await receiver.close()
    except Exception as err:
        QUEUE_ERROR_MESSAGE = "Specificed queue does not exist."
        UNAUTHORIZED_MESSAGE = "Unauthorized"
        if err.args[0] == QUEUE_ERROR_MESSAGE:
            return exception_handler("Invalid connection string. Invalid outgoing queue name for {0}".format(queue_name),400)
        if UNAUTHORIZED_MESSAGE in err.args[0]:
            return exception_handler("Invalid outgoing queue connection string. Either Client Shared Key Name/Shared Key value is invalid.",400)
    finally:
        pass
