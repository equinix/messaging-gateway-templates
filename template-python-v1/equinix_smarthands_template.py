# EQUINIX MESSAGING GATEWAY SMARTHANDS TEMPLATE

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

from util.message_util import (exception_handler, loop_read_queue,
                               message_processor, response_message_error,
                               response_message_success)


async def create_smarthands(request_json, client_id, client_secret):
    '''Sends the given create SmartHands message to Equinix Incoming Queue.

        Args:
            request_json (str): Message to send.
            client_id (str): Equinix issued client_id.
            client_secret (str): Equinix issued client_secret.

        Raises:
            obj: returns an error while processing message.

        Returns:
            str: Received response message
        '''
    ERROR_MESSAGE = "Processing failed with following error: "
    request_json_obj = json.loads(request_json)
    try:
        service_bus_response = await message_processor(request_json_obj, "Create", "SmartHands",client_id, client_secret)
        if 'errors' in service_bus_response:
            return service_bus_response
        response_json_obj = json.loads(service_bus_response)
        if response_json_obj["Body"]["StatusCode"] == 201 :
            return response_message_success(response_json_obj)
        else:
            if response_json_obj["Body"]["Description"] in ERROR_MESSAGE:
                res = json.loads(response_json_obj["Body"]["Description"].replace(ERROR_MESSAGE, ""))
                res["statusCode"] = response_json_obj["Body"]["StatusCode"]
                return res
            else:
                return response_message_error(response_json_obj)
    except Exception as err:
        return exception_handler(err, 400)


async def update_smarthands(request_json, client_id, client_secret):
    '''Sends the given update SmartHands message to Equinix Incoming Queue.

        Args:
            request_json (str): Message to send.
            client_id (str): Equinix issued client_id.
            client_secret (str): Equinix issued client_secret.

        Raises:
            obj: returns an error while processing message.

        Returns:
            str: Received response message
        '''
    ERROR_MESSAGE = "Processing failed with following error: "
    MULTIPLE_MESSAGE_ERROR = "Multiple tickets found for RequestorID"
    request_json_obj = json.loads(request_json)
    try:
        service_bus_response = await message_processor(request_json_obj, "Update", "SmartHands", client_id, client_secret)
        if 'errors' in service_bus_response:
            return service_bus_response
        response_json_obj = json.loads(service_bus_response)
        if response_json_obj["Body"]["StatusCode"] == 202 :
            return response_message_success(response_json_obj)
        else:
            if response_json_obj["Body"]["Description"] in ERROR_MESSAGE:
                res = json.loads(response_json_obj["Body"]["Description"].replace(ERROR_MESSAGE, ""))
                res["statusCode"] = response_json_obj["Body"]["StatusCode"]
                return res
            elif response_json_obj["Body"]["StatusCode"] == 404 or MULTIPLE_MESSAGE_ERROR in response_json_obj["Body"]["Description"]:
                return exception_handler(MULTIPLE_MESSAGE_ERROR, 400)
            else:
                return response_message_error(response_json_obj)
    except Exception as err:
        return exception_handler(err, 400)


async def cancel_smarthands(request_json, client_id, client_secret):
    '''Sends the given cancel SmartHands message to Equinix Incoming Queue.

        Args:
            request_json (str): Message to send.
            client_id (str): Equinix issued client_id.
            client_secret (str): Equinix issued client_secret.

        Raises:
            obj: returns an error while processing message.

        Returns:
            str: Received response message
        '''
    ERROR_MESSAGE = "Processing failed with following error: "
    request_json_obj = json.loads(request_json)
    try:
        service_bus_response = await message_processor(request_json_obj, "Cancelled", "SmartHands", client_id, client_secret)
        if 'errors' in service_bus_response:
            return service_bus_response
        response_json_obj = json.loads(service_bus_response)
        if response_json_obj["Body"]["StatusCode"] == 202 :
            return response_message_success(response_json_obj)
        else:
            if response_json_obj["Body"]["Description"] in ERROR_MESSAGE:
                res = json.loads(response_json_obj["Body"]["Description"].replace(ERROR_MESSAGE, ""))
                res["statusCode"] = response_json_obj["Body"]["StatusCode"]
                return res
            else:
                return response_message_error(response_json_obj)
    except Exception as err:
        return exception_handler(err, 400)

async def get_notifications(customer_reference_number, servicer_id, activity_id, state):
    '''Receive SmartHands notification that matches the filter criteria from Equinix Outgoing Queue.

        Args:
            customer_reference_number (str): Customer Reference Number used for searching SmartHands order
            servicer_id (str): Order Number used for searching SmartHands order
            activity_id (str): Activity ID used for searching SmartHands Activity
            state (str): SmartHands order state (eg: Open, InProgress, Pending Customer Input, Cancelled, Closed) 

        Raises:
            obj: if the service returns an error while retrieving notification.

        Returns:
            str: Received response message
        '''
    all_filters = {"ResourceType": "SmartHands"}
    if customer_reference_number:
        all_filters.update({"RequestorId": customer_reference_number})
    if servicer_id:
        all_filters.update({"ServicerId": servicer_id})
    if activity_id:
        all_filters.update({"Activity": activity_id})
    if state:
        all_filters.update({"State": state})
    queue_message = await loop_read_queue( None, all_filters)
    return queue_message