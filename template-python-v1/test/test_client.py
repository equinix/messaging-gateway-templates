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
import base64
import equinix_shipment_template
import equinix_smarthands_template
import equinix_troubleticket_template
import equinix_workvisit_template
import equinix_crossconnect_template
from util.message_util import (encodeFileToBase64)


ORDER_NUMBER = "<ORDERNUMBER>"

CLIENT_ID = "<CLIENTID>" # Will be supplied by Customer
CLIENT_SECRET = "<CLIENTSECRET>" # Will be supplied by Customer
OAUTH_TOKEN = "<OAUTHTOKEN>" # Will be supplied by Customer

CREATE_WORKVISIT_PAYLOAD = {
    "CustomerContact": "<CUSTOMER CONTACT>",
    "RequestorId": "<REQUESTOR ID>",
    "RequestorIdUnique": False,
    "Location": "<LOCATION>",
    "Attachments": [],
    "Description": "Test description for WorkVisit Create",
    "ServiceDetails": {
        "StartDateTime": "2020-09-20T07:05:00.000Z",
        "EndDateTime": "2020-09-21T10:00:00Z",
        "OpenCabinet": True,
        "Visitors": [
            {
                "FirstName": "Test FirstName",
                "LastName": "Test LastName",
                "CompanyName": "Test Company"
            }
        ]
    }
}

UPDATE_WORKVISIT_PAYLOAD = {
    "ServicerId": ORDER_NUMBER,
    "Attachments": [],
    "Description": "Test description for WorkVisit Update",
    "ServiceDetails": {
        "StartDateTime": "2020-09-25T07:05:00.000Z",
        "EndDateTime": "2020-09-26T10:00:00Z",
        "OpenCabinet": False,
        "Visitors": [
            {
                "FirstName": "Test FirstName",
                "LastName": "Test LastName",
                "CompanyName": "Test Company"
            }
        ]
    }
}

CANCEL_WORKVISIT_PAYLOAD = {
    "State": "Cancelled",
    "ServicerId": ORDER_NUMBER,
    "Description": "Test description for WorkVisit Cancel",
}


CREATE_WORKVISIT_PAYLOAD_AS_PER_API_SCHEMA = {
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

UPDATE_WORKVISIT_PAYLOAD_AS_PER_API_SCHEMA = {
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

CANCEL_WORKVISIT_PAYLOAD_AS_PER_API_SCHEMA = {
    "orderNumber": ORDER_NUMBER,
    "cancellationReason": "Test Cancellation"
}

CREATE_SMARTHAND_PAYLOAD = {
    "CustomerContact": "<CUSTOMER CONTACT>",
    "Attachments": [{"Name":"equinix_logo.png","Data": encodeFileToBase64("test/equinix_logo.png").decode("utf-8")}],
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
    "Description": "Test description for SmartHands Update",
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

CREATE_INBOUNDSHIPMENT_CARRIERTYPE_PAYLOAD = {
    "RequestorId": "<REQUESTOR ID>",
    "RequestorIdUnique": False,
    "CustomerContact": "<CUSTOMER_CONTACT>",
    "Operation": "0000/0000",
    "Location": "<LOCATION>",
    "Description": "Test description for Inbound Shipment Create",
    "Attachments": [],
    "CarrierName": "TEST",
    "ShipmentDateTime": "2020-09-20T07:05:00.000Z",
    "ShipmentIdentifier": "TRACK123456",
    "ServiceDetails": {
      "NoOfBoxes": 99,
      "DeliverToCage": False
    }
}

CREATE_INBOUNDSHIPMENT_CUSTOMERCARRYTYPE_PAYLOAD = {
    "RequestorId": "<REQUESTOR ID>",
    "RequestorIdUnique": False,
    "CustomerContact": "<CUSTOMER_CONTACT>",
    "Operation": "0000/0001",
    "Location": "<LOCATION>",
    "Description": "Test description for Inbound Shipment Create",
    "Attachments": [],
    "CarrierName": "TEST",
    "ShipmentDateTime": "2020-09-20T04:05:00.000Z",
    "ServiceDetails": {
      "NoOfBoxes": 99,
      "DeliverToCage": False
    }
}

CREATE_OUTBOUNDSHIPMENT_CARRIERTYPE_PAYLOAD = {
    "RequestorId": "<REQUESTOR ID>",
    "RequestorIdUnique": False,
    "Operation": "0001/0000",
    "Location": "<LOCATION>",
    "CustomerContact": "<CUSTOMER_CONTACT>",
    "Description": "Test description for Outbound Shipment Create",
    "Attachments": [],
    "CarrierName": "TEST",
    "ShipmentIdentifier": "12345dse456546456",
    "ShipmentDateTime": "2020-09-20T10:05:00.000Z",
    "ShipmentLabel": [{ "Name": "atta1.jpeg", "Url": "https://eqixazurestorage.blob.core.windows.net/emg-download-blob/atta1.jpeg" }],
    "ShipmentLabelInsideBox": False,
    "ServiceDetails": {
          "NoOfBoxes": 3,
          "DeclaredValue": "3",
          "ShipmentDescription": "Test ShipmentDescription",
          "ShipToName": "test",
          "ShipToAddress": "1188 test address",
          "ShipToCity": "Sunnyvale",
          "ShipToCountry": "US",
          "ShipToState": "CALIFORNIA",
          "ShipToZipCode": "94085",
          "ShipToPhoneNumber": "+1 1331313",
          "ShipToCarrierAccountNumber": "111",
          "InsureShipment": False,
          "PickUpFromCageSuite": False,
        }
}

CREATE_OUTBOUNDSHIPMENT_CUSTOMERCARRYTYPE_PAYLOAD = {
    "RequestorId": "<REQUESTOR ID>",
    "RequestorIdUnique": False,
    "Operation": "0001/0001",
    "Location": "<LOCATION>",
    "CustomerContact": "<CUSTOMER_CONTACT>",
    "Description": "Test description for Outbound Shipment Create",
    "Attachments": [],
    "ShipmentDateTime": "2020-09-20T07:05:00.000Z",
    "ShipmentLabelInsideBox": False
}

UPDATE_INBOUNDSHIPMENT_PAYLOAD = {
    "RequestorId": "<REQUESTOR ID>",
    "ServicerId": ORDER_NUMBER,
    "Description": "Test description for Inbound Shipment Update",
    "Attachments": [],
    "CarrierName": "OTHER",
    "ServiceDetails": {
        "NoOfBoxes": 999,
        "DeliverToCage": True
    }
}

UPDATE_OUTBOUNDSHIPMENT_PAYLOAD = {
    "RequestorId": "<REQUESTOR ID>",
    "ServicerId": ORDER_NUMBER,
    "Attachments": [],
    "Description": "Test description for Outbound Shipment Update",
    "ShipmentIdentifier": "12345dse456546456",
    "ShipmentDateTime": "2020-09-20T07:05:00.000Z",
    "CarrierName": "OTHER",
    "ShipmentLabelInsideBox": True,
    "ServiceDetails": {
      "NoOfBoxes": 3,
      "DeclaredValue": "3",
      "ShipmentDescription": "Test ShipmentDescription",
      "ShipToName": "test",
      "ShipToAddress": "1188 test address",
      "ShipToCity": "Sunnyvale",
      "ShipToCountry": "US",
      "ShipToState": "CALIFORNIA",
      "ShipToZipCode": "94085",
      "ShipToPhoneNumber": "+1 1331313",
      "ShipToCarrierAccountNumber": "111",
      "InsureShipment": False,
      "PickUpFromCageSuite": False,
    }
}

CANCEL_SHIPMENT_PAYLOAD = {
    "Description": "Test description for Shipment Cancel",
    "RequestorId": "<REQUESTOR ID>",
    "ServicerId": ORDER_NUMBER,
    "State": "Cancelled"
}

CREATE_CROSSCONNECT_PAYLOAD = {
    "CustomerContact": "<CUSTOMER_CONTACT>",
    "RequestorId": "<REQUESTOR ID>",
    "RequestorIdUnique": False,
    "Attachments": [],
    "Operation": "0000",
    "Description": "Test description for CrossConnect Create",
    "SchedulingDetails": {
        "RequestedCompletionDate": None
    },
    "AdditionalContacts": [
        {
            "ContactType": "TECHNICAL",
            "FirstName": "Test FirstName",
            "LastName": "Test LastName",
            "Email": "<test@test.com>",
            "WorkPhoneCountryCode": "+1",
            "WorkPhone": "866-205-4244",
            "WorkPhonePrefToCall": "ANYTIME",
            "WorkPhoneTimeZone": "Atlantic/Canary",
            "MobilePhoneCountryCode": "+1",
            "MobilePhone": "346-205-4244",
            "MobilePhonePrefToCall": "ANYTIME",
            "MobilePhoneTimeZone": "Atlantic/Canary"
        }
    ],
    "ConnectionDetails": [
        {
            "ASide": {
                "ConnectionService": "<Connection_Service>",
                "MediaType": "<MediaType>",
                "ProtocolType": "<ProtocolType>",
                "ConnectorType": "<ConnectorType>",
                "PatchPanel": {
                    "Id": "<PatchPanel_Id>",
                    "PortA": None,
                    "PortB": None
                }
            },
            "ZSide": {
                ## Existing Provider 
                "ConnectorType": "<ConnectorType>",
                "PatchPanel": {
                    "Id": "<PatchPanel_Id>",
                    "PortA": None,
                    "PortB": None
                },
                "CircuitId": "12345",
                ## New Provider 
                # "LOAAttachment": { "Name": "<LOAAttachment_Name>", "Url": "<LOAAttachment_Url>" },
                # "IBX": "<IBX>",
                # "ProviderName": "<Provider_Name>",
            },
            "ServiceDetails": None
        }
    ]
}

NOTIFICATION_PENDING_CUSTOMER_INPUT = "Pending Customer Input"
NOTIFICATION_OPEN = "Open"
NOTIFICATION_INPROGRESS = "InProgress"
NOTIFICATION_CANCELLED = "Cancelled"

@pytest.mark.asyncio
async def test_create_work_visit():
    print ("\n\nSending Create WorkVisit Request Message  **********\n\n")
    result = await equinix_workvisit_template.create_workvisit(json.dumps(CREATE_WORKVISIT_PAYLOAD), CLIENT_ID, CLIENT_SECRET)
    if result:
        print ("\n\nReceiving Create WorkVisit Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 201, "Should pass test with status code as 201"

@pytest.mark.asyncio
async def test_create_work_visit_using_oauth():
    print ("\n\nSending Create WorkVisit Request Message  **********\n\n")
    result = await equinix_workvisit_template.create_workvisit_oauth(json.dumps(CREATE_WORKVISIT_PAYLOAD), OAUTH_TOKEN)
    if result:
        print ("\n\nReceiving Create WorkVisit Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 201, "Should pass test with status code as 201"

@pytest.mark.asyncio
async def test_update_work_visit():
    print ("\n\nSending Update WorkVisit Request Message  **********\n\n")
    result = await equinix_workvisit_template.update_work_visit(json.dumps(UPDATE_WORKVISIT_PAYLOAD), CLIENT_ID, CLIENT_SECRET)
    if result:
        print ("\n\nReceiving Update WorkVisit Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 406, "expect 406 error"
        assert "In view of the evolving COVID-19 pandemic" in result["Body"]["Description"], "Test fail"

@pytest.mark.asyncio
async def test_update_work_visit_using_oauth():
    print ("\n\nSending Update WorkVisit Request Message  **********\n\n")
    result = await equinix_workvisit_template.update_work_visit_oauth(json.dumps(UPDATE_WORKVISIT_PAYLOAD), OAUTH_TOKEN)
    if result:
        print ("\n\nReceiving Update WorkVisit Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 406, "expect 406 error"
        assert "In view of the evolving COVID-19 pandemic" in result["Body"]["Description"], "Test fail"

@pytest.mark.asyncio
async def test_cancel_work_visit():
    print ("\n\nSending Cancel WorkVisit Request Message  **********\n\n")
    result = await equinix_workvisit_template.cancel_work_visit(json.dumps(CANCEL_WORKVISIT_PAYLOAD), CLIENT_ID, CLIENT_SECRET)
    if result:
        print ("\n\nReceiving Cancel WorkVisit Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 202, "Should pass test with status code as 202"

@pytest.mark.asyncio
async def test_cancel_work_visit_using_oauth():
    print ("\n\nSending Cancel WorkVisit Request Message  **********\n\n")
    result = await equinix_workvisit_template.cancel_work_visit_oauth(json.dumps(CANCEL_WORKVISIT_PAYLOAD), OAUTH_TOKEN)
    if result:
        print ("\n\nReceiving Cancel WorkVisit Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 202, "Should pass test with status code as 202"


@pytest.mark.asyncio
async def test_create_work_visit_extension():
    print ("\n\nSending Create WorkVisit Request Message as per API Schema  **********\n\n")
    result = await equinix_workvisit_template.create_workvisit_extn(json.dumps(CREATE_WORKVISIT_PAYLOAD_AS_PER_API_SCHEMA), CLIENT_ID, CLIENT_SECRET)
    if result:
        print ("\n\nReceiving Create WorkVisit Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["statusCode"] == 201, "Should pass test with status code as 201"

@pytest.mark.asyncio
async def test_create_work_visit_extension_using_oauth():
    print ("\n\nSending Create WorkVisit Request Message as per API Schema  **********\n\n")
    result = await equinix_workvisit_template.create_workvisit_extn_oauth(json.dumps(CREATE_WORKVISIT_PAYLOAD_AS_PER_API_SCHEMA), OAUTH_TOKEN)
    if result:
        print ("\n\nReceiving Create WorkVisit Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["statusCode"] == 201, "Should pass test with status code as 201"

@pytest.mark.asyncio
async def test_update_work_visit_extension():
    print ("\n\nSending Update WorkVisit Request Message as per API Schema **********\n\n")
    result = await equinix_workvisit_template.update_work_visit_extn(json.dumps(UPDATE_WORKVISIT_PAYLOAD_AS_PER_API_SCHEMA), CLIENT_ID, CLIENT_SECRET)
    if result:
        print ("\n\nReceiving Update WorkVisit Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["errors"][0]['code'] == 406, "expect 406 error"
        assert "In view of the evolving COVID-19 pandemic" in result["errors"][0]['message'], "Test fail"

@pytest.mark.asyncio
async def test_update_work_visit_extension_using_oauth():
    print ("\n\nSending Update WorkVisit Request Message as per API Schema **********\n\n")
    result = await equinix_workvisit_template.update_work_visit_extn_oauth(json.dumps(UPDATE_WORKVISIT_PAYLOAD_AS_PER_API_SCHEMA), OAUTH_TOKEN)
    if result:
        print ("\n\nReceiving Update WorkVisit Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["errors"][0]['code'] == 406, "expect 406 error"
        assert "In view of the evolving COVID-19 pandemic" in result["errors"][0]['message'], "Test fail"

@pytest.mark.asyncio
async def test_cancel_work_visit_extension():
    print ("\n\nSending Cancel WorkVisit Request Message as per API Schema **********\n\n")
    result = await equinix_workvisit_template.cancel_work_visit_extn(json.dumps(CANCEL_WORKVISIT_PAYLOAD_AS_PER_API_SCHEMA), CLIENT_ID, CLIENT_SECRET)
    if result:
        print ("\n\nReceiving Cancel WorkVisit Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["statusCode"] == 202, "Should pass test with status code as 202"

@pytest.mark.asyncio
async def test_cancel_work_visit_extension_using_oauth():
    print ("\n\nSending Cancel WorkVisit Request Message as per API Schema **********\n\n")
    result = await equinix_workvisit_template.cancel_work_visit_extn_oauth(json.dumps(CANCEL_WORKVISIT_PAYLOAD_AS_PER_API_SCHEMA), OAUTH_TOKEN)
    if result:
        print ("\n\nReceiving Cancel WorkVisit Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["statusCode"] == 202, "Should pass test with status code as 202"

@pytest.mark.asyncio
async def test_get_notifications_for_work_visit():   
    print ("\n\nSending WorkVisit Notification Request Message  **********\n\n")
    # (customerReferenceNumber, orderNumber, activityID, state - Open, InProgress, Cancelled, Closed)
    result = await equinix_workvisit_template.get_notifications(None, ORDER_NUMBER, None, None)
    if result:
        print("\n\nReceiving WorkVisit Notification Response Message  **********\n\n", result)


@pytest.mark.asyncio
async def test_create_smarthands():
    print ("\n\nSending Create SmartHands Request Message  **********\n\n")
    result = await equinix_smarthands_template.create_smarthands(json.dumps(CREATE_SMARTHAND_PAYLOAD), CLIENT_ID, CLIENT_SECRET)
    if result:
        print ("\n\nReceiving Create SmartHands Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 201, "Should pass test with status code as 201"

@pytest.mark.asyncio
async def test_create_smarthands_using_oauth():
    print ("\n\nSending Create SmartHands Request Message  **********\n\n")
    result = await equinix_smarthands_template.create_smarthands_oauth(json.dumps(CREATE_SMARTHAND_PAYLOAD), OAUTH_TOKEN)
    if result:
        print ("\n\nReceiving Create SmartHands Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 201, "Should pass test with status code as 201"

@pytest.mark.asyncio
async def test_update_smarthands():
    print ("\n\nSending Update SmartHands Request Message  **********\n\n")
    result = await equinix_smarthands_template.update_smarthands(json.dumps(UPDATE_SMARTHAND_PAYLOAD), CLIENT_ID, CLIENT_SECRET)
    if result:
        print ("\n\nReceiving Update SmartHands Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 202, "Should pass test with status code as 202"

@pytest.mark.asyncio
async def test_update_smarthands_using_oauth():
    print ("\n\nSending Update SmartHands Request Message  **********\n\n")
    result = await equinix_smarthands_template.update_smarthands_oauth(json.dumps(UPDATE_SMARTHAND_PAYLOAD), OAUTH_TOKEN)
    if result:
        print ("\n\nReceiving Update SmartHands Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 202, "Should pass test with status code as 202"

@pytest.mark.asyncio
async def test_cancel_smarthands():
    print ("\n\nSending Cancel SmartHands Request Message  **********\n\n")
    result = await equinix_smarthands_template.cancel_smarthands(json.dumps(CANCEL_SMARTHAND_PAYLOAD), CLIENT_ID, CLIENT_SECRET)
    if result:
        print ("\n\nReceiving Cancel SmartHands Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 202, "Should pass test with status code as 202"

@pytest.mark.asyncio
async def test_cancel_smarthands_using_oauth():
    print ("\n\nSending Cancel SmartHands Request Message  **********\n\n")
    result = await equinix_smarthands_template.cancel_smarthands_oauth(json.dumps(CANCEL_SMARTHAND_PAYLOAD), OAUTH_TOKEN)
    if result:
        print ("\n\nReceiving Cancel SmartHands Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 202, "Should pass test with status code as 202"

@pytest.mark.asyncio
async def test_get_notifications_for_smarthands():   
    print ("\n\nSending SmartHands Notification Request Message  **********\n\n")
    # (customerReferenceNumber, orderNumber, activityID, state - Open, InProgress, Cancelled, Closed)
    result = await equinix_smarthands_template.get_notifications(None, ORDER_NUMBER, None, None)
    if result:
        print("\n\nReceiving SmartHands Notification Response Message  **********\n\n", result)

@pytest.mark.asyncio
async def test_create_troubleticket():
    print ("\n\nSending Create TroubleTicket Request Message  **********\n\n")
    result = await equinix_troubleticket_template.create_troubleticket(json.dumps(CREATE_TROUBLETICKET_PAYLOAD), CLIENT_ID, CLIENT_SECRET)
    if result:
        print ("\n\nReceiving Create TroubleTicket Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 201, "Should pass test with status code as 201"

@pytest.mark.asyncio
async def test_create_troubleticket_using_oauth():
    print ("\n\nSending Create TroubleTicket Request Message  **********\n\n")
    result = await equinix_troubleticket_template.create_troubleticket_oauth(json.dumps(CREATE_TROUBLETICKET_PAYLOAD), OAUTH_TOKEN)
    if result:
        print ("\n\nReceiving Create TroubleTicket Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 201, "Should pass test with status code as 201"

@pytest.mark.asyncio
async def test_update_troubleticket():
    print ("\n\nSending Update TroubleTicket Request Message  **********\n\n")
    result = await equinix_troubleticket_template.update_troubleticket(json.dumps(UPDATE_TROUBLETICKET_PAYLOAD), CLIENT_ID, CLIENT_SECRET)
    if result:
        print ("\n\nReceiving Update TroubleTicket Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 202, "Should pass test with status code as 202"

@pytest.mark.asyncio
async def test_update_troubleticket_using_oauth():
    print ("\n\nSending Update TroubleTicket Request Message  **********\n\n")
    result = await equinix_troubleticket_template.update_troubleticket_oauth(json.dumps(UPDATE_TROUBLETICKET_PAYLOAD), OAUTH_TOKEN)
    if result:
        print ("\n\nReceiving Update TroubleTicket Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 202, "Should pass test with status code as 202"

@pytest.mark.asyncio
async def test_cancel_troubleticket():
    print ("\n\nSending Cancel TroubleTicket Request Message  **********\n\n")
    result = await equinix_troubleticket_template.cancel_troubleticket(json.dumps(CANCEL_TROUBLETICKET_PAYLOAD), CLIENT_ID, CLIENT_SECRET)
    if result:
        print ("\n\nReceiving Cancel TroubleTicket Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 202, "Should pass test with status code as 202"

@pytest.mark.asyncio
async def test_cancel_troubleticket_using_oauth():
    print ("\n\nSending Cancel TroubleTicket Request Message  **********\n\n")
    result = await equinix_troubleticket_template.cancel_troubleticket_oauth(json.dumps(CANCEL_TROUBLETICKET_PAYLOAD), OAUTH_TOKEN)
    if result:
        print ("\n\nReceiving Cancel TroubleTicket Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 202, "Should pass test with status code as 202"

@pytest.mark.asyncio
async def test_get_notifications_for_troubleticket():   
    print ("\n\nSending TroubleTicket Notification Request Message  **********\n\n")
    # (customerReferenceNumber, orderNumber, activityID, state - Open, InProgress, Cancelled, Closed)
    result = await equinix_troubleticket_template.get_notifications(None, ORDER_NUMBER, None, None)
    if result:
        print("\n\nReceiving TroubleTicket Notification Response Message  **********\n\n", result)


@pytest.mark.asyncio
async def test_create_inbound_shipment_carriertype():
    print ("\n\nSending Create inbound shipment carrier type Request Message  **********\n\n")
    result = await equinix_shipment_template.create_shipment(json.dumps(CREATE_INBOUNDSHIPMENT_CARRIERTYPE_PAYLOAD), CLIENT_ID, CLIENT_SECRET)
    if result:
        print ("\n\nReceiving Create Shipment Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 201, "Should pass test with status code as 201"

@pytest.mark.asyncio
async def test_create_inbound_shipment_carriertype_using_oauth():
    print ("\n\nSending Create inbound shipment carrier type Request Message  **********\n\n")
    result = await equinix_shipment_template.create_shipment_oauth(json.dumps(CREATE_INBOUNDSHIPMENT_CARRIERTYPE_PAYLOAD), OAUTH_TOKEN)
    if result:
        print ("\n\nReceiving Create Shipment Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 201, "Should pass test with status code as 201"

@pytest.mark.asyncio
async def test_create_inbound_shipment_customercarrytype():
    print ("\n\nSending Create inbound shipment customer carry type Request Message  **********\n\n")
    result = await equinix_shipment_template.create_shipment(json.dumps(CREATE_INBOUNDSHIPMENT_CUSTOMERCARRYTYPE_PAYLOAD), CLIENT_ID, CLIENT_SECRET)
    if result:
        print ("\n\nReceiving Create Shipment Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 201, "Should pass test with status code as 201"

@pytest.mark.asyncio
async def test_create_inbound_shipment_customercarrytype_using_oauth():
    print ("\n\nSending Create inbound shipment customer carry type Request Message  **********\n\n")
    result = await equinix_shipment_template.create_shipment_oauth(json.dumps(CREATE_INBOUNDSHIPMENT_CUSTOMERCARRYTYPE_PAYLOAD), OAUTH_TOKEN)
    if result:
        print ("\n\nReceiving Create Shipment Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 201, "Should pass test with status code as 201"

@pytest.mark.asyncio
async def test_create_outbound_shipment_carriertype():
    print ("\n\nSending Create outbound shipment carrier type Request Message  **********\n\n")
    result = await equinix_shipment_template.create_shipment(json.dumps(CREATE_OUTBOUNDSHIPMENT_CARRIERTYPE_PAYLOAD), CLIENT_ID, CLIENT_SECRET)
    if result:
        print ("\n\nReceiving Create Shipment Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 201, "Should pass test with status code as 201"

@pytest.mark.asyncio
async def test_create_outbound_shipment_carriertype_using_oauth():
    print ("\n\nSending Create outbound shipment carrier type Request Message  **********\n\n")
    result = await equinix_shipment_template.create_shipment_oauth(json.dumps(CREATE_OUTBOUNDSHIPMENT_CARRIERTYPE_PAYLOAD), OAUTH_TOKEN)
    if result:
        print ("\n\nReceiving Create Shipment Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 201, "Should pass test with status code as 201"

@pytest.mark.asyncio
async def test_create_outbound_shipment_customercarrytype():
    print ("\n\nSending Create outbound shipment customer carry type Request Message  **********\n\n")
    result = await equinix_shipment_template.create_shipment(json.dumps(CREATE_OUTBOUNDSHIPMENT_CUSTOMERCARRYTYPE_PAYLOAD), CLIENT_ID, CLIENT_SECRET)
    if result:
        print ("\n\nReceiving Create Shipment Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 201, "Should pass test with status code as 201"

@pytest.mark.asyncio
async def test_create_outbound_shipment_customercarrytype_using_oauth():
    print ("\n\nSending Create outbound shipment customer carry type Request Message  **********\n\n")
    result = await equinix_shipment_template.create_shipment_oauth(json.dumps(CREATE_OUTBOUNDSHIPMENT_CUSTOMERCARRYTYPE_PAYLOAD), OAUTH_TOKEN)
    if result:
        print ("\n\nReceiving Create Shipment Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 201, "Should pass test with status code as 201"

@pytest.mark.asyncio
async def test_update_inbound_shipment():
    print ("\n\nSending Update inbound shipment Request Message  **********\n\n")
    result = await equinix_shipment_template.update_shipment(json.dumps(UPDATE_INBOUNDSHIPMENT_PAYLOAD), CLIENT_ID, CLIENT_SECRET)
    if result:
        print ("\n\nReceiving Update Shipment Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 202, "Should pass test with status code as 202"

@pytest.mark.asyncio
async def test_update_inbound_shipment_using_oauth():
    print ("\n\nSending Update inbound shipment Request Message  **********\n\n")
    result = await equinix_shipment_template.update_shipment_oauth(json.dumps(UPDATE_INBOUNDSHIPMENT_PAYLOAD), OAUTH_TOKEN)
    if result:
        print ("\n\nReceiving Update Shipment Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 202, "Should pass test with status code as 202"

@pytest.mark.asyncio
async def test_update_outbound_shipment():
    print ("\n\nSending Update outbound shipment Request Message  **********\n\n")
    result = await equinix_shipment_template.update_shipment(json.dumps(UPDATE_OUTBOUNDSHIPMENT_PAYLOAD), CLIENT_ID, CLIENT_SECRET)
    if result:
        print ("\n\nReceiving Update Shipment Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 202, "Should pass test with status code as 202"

@pytest.mark.asyncio
async def test_update_outbound_shipment_using_oauth():
    print ("\n\nSending Update outbound shipment Request Message  **********\n\n")
    result = await equinix_shipment_template.update_shipment_oauth(json.dumps(UPDATE_OUTBOUNDSHIPMENT_PAYLOAD), OAUTH_TOKEN)
    if result:
        print ("\n\nReceiving Update Shipment Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 202, "Should pass test with status code as 202"

@pytest.mark.asyncio
async def test_cancel_shipment():
    print ("\n\nSending Cancel Shipment Request Message  **********\n\n")
    result = await equinix_shipment_template.cancel_shipment(json.dumps(CANCEL_SHIPMENT_PAYLOAD), CLIENT_ID, CLIENT_SECRET)
    if result:
        print ("\n\nReceiving Cancel Shipment Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 202, "Should pass test with status code as 202"

@pytest.mark.asyncio
async def test_cancel_shipment_using_oauth():
    print ("\n\nSending Cancel Shipment Request Message  **********\n\n")
    result = await equinix_shipment_template.cancel_shipment_oauth(json.dumps(CANCEL_SHIPMENT_PAYLOAD), OAUTH_TOKEN)
    if result:
        print ("\n\nReceiving Cancel Shipment Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 202, "Should pass test with status code as 202"

@pytest.mark.asyncio
async def test_get_notifications_for_shipment():   
    print ("\n\nSending Shipment Notification Request Message  **********\n\n")
    # (customerReferenceNumber, orderNumber, activityID, state - Open, InProgress, Cancelled, Closed)
    result = await equinix_shipment_template.get_notifications(None, ORDER_NUMBER, None, None)
    if result:
        print("\n\nReceiving Shipment Notification Response Message  **********\n\n", result)

@pytest.mark.asyncio
async def test_create_crossconnect():
    print ("\n\nSending Create CrossConnect Request Message  **********\n\n")
    result = await equinix_crossconnect_template.create_crossconnect(json.dumps(CREATE_CROSSCONNECT_PAYLOAD), CLIENT_ID, CLIENT_SECRET)
    if result:
        print ("\n\nReceiving Create CrossConnect Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 201, "Should pass test with status code as 201"

@pytest.mark.asyncio
async def test_create_crossconnect_using_oauth():
    print ("\n\nSending Create CrossConnect Request Message  **********\n\n")
    result = await equinix_crossconnect_template.create_crossconnect_oauth(json.dumps(CREATE_CROSSCONNECT_PAYLOAD), OAUTH_TOKEN)
    if result:
        print ("\n\nReceiving Create CrossConnect Response Message  **********\n\n {0}".format(result))
        assert result, "Test Fail"
        assert result["Body"]["StatusCode"] == 201, "Should pass test with status code as 201"

@pytest.mark.asyncio
async def test_get_notifications_for_crossconnect():   
    print ("\n\nSending CrossConnect Notification Request Message  **********\n\n")
    # (customerReferenceNumber, orderNumber, activityID, state - Open, InProgress, Cancelled, Closed)
    result = await equinix_crossconnect_template.get_notifications(None, ORDER_NUMBER, None, NOTIFICATION_PENDING_CUSTOMER_INPUT)
    if result:
        print("\n\nReceiving CrossConnect Notification Response Message  **********\n\n", result) 
