# EQUINIX MESSAGING GATEWAY WORKVISIT TEMPLATE

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

import asyncio
import datetime
import json
import time
import uuid
from http import HTTPStatus

from util.message_util import (CANCEL_OPERATION, CREATE_OPERATION,
                               TICKET_TYPE_WORKVISIT, UPDATE_OPERATION,
                               message_processor, read_from_queue)


async def create_workvisit (request_json,client_id, client_secret):
    """Sends the create WorkVisit message to Equinix Messaging Gateway.

        Args:
            request_json (str): Message to send.
            client_id (str): Equinix issued client_id.
            client_secret (str): Equinix issued client_secret.

        Raises:
            obj: returns an error if Equinix Messaging Gateway returns an error while processing the message.

        Returns:
            str: Received response message
        """
    json_obj = json.loads(request_json)
    response_json = await message_processor(json_obj, CREATE_OPERATION, TICKET_TYPE_WORKVISIT, client_id, client_secret)
    return response_json


async def update_work_visit(request_json,client_id, client_secret):
    """Sends the update WorkVisit message to Equinix Messaging Gateway.

        Args:
            request_json (str): Message to send.
            client_id (str): Equinix issued client_id.
            client_secret (str): Equinix issued client_secret.

        Raises:
            obj:  returns an error if Equinix Messaging Gateway returns an error while processing the message.

        Returns:
            str: Received response message
        """
    json_obj = json.loads(request_json)
    response_json = await message_processor(json_obj, UPDATE_OPERATION, TICKET_TYPE_WORKVISIT, client_id, client_secret)
    return response_json


async def cancel_work_visit(request_json,client_id, client_secret):
    """Sends the cancel WorkVisit message to Equinix Messaging Gateway.

        Args:
            request_json (str): Message to send.
            client_id (str): Equinix issued client_id.
            client_secret (str): Equinix issued client_secret.

        Raises:
            obj: returns an error if Equinix Messaging Gateway returns an error while processing the message.

        Returns:
            str: Received response message
        """
    json_obj = json.loads(request_json)
    response_json = await message_processor(json_obj, CANCEL_OPERATION, TICKET_TYPE_WORKVISIT, client_id, client_secret)
    return response_json
   

async def create_workvisit_extn (request_json,client_id, client_secret):
    """Sends the create WorkVisit message to Equinix Messaging Gateway as per API Schema.

        Args:
            request_json (str): Message to send.
            client_id (str): Equinix issued client_id.
            client_secret (str): Equinix issued client_secret.

        Raises:
            obj: returns an error if Equinix Messaging Gateway returns an error while processing the message.

        Returns:
            str: Received response message
        """
    json_obj = json.loads(request_json)
    json_obj = await create_workvisit_request_wrapper(json_obj)
    response_json = await message_processor(json_obj, CREATE_OPERATION, TICKET_TYPE_WORKVISIT, client_id, client_secret)
    return create_workvisit_response_wrapper(response_json, json.loads(request_json))


async def update_work_visit_extn (request_json,client_id, client_secret):
    """Sends the update WorkVisit message to Equinix Messaging Gateway as per API Schema.

        Args:
            request_json (str): Message to send.
            client_id (str): Equinix issued client_id.
            client_secret (str): Equinix issued client_secret.

        Raises:
            obj: returns an error if Equinix Messaging Gateway returns an error while processing the message.

        Returns:
            str: Received response message
        """
    json_obj = json.loads(request_json)
    json_obj = await update_workvisit_request_wrapper(json_obj)
    response_json = await message_processor(json_obj, UPDATE_OPERATION, TICKET_TYPE_WORKVISIT, client_id, client_secret)
    return workvisit_response_wrapper(response_json)


async def cancel_work_visit_extn(request_json,client_id, client_secret):
    """Sends the cancel WorkVisit message to Equinix Messaging Gateway as per API Schema.

        Args:
            request_json (str): Message to send.
            client_id (str): Equinix issued client_id.
            client_secret (str): Equinix issued client_secret.

        Raises:
            obj: returns an error if Equinix Messaging Gateway returns an error while processing the message.

        Returns:
            str: Received response message
        """
    json_obj = json.loads(request_json)
    json_obj = await cancel_workvisit_request_wrapper(json_obj)
    response_json = await message_processor(json_obj, CANCEL_OPERATION, TICKET_TYPE_WORKVISIT, client_id, client_secret)
    return workvisit_response_wrapper(response_json)


async def get_notifications(requestor_id, servicer_id, activity_id, ticket_state):
    """Receive ticket notification from Equinix Messaging Gateway that matches the provided filter criteria.

        Args:
            requestor_id (str): Customer Reference Number of the WorkVisit ticket.
            servicer_id (str): Ticket Number of the WorkVisit ticket.
            activity_id (str): Activity Number of the WorkVisit ticket.
            ticket_state (str): State of the WorkVisit ticket (ex: Open, InProgress, Pending Customer Input, Cancelled, Closed). 

        Raises:
            obj: returns an error if Equinix Messaging Gateway returns an error while retrieving notification.

        Returns:
            str: Received notification message
        """
    all_filters = {"ResourceType": TICKET_TYPE_WORKVISIT}
    if requestor_id:
        all_filters.update({"RequestorId": requestor_id})
    if servicer_id:
        all_filters.update({"ServicerId": servicer_id})
    if activity_id:
        all_filters.update({"Activity": activity_id})
    if ticket_state:
        all_filters.update({"State": ticket_state})
    notification_msg = await read_from_queue(None, all_filters)
    return notification_msg


async def create_workvisit_request_wrapper(json_obj):
    res = {}
    visitor_array = []
    temp = {
        "FirstName":"Test FirstName",
        "LastName":"Test LastName",
        "CompanyName":"Test Company"
    }
    if "serviceDetails" in json_obj and "visitors" in json_obj["serviceDetails"]:
        for visitor in json_obj["serviceDetails"]["visitors"]:
            temp["FirstName"] = visitor["firstName"] if "firstName" in visitor else None
            temp["LastName"] = visitor["lastName"] if "lastName" in visitor else None
            temp["CompanyName"] = visitor["company"] if "company" in visitor else None
            visitor_array.append(temp)

        response = {
            "RequestorIdUnique": False
        }
        if "contacts" in json_obj and "userName" in json_obj["contacts"][0]:
            response["CustomerContact"] = json_obj["contacts"][0]["userName"]
        else: 
            response["CustomerContact"] = None

        if "customerReferenceNumber" in json_obj:
            response["RequestorId"] = json_obj["customerReferenceNumber"]
        else: 
            response["RequestorId"] = None

        if "ibxLocation" in json_obj and "cages" in json_obj["ibxLocation"] and "cage" in json_obj["ibxLocation"]["cages"][0]:
            response["Location"] = json_obj["ibxLocation"]["cages"][0]["cage"]
        else: 
            response["Location"] = None   

        if "attachments" in json_obj:
            response["Attachments"] = json_obj["attachments"]
        else: 
            response["Attachments"] = None

        if "serviceDetails" in json_obj and "additionalDetails" in json_obj["serviceDetails"]:
            response["Description"] = json_obj["serviceDetails"]["additionalDetails"]
        else: 
            response["Description"] = None

        if "schedule" in json_obj["serviceDetails"] and "startDateTime" in json_obj["serviceDetails"]["schedule"]:
            response["StartDateTime"] = json_obj["serviceDetails"]["schedule"]["startDateTime"]
        else: 
            response["StartDateTime"] = None

        if "schedule" in json_obj["serviceDetails"] and "endDateTime" in json_obj["serviceDetails"]["schedule"]:
            response["EndDateTime"] = json_obj["serviceDetails"]["schedule"]["endDateTime"]
        else: 
            response["EndDateTime"] = None

        if "openCabinet" in json_obj["serviceDetails"]:
            response["OpenCabinet"] = json_obj["serviceDetails"]["openCabinet"]
        else: 
            response["OpenCabinet"] = None
        
        res = {
            "CustomerContact": response["CustomerContact"],
            "RequestorId": response["RequestorId"],
            "RequestorIdUnique": response["RequestorIdUnique"],
            "Location": response["Location"],
            "Attachments": response["Attachments"],
            "Description": response["Description"],
            "ServiceDetails": {
                "StartDateTime": response["StartDateTime"],
                "EndDateTime": response["EndDateTime"],
                "OpenCabinet": response["OpenCabinet"],
                "Visitors": visitor_array
            }
        }
    return res
    

async def update_workvisit_request_wrapper(json_obj):
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


async def cancel_workvisit_request_wrapper(json_obj):
    res = {
        "State": "Cancelled",
        "RequestorId": json_obj["customerReferenceNumber"] if 'customerReferenceNumber' in json_obj else None,
        "ServicerId": json_obj["orderNumber"] if 'orderNumber' in json_obj else None,
        "Attachments": json_obj["attachments"] if 'attachments' in json_obj else None,
        "Description": json_obj["cancellationReason"] if 'cancellationReason' in json_obj else None
    }
    return res


def create_workvisit_response_wrapper(response_json, request_json_obj):
    if not type(response_json) == dict:
        response_json = json.loads(response_json)
    res = {
        "successes": [
            {
                "ibxLocation": {
                    "ibxTime": None,
                    "timezone": None,
                    "ibx": None,
                    "region": None,
                    "address1": None,
                    "city": None,
                    "state": None,
                    "country": None,
                    "zipCode": None,
                    "cageDetails": [
                        {
                            "cage": request_json_obj["ibxLocation"]["cages"][0]["cage"],
                            "cageUSID": None,
                            "systemName": None,
                            "accountNumber": None,
                            "cabinets": [
                                {
                                    "cabinet": None
                                }
                            ],
                            "notes": [
                                {
                                    "noteDescription": None,
                                    "noteType": ""
                                }
                            ],
                            "multiCabinet": False
                        }
                    ]
                },
                "response": {
                    "OrderNumber": response_json["Body"]["ServicerId"] if "ServicerId" in response_json["Body"] else None
                }
            }
        ]}
    res["statusCode"] = response_json["Body"]["StatusCode"]
    return res


def workvisit_response_wrapper(response_json):
    if "Body" in response_json and "Description" in response_json["Body"] and "StatusCode" in response_json["Body"]:
        if response_json["Body"]["StatusCode"] == HTTPStatus.ACCEPTED:
            res = {
                "status": "Success",
                "Description": response_json["Body"]["Description"],
                "errorCode": "",
                "errorMessage": ""
            }
            res["statusCode"] = response_json["Body"]["StatusCode"]
            return res
        else:
            res = {
            "errors": [{
                "code": response_json["Body"]["StatusCode"],
                "message": response_json["Body"]["Description"]
             }]
            }
            return res
    else:
        res = {
            "errors": [{
                "code": HTTPStatus.BAD_REQUEST,
                "message": "Null Exception"
             }]
        }
        return res
