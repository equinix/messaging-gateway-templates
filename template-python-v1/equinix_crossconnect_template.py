# EQUINIX MESSAGING GATEWAY CROSSCONNECT TEMPLATE

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


from util.message_util import (CANCEL_OPERATION, CREATE_OPERATION,
                               TICKET_TYPE_CROSSCONNECT, UPDATE_OPERATION, downloadAllAttachments,
                               message_processor, read_from_queue)


async def create_crossconnect(request_json, client_id, client_secret):
    """Sends the create CrossConnect message to Equinix Messaging Gateway.

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
    response_json = await message_processor(json_obj, CREATE_OPERATION, TICKET_TYPE_CROSSCONNECT, client_id, client_secret, False)
    return response_json    
               
async def create_crossconnect_oauth(request_json, oauth_token):
    """Sends the create CrossConnect message to Equinix Messaging Gateway.

        Args:
            request_json (str): Message to send.
            oauthToken (str): OAuth token used for authentication.

        Raises:
            obj: returns an error if Equinix Messaging Gateway returns an error while processing the message.

        Returns:
            str: Received response message
        """
    json_obj = json.loads(request_json)
    response_json = await message_processor(json_obj, CREATE_OPERATION, TICKET_TYPE_CROSSCONNECT, None, oauth_token, True)
    return response_json

async def update_crossconnect(request_json, client_id, client_secret):
    """Sends the update CrossConnect message to Equinix Messaging Gateway.

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
    response_json = await message_processor(json_obj, UPDATE_OPERATION, TICKET_TYPE_CROSSCONNECT, client_id, client_secret, False)
    return response_json
   
async def update_crossconnect_oauth(request_json, oauth_token):
    """Sends the update CrossConnect message to Equinix Messaging Gateway.

        Args:
            request_json (str): Message to send.
            oauthToken (str): OAuth token used for authentication.

        Raises:
            obj: returns an error if Equinix Messaging Gateway returns an error while processing the message.

        Returns:
            str: Received response message
        """
    json_obj = json.loads(request_json)
    response_json = await message_processor(json_obj, UPDATE_OPERATION, TICKET_TYPE_CROSSCONNECT, None, oauth_token, True)
    return response_json

async def cancel_crossconnect(request_json, client_id, client_secret):
    """Sends the cancel CrossConnect message to Equinix Messaging Gateway.

        Args:
            request_json (str): Message to send.
            client_id (str): Equinix issued client_id.
            client_secret (str): Equinix issued client_secret.

        Raises:
            obj: returns an error if Equinix Messaging Gateway returns an error while processing the message.

        Returns:
            str: Received response message
        """
    request_json_obj = json.loads(request_json)
    response_json = await message_processor(request_json_obj, CANCEL_OPERATION, TICKET_TYPE_CROSSCONNECT, client_id, client_secret, False)
    return response_json

async def cancel_crossconnect_oauth(request_json, oauth_token):
    """Sends the cancel CrossConnect message to Equinix Messaging Gateway.

        Args:
            request_json (str): Message to send.
            oauthToken (str): OAuth token used for authentication.

        Raises:
            obj: returns an error if Equinix Messaging Gateway returns an error while processing the message.

        Returns:
            str: Received response message
        """
    request_json_obj = json.loads(request_json)
    response_json = await message_processor(request_json_obj, CANCEL_OPERATION, TICKET_TYPE_CROSSCONNECT, None, oauth_token, True)
    return response_json

async def get_notifications(requestor_id, servicer_id, activity_id, ticket_state):
    """Receive ticket notification from Equinix Messaging Gateway that matches the provided filter criteria.

        Args:
            requestor_id (str): Customer Reference Number of the Crossconnect ticket.
            servicer_id (str): Ticket Number of the CrossConnect ticket.
            activity_id (str): Activity Number of the CrossConnect ticket.
            ticket_state (str): State of the CrossConnect ticket (ex: Open, InProgress, Pending Customer Input, Cancelled, Closed). 

        Raises:
            obj: returns an error if Equinix Messaging Gateway returns an error while retrieving notification.

        Returns:
            str: Received notification message
        """
    all_filters = {"ResourceType": TICKET_TYPE_CROSSCONNECT}
    if requestor_id:
        all_filters.update({"RequestorId": requestor_id})
    if servicer_id:
        all_filters.update({"ServicerId": servicer_id})
    if activity_id:
        all_filters.update({"Activity": activity_id})
    if ticket_state:
        all_filters.update({"State": ticket_state})
    notification_msg = await read_from_queue( None, all_filters)
    if 'Attachments' in notification_msg['Body'] and len(notification_msg['Body']['Attachments'])>0:
        newAttachments = await downloadAllAttachments(notification_msg['Body']['Attachments'])
        notification_msg['Body']['Attachments'] = newAttachments

    return notification_msg
