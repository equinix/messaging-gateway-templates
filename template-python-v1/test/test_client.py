# EQUINIX MESSAGING GATEWAY TEST CLIENT 

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
import json

import pytest

import equinix_smarthands_template
import equinix_troubleticket_template
import equinix_workvisit_template

ORDER_NUMBER = "<ORDERNUMER>"

CLIENTID = "<CLIENTID>" # Will be supplied by Customer
CLIENTSECRET = "<CLIENTSECRET>" # Will be supplied by Customer

CREATE_WORKVISIT_PAYLOAD = {
    "ibxLocation": {
        "cages": [
            {
                "cage": "<CAGE>",
                "accountNumber":"1"

            }
        ],
        "ibx": "<IBX>"
    },
    "attachments": [],
    "customerReferenceNumber": "<CUSTOMER REFERENCE NUMBER>",
    "serviceDetails": {
        "schedule": {
            "startDateTime": "2020-10-25T07:05:00.000Z",
            "endDateTime": "2020-10-28T10:00:00Z"
        },
        "openCabinet": True,
        "additionalDetails": "Test description for WorkVisit",
        "visitors": [
            {
                "firstName": "Test FirstName",
                "lastName": "Test LastName",
                "company": "Test Company"
            }
        ]
    },
    "contacts": [
        {
            "contactType": "ORDERING",
            "userName": "<USER NAME>"
        },
        {
            "contactType": "TECHNICAL",
            "userName": "<USER NAME>",
            "workPhonePrefToCall": "ANYTIME"
        },
        {
            "contactType": "NOTIFICATION",
            "userName": "<USER NAME>"
        }
    ]
}

UPDATE_WORKVISIT_PAYLOAD = {
    "attachments": [],
    "orderNumber": ORDER_NUMBER,
    "serviceDetails": {
        "startDateTime": "2020-11-25T07:05:00.000Z",
        "endDateTime": "2020-11-27T10:00:00Z",
        "openCabinet": False,
        "additionalDetails": "Test Update APAC region WorkVisit",
        "visitors": [
            {
                "firstName": "Test FirstName New",
                "lastName": "Test LastName New",
                "company": "Test Company New"
            }
        ]
    }
}

CANCEL_WORKVISIT_PAYLOAD = {
    "orderNumber": ORDER_NUMBER,
    "cancellationReason": "Test Cancellation"
}

CREATE_SMARTHAND_PAYLOAD = {
    "CustomerContact": "<CUSTOMER CONTACT>",
    "Attachments": [],
    "RequestorId": "<REQUESTOR ID>",
    "RequestorIdUnique": False,
    "Operation": "0000",
    "Location": "<LOCATION>",
    "Description": "Test description for SmartHands Create",
    "SchedulingDetails": {
        "RequestedStartDate": None,
        "RequestedCompletionDate": None
    }
}

UPDATE_SMARTHAND_PAYLOAD = {
    "ServicerId": ORDER_NUMBER,
    "Attachments":[],
    "Description": "Test description for SmartHands Update 2 Way",
}
CANCEL_SMARTHAND_PAYLOAD = {
    "State": "Cancelled",
    "ServicerId": ORDER_NUMBER,
    "Description": "Test description for SmartHands Cancel",
}

CREATE_TROUBLETICKET_PAYLOAD = {
    "RequestorId": "<REQUESTOR ID>",
    "IncidentDate": "2020-09-11T00:00:00+00:00",
    "Description": "Test description for TroubleTicket Create",
    "Attachments": [],
    "RequestorIdUnique": False,
    "Operation": "0005/0001",
    "Location": "<LOCATION>",
    "CallFromCage": True,
    "CustomerContact": "<CUSTOMER CONTACT>",
    "Device": "<DEVICE>"
}

UPDATE_TROUBLETICKET_PAYLOAD = {
    "RequestorId": "<REQUESTOR ID>",
    "Description": "Test description for TroubleTicket Update",
    "Attachments": [],
    "ServicerId": ORDER_NUMBER,
    "CallFromCage": False,
}

CANCEL_TROUBLETICKET_PAYLOAD = {
    "Description": "Test description for TroubleTicket Cancel",
    "ServicerId": ORDER_NUMBER,
    "State": "Cancelled"
}


NOTIFICATION_PENDING_CUSTOMER_INPUT = "Pending Customer Input"
NOTIFICATION_OPEN = "Open"
NOTIFICATION_INPROGRESS = "InProgress"
NOTIFICATION_CANCELLED = "Cancelled"


@pytest.mark.asyncio
async def test_create_work_visit():
    print ("\n\nSending Create WorkVisit Request Message  **********\n\n")
    result = await equinix_workvisit_template.create_workvisit(json.dumps(CREATE_WORKVISIT_PAYLOAD), CLIENTID, CLIENTSECRET)
    if result:
        print ("\n\nReceiving Create WorkVisit Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["statusCode"] == 201, "Should pass test with status code as 201"

@pytest.mark.asyncio
async def test_update_work_visit():
    print ("\n\nSending Update WorkVisit Request Message  **********\n\n")
    result = await equinix_workvisit_template.update_work_visit(json.dumps(UPDATE_WORKVISIT_PAYLOAD), CLIENTID, CLIENTSECRET)
    if result:
        print ("\n\nReceiving Update WorkVisit Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["errors"][0]['code'] == 406, "expect 406 error"
        assert "In view of the evolving COVID-19 pandemic" in result["errors"][0]['message'], "Test fail"

@pytest.mark.asyncio
async def test_cancel_work_visit():
    print ("\n\nSending Cancel WorkVisit Request Message  **********\n\n")
    result = await equinix_workvisit_template.cancel_work_visit(json.dumps(CANCEL_WORKVISIT_PAYLOAD), CLIENTID, CLIENTSECRET)
    if result:
        print ("\n\nReceiving Cancel WorkVisit Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["statusCode"] == 202, "Should pass test with status code as 202"

@pytest.mark.asyncio
async def test_workvisit_notifications():   
    print ("\n\nSending WorkVisit Notification Request Message  **********\n\n")
    result = await equinix_workvisit_template.get_notifications(None, ORDER_NUMBER, None, NOTIFICATION_OPEN)
    if result:
        print("\n\nReceiving WorkVisit Notification Response Message  **********\n\n", result)


@pytest.mark.asyncio
async def test_create_smarthands():
    print ("\n\nSending Create SmartHands Request Message  **********\n\n")
    result = await equinix_smarthands_template.create_smarthands(json.dumps(CREATE_SMARTHAND_PAYLOAD), CLIENTID, CLIENTSECRET)
    if result:
        print ("\n\nReceiving Create SmartHands Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["statusCode"] == 201, "Should pass test with status code as 201"

@pytest.mark.asyncio
async def test_update_smarthands():
    print ("\n\nSending Update SmartHands Request Message  **********\n\n")
    result = await equinix_smarthands_template.update_smarthands(json.dumps(UPDATE_SMARTHAND_PAYLOAD), CLIENTID, CLIENTSECRET)
    if result:
        print ("\n\nReceiving Update SmartHands Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["statusCode"] == 202, "Should pass test with status code as 202"

@pytest.mark.asyncio
async def test_cancel_smarthands():
    print ("\n\nSending Cancel SmartHands Request Message  **********\n\n")
    result = await equinix_smarthands_template.cancel_smarthands(json.dumps(CANCEL_SMARTHAND_PAYLOAD), CLIENTID, CLIENTSECRET)
    if result:
        print ("\n\nReceiving Cancel SmartHands Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["statusCode"] == 202, "Should pass test with status code as 202"

@pytest.mark.asyncio
async def test_smarthands_notifications():   
    print ("\n\nSending SmartHands Notification Request Message  **********\n\n")
    result = await equinix_smarthands_template.get_notifications(None, ORDER_NUMBER, None, NOTIFICATION_OPEN)
    if result:
        print("\n\nReceiving SmartHands Notification Response Message  **********\n\n", result)


@pytest.mark.asyncio
async def test_create_troubleticket():
    print ("\n\nSending Create TroubleTicket Request Message  **********\n\n")
    result = await equinix_troubleticket_template.create_troubleticket(json.dumps(CREATE_TROUBLETICKET_PAYLOAD), CLIENTID, CLIENTSECRET)
    if result:
        print ("\n\nReceiving Create TroubleTicket Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["statusCode"] == 201, "Should pass test with status code as 201"

@pytest.mark.asyncio
async def test_update_troubleticket():
    print ("\n\nSending Update TroubleTicket Request Message  **********\n\n")
    result = await equinix_troubleticket_template.update_troubleticket(json.dumps(UPDATE_TROUBLETICKET_PAYLOAD), CLIENTID, CLIENTSECRET)
    if result:
        print ("\n\nReceiving Update TroubleTicket Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["statusCode"] == 202, "Should pass test with status code as 202"

@pytest.mark.asyncio
async def test_cancel_troubleticket():
    print ("\n\nSending Cancel TroubleTicket Request Message  **********\n\n")
    result = await equinix_troubleticket_template.cancel_troubleticket(json.dumps(CANCEL_TROUBLETICKET_PAYLOAD), CLIENTID, CLIENTSECRET)
    if result:
        print ("\n\nReceiving Cancel TroubleTicket Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["statusCode"] == 202, "Should pass test with status code as 202"

@pytest.mark.asyncio
async def test_troubleticket_notifications():   
    print ("\n\nSending TroubleTicket Notification Request Message  **********\n\n")
    result = await equinix_troubleticket_template.get_notifications(None, ORDER_NUMBER, None, NOTIFICATION_OPEN)
    if result:
        print("\n\nReceiving TroubleTicket Notification Response Message  **********\n\n", result)
