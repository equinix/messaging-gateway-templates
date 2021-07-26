/** EQUINIX MESSAGING GATEWAY TEST CLIENT **/

'use strict'
const workVisitTemplate = require('../EquinixWorkVisitTemplate')
const smartHandsTemplate = require('../EquinixSmartHandsTemplate')
const troubleTicketTemplate = require('../EquinixTroubleTicketTemplate')
const shipmentTemplate = require('../EquinixShipmentTemplate')
const crossConnectTemplate = require('../EquinixCrossConnectTemplate')
const safeStringify = require('fast-safe-stringify');
const messageUtil = require('../util/MessageUtil');
const path = require('path');


var ORDER_NUMBER = "<ORDER_NUMBER>";
var CLIENT_ID = "<CLIENT_ID>"; // Will be supplied by Customer
var CLIENT_SECRET = "<CLIENT_SECRET>"; // Will be supplied by Customer

const NOTIFICATION_PENDING_CUSTOMER_INPUT = "Pending Customer Input";
const NOTIFICATION_OPEN = "Open";
const NOTIFICATION_INPROGRESS = "InProgress";
const NOTIFICATION_CANCELLED = "Cancelled";

const CREATE_WORKVISIT_PAYLOAD = {
    "CustomerContact": "<CUSTOMER_CONTACT>",
    "RequestorId": "102894102Test1234",
    "RequestorIdUnique": false,
    "Location": "<LOCATION>",
    "Attachments": [],
    "Description": "Test description for WorkVisit Create",
    "ServiceDetails": {
        "StartDateTime": "2020-09-20T07:05:00.000Z",
        "EndDateTime": "2020-09-21T10:00:00Z",
        "OpenCabinet": true,
        "Visitors": [
            {
                "FirstName": "Test FirstName",
                "LastName": "Test LastName",
                "CompanyName": "Test Company"
            }
        ]
    }
}

const UPDATE_WORKVISIT_PAYLOAD = {
    "ServicerId": ORDER_NUMBER,
    "Attachments": [],
    "Description": "Test description for WorkVisit Update",
    "ServiceDetails": {
        "StartDateTime": "2020-09-25T07:05:00.000Z",
        "EndDateTime": "2020-09-26T10:00:00Z",
        "OpenCabinet": false,
        "Visitors": [
            {
                "FirstName": "Test FirstName",
                "LastName": "Test LastName",
                "CompanyName": "Test Company"
            }
        ]
    }
}

const CANCEL_WORKVISIT_PAYLOAD = {
    "State": "Cancelled",
    "ServicerId": ORDER_NUMBER,
    "Description": "Test description for WorkVisit Cancel",
}

const CREATE_WORKVISIT_PAYLOAD_AS_PER_API_SCHEMA = {
    "ibxLocation": {
        "cages": [
            {
                "cage": "<LOCATION>",
                "accountNumber": "1"

            }
        ],
        "ibx": "<IBX>"
    },
    "attachments": [],
    "customerReferenceNumber": "102894102Test1234",
    "serviceDetails": {
        "schedule": {
            "startDateTime": "2020-09-20T07:05:00.000Z",
            "endDateTime": "2020-09-21T10:00:00Z"
        },
        "openCabinet": true,
        "additionalDetails": "Test description for WorkVisit Create",
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
            "userName": "<USER_NAME>"
        },
        {
            "contactType": "TECHNICAL",
            "userName": "<USER_NAME>",
            "workPhonePrefToCall": "ANYTIME"
        },
        {
            "contactType": "NOTIFICATION",
            "userName": "<USER_NAME>"
        }
    ]
}

const UPDATE_WORKVISIT_PAYLOAD_AS_PER_API_SCHEMA = {
    "attachments": [],
    "orderNumber": ORDER_NUMBER,
    "serviceDetails": {
        "startDateTime": "2020-09-25T07:05:00.000Z",
        "endDateTime": "2020-09-27T10:00:00Z",
        "openCabinet": false,
        "additionalDetails": "Test description for WorkVisit Update",
        "visitors": [
            {
                "firstName": "Test FirstName New",
                "lastName": "Test LastName New",
                "company": "Test Company New"
            }
        ]
    }
}

const CANCEL_WORKVISIT_PAYLOAD_AS_PER_API_SCHEMA = {
    "orderNumber": ORDER_NUMBER,
    "cancellationReason": "Test description for WorkVisit Cancel"
}



const CREATE_SMARTHAND_PAYLOAD = {
    "CustomerContact": "<CUSTOMER_CONTACT>",
    "Attachments": [
        { "Name": "equinix_logo.png", "Data": messageUtil.convertFileToBase64(path.resolve(__dirname, "equinix_logo.png")) },
        { "Name": "TestWordDoc.doc", "Data": messageUtil.convertFileToBase64(path.resolve(__dirname, "TestWordDoc.doc")) }
    ],
    "RequestorId": "102894102Test1234",
    "RequestorIdUnique": false,
    "Operation": "0000",
    "Location": "<LOCATION>",
    "Description": "Test description for SmartHands Create",
    "SchedulingDetails": {
        "RequestedStartDate": null,
        "RequestedCompletionDate": null
    }
}
const UPDATE_SMARTHAND_PAYLOAD = {
    "ServicerId": ORDER_NUMBER,
    "Attachments": [],
    "Description": "Test description for SmartHands Update",
}
const CANCEL_SMARTHAND_PAYLOAD = {
    "State": "Cancelled",
    "ServicerId": ORDER_NUMBER,
    "Description": "Test description for SmartHands Cancel",
}

const CREATE_TROUBLETICKET_PAYLOAD = {
    "RequestorId": "102894102Test1234",
    "IncidentDate": "2020-09-11T00:00:00+00:00",
    "Description": "Test description for TroubleTicket Create",
    "Attachments": [],
    "RequestorIdUnique": false,
    "Operation": "0005/0001",
    "Location": "<LOCATION>",
    "CallFromCage": true,
    "CustomerContact": "<CUSTOMER_CONTACT>",
    "Device": "<DEVICE>"
}

const UPDATE_TROUBLETICKET_PAYLOAD = {
    "RequestorId": "102894102Test1234",
    "Description": "Test description for TroubleTicket Update",
    "Attachments": [],
    "ServicerId": ORDER_NUMBER,
    "CallFromCage": false
}

const CANCEL_TROUBLETICKET_PAYLOAD = {
    "Description": "Test description for TroubleTicket Cancel",
    "ServicerId": ORDER_NUMBER,
    "State": "Cancelled"
}

const CREATE_INBOUNDSHIPMENT_CARRIERTYPE_PAYLOAD = {
    "RequestorId": "102894102Test1234",
    "RequestorIdUnique": false,
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
        "DeliverToCage": false
    }
}

const CREATE_INBOUNDSHIPMENT_CUSTOMERCARRYTYPE_PAYLOAD = {
    "RequestorId": "102894102Test1234",
    "RequestorIdUnique": false,
    "CustomerContact": "<CUSTOMER_CONTACT>",
    "Operation": "0000/0001",
    "Location": "<LOCATION>",
    "Description": "Test description for Inbound Shipment Create",
    "Attachments": [],
    "CarrierName": "TEST",
    "ShipmentDateTime": "2020-09-20T04:05:00.000Z",
    "ServiceDetails": {
        "NoOfBoxes": 99,
        "DeliverToCage": false
    }
}

const CREATE_OUTBOUNDSHIPMENT_CARRIERTYPE_PAYLOAD = {
    "RequestorId": "102894102Test1234",
    "RequestorIdUnique": false,
    "Operation": "0001/0000",
    "Location": "<LOCATION>",
    "CustomerContact": "<CUSTOMER_CONTACT>",
    "Description": "Test description for Outbound Shipment Create",
    "Attachments": [],
    "CarrierName": "TEST",
    "ShipmentIdentifier": "12345dse456546456",
    "ShipmentDateTime": "2020-09-20T10:05:00.000Z",
    "ShipmentLabel": [{ "Name": "atta1.jpeg", "Url": "https://eqixazurestorage.blob.core.windows.net/emg-download-blob/atta1.jpeg" }],
    "ShipmentLabelInsideBox": false,
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
        "InsureShipment": false,
        "PickUpFromCageSuite": false,
    }
}

const CREATE_OUTBOUNDSHIPMENT_CUSTOMERCARRYTYPE_PAYLOAD = {
    "RequestorId": "102894102Test1234",
    "RequestorIdUnique": false,
    "Operation": "0001/0001",
    "Location": "<LOCATION>",
    "CustomerContact": "<CUSTOMER_CONTACT>",
    "Description": "Test description for Outbound Shipment Create",
    "Attachments": [],
    "ShipmentDateTime": "2020-09-20T07:05:00.000Z",
    "ShipmentLabelInsideBox": false
}

const UPDATE_INBOUNDSHIPMENT_PAYLOAD = {
    "RequestorId": "102894102Test1234",
    "ServicerId": ORDER_NUMBER,
    "Description": "Test description for Inbound Shipment Update",
    "Attachments": [],
    "CarrierName": "OTHER",
    "ServiceDetails": {
        "NoOfBoxes": 999,
        "DeliverToCage": true
    }
}

const UPDATE_OUTBOUNDSHIPMENT_PAYLOAD = {
    "RequestorId": "102894102Test1234",
    "ServicerId": ORDER_NUMBER,
    "Attachments": [],
    "Description": "Test description for Outbound Shipment Update",
    "ShipmentIdentifier": "12345dse456546456",
    "ShipmentDateTime": "2020-09-20T07:05:00.000Z",
    "CarrierName": "OTHER",
    "ShipmentLabelInsideBox": true,
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
        "InsureShipment": false,
        "PickUpFromCageSuite": false,
    }
}

const CANCEL_SHIPMENT_PAYLOAD = {
    "Description": "Test description for Shipment Cancel",
    "RequestorId": "102894102Test1234",
    "ServicerId": ORDER_NUMBER,
    "State": "Cancelled"
}

const CREATE_CROSSCONNECT_PAYLOAD = {
    "CustomerContact": "<CUSTOMER_CONTACT>",
    "RequestorId": "102894102Test1234",
    "RequestorIdUnique": false,
    "Attachments": [],
    "Operation": "0000",
    "Description": "Test description for CrossConnect Create",
    "SchedulingDetails": {
        "RequestedCompletionDate": null
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
                "ConnectionService": "COAX",
                "MediaType": "COAX",
                "ProtocolType": "ANTENNA",
                "ConnectorType": "BNC",
                "PatchPanel": {
                    "Id": "<PATCH_PANEL_ID>",
                    "PortA": null,
                    "PortB": null
                }
            },
            "ZSide": {
                /** Existing Provider **/
                "ConnectorType": "BNC",
                "PatchPanel": {
                    "Id": "<PATCH_PANEL_ID>",
                    "PortA": null,
                    "PortB": null
                },
                "CircuitId": "12345",
                /** New Provider **/
                // "LOAAttachment": { "Name": "<LOAATTACHMENT_NAME>", "Url": "<>LOAATTACHMENT_URL" },
                // "IBX": "<IBX>",
                // "ProviderName": "New Telco. Corp.",
            },
            "ServiceDetails": null
        }
    ]
}

describe('EMG Template Test Suite', function () {
    this.timeout(10000000);
    it('test_create_work_visit', async function () {
        console.log("\n\nSending Create WorkVisit Request Message  **********\n\n")
        const result = await workVisitTemplate.createWorkVisit(
            JSON.stringify(CREATE_WORKVISIT_PAYLOAD),
            CLIENT_ID,
            CLIENT_SECRET
        );
        console.log("\n\nReceiving Create WorkVisit Response Message  **********\n\n", safeStringify(result))
    })

    it('test_update_work_visit', async function () {
        console.log("\n\nSending Update WorkVisit Request Message  **********\n\n")
        const result = await workVisitTemplate.updateWorkVisit(
            JSON.stringify(UPDATE_WORKVISIT_PAYLOAD),
            CLIENT_ID,
            CLIENT_SECRET
        )
        console.log("\n\nReceiving Update WorkVisit Response Message  **********\n\n", safeStringify(result))
    })

    it('test_cancel_work_visit', async function () {
        console.log("\n\nSending Cancel WorkVisit Request Message  **********\n\n")
        const result = await workVisitTemplate.cancelWorkVisit(
            JSON.stringify(CANCEL_WORKVISIT_PAYLOAD),
            CLIENT_ID,
            CLIENT_SECRET
        )
        console.log("\n\nReceiving Cancel WorkVisit Response Message  **********\n\n", safeStringify(result))
    })

    it('test_create_work_visit_extension', async function () {
        console.log("\n\nSending Create WorkVisit Request Message as per API Schema  **********\n\n")
        const result = await workVisitTemplate.createWorkVisitExtn(
            JSON.stringify(CREATE_WORKVISIT_PAYLOAD_AS_PER_API_SCHEMA),
            CLIENT_ID,
            CLIENT_SECRET
        );
        console.log("\n\nReceiving Create WorkVisit Response Message  **********\n\n", safeStringify(result))
    })

    it('test_update_work_visit_extension', async function () {
        console.log("\n\nSending Update WorkVisit Request Message as per API Schema **********\n\n")
        const result = await workVisitTemplate.updateWorkVisitExtn(
            JSON.stringify(UPDATE_WORKVISIT_PAYLOAD_AS_PER_API_SCHEMA),
            CLIENT_ID,
            CLIENT_SECRET
        )
        console.log("\n\nReceiving Update WorkVisit Response Message  **********\n\n", safeStringify(result))
    })

    it('test_cancel_work_visit_extension', async function () {
        console.log("\n\nSending Cancel WorkVisit Request Message as per API Schema **********\n\n")
        const result = await workVisitTemplate.cancelWorkVisitExtn(
            JSON.stringify(CANCEL_WORKVISIT_PAYLOAD_AS_PER_API_SCHEMA),
            CLIENT_ID,
            CLIENT_SECRET
        )
        console.log("\n\nReceiving Cancel WorkVisit Response Message  **********\n\n", safeStringify(result))
    })

    it('test_workvisit_notifications_open', async function () {
        console.log("\n\nSending WorkVisit Notification Request Message  **********\n\n")
        //(customerReferenceNumber, orderNumber, activityID, state - Open, InProgress, Cancelled, Closed)
        const result = await workVisitTemplate.getNotifications(null, ORDER_NUMBER, null, NOTIFICATION_OPEN)
        console.log("\n\nReceiving WorkVisit Notification Response Message  **********\n\n", safeStringify(result))
    })


    it('test_create_smarthands', async function () {
        console.log("\n\nSending Create SmartHands Request Message  **********\n\n")
        const result = await smartHandsTemplate.createSmartHands(
            JSON.stringify(CREATE_SMARTHAND_PAYLOAD),
            CLIENT_ID,
            CLIENT_SECRET
        )
        console.log("\n\nReceiving Create SmartHands Response Message  **********\n\n", safeStringify(result))
    })

    it('test_update_smarthands', async function () {
        console.log("\n\nSending Update SmartHands Request Message  **********\n\n")
        const result = await smartHandsTemplate.updateSmartHands(
            JSON.stringify(UPDATE_SMARTHAND_PAYLOAD),
            CLIENT_ID,
            CLIENT_SECRET
        )
        console.log("\n\nReceiving Update SmartHands Response Message  **********\n\n", safeStringify(result))
    })

    it('test_cancel_smarthands', async function () {
        console.log("\n\nSending Cancel SmartHands Request Message  **********\n\n")
        const result = await smartHandsTemplate.cancelSmartHands(
            JSON.stringify(CANCEL_SMARTHAND_PAYLOAD),
            CLIENT_ID,
            CLIENT_SECRET
        )
        console.log("\n\nReceiving Cancel SmartHands Response Message  **********\n\n", safeStringify(result))
    })

    it('test_smarthands_notifications_open', async function () {
        console.log("\n\nSending SmartHands Notification Request Message  **********\n\n")
        //(customerReferenceNumber, orderNumber, activityID, state - Open, InProgress, Pending Customer Input, Cancelled, Closed)
        const result = await smartHandsTemplate.getNotifications(null, ORDER_NUMBER, null, NOTIFICATION_OPEN)
        console.log("\n\nReceiving SmartHands Notification Response Message  **********\n\n", safeStringify(result))
    })

    it('test_create_troubleticket', async function () {
        console.log("\n\nSending Create TroubleTicket Request Message  **********\n\n")
        const result = await troubleTicketTemplate.createTroubleTicket(
            JSON.stringify(CREATE_TROUBLETICKET_PAYLOAD),
            CLIENT_ID,
            CLIENT_SECRET
        )
        console.log("\n\nReceiving Create TroubleTicket Response Message  **********\n\n", safeStringify(result))
    })

    it('test_update_troubleticket', async function () {
        console.log("\n\nSending Update TroubleTicket Request Message  **********\n\n")
        const result = await troubleTicketTemplate.updateTroubleTicket(
            JSON.stringify(UPDATE_TROUBLETICKET_PAYLOAD),
            CLIENT_ID,
            CLIENT_SECRET
        )
        console.log("\n\nReceiving Update TroubleTicket Response Message  **********\n\n", safeStringify(result))
    })

    it('test_cancel_troubleticket', async function () {
        console.log("\n\nSending Cancel TroubleTicket Request Message  **********\n\n")
        const result = await troubleTicketTemplate.cancelTroubleTicket(
            JSON.stringify(CANCEL_TROUBLETICKET_PAYLOAD),
            CLIENT_ID,
            CLIENT_SECRET
        )
        console.log("\n\nReceiving Cancel TroubleTicket Response Message  **********\n\n", safeStringify(result))
    })

    it('test_troubleticket_notifications_open', async function () {
        console.log("\n\nSending TroubleTicket Notification Request Message  **********\n\n")
        //(customerReferenceNumber, orderNumber, activityID, state - Open, InProgress, Pending Customer Input, Cancelled, Closed)
        const result = await troubleTicketTemplate.getNotifications(null, ORDER_NUMBER, null, NOTIFICATION_OPEN)
        console.log("\n\nReceiving TroubleTicket Notification Response Message  **********\n\n", safeStringify(result))
    })

    it('test_create_inbound_shipment_carriertype', async function () {
        console.log("\n\nSending Create Inbound Shipment Request Message  **********\n\n")
        const result = await shipmentTemplate.createShipment(
            JSON.stringify(CREATE_INBOUNDSHIPMENT_CARRIERTYPE_PAYLOAD),
            CLIENT_ID,
            CLIENT_SECRET
        )
        console.log("\n\nReceiving Create Inbound Shipment Response Message  **********\n\n", safeStringify(result))
    })

    it('test_create_inbound_shipment_customercarrytype', async function () {
        console.log("\n\nSending Create Inbound Shipment Request Message  **********\n\n")
        const result = await shipmentTemplate.createShipment(
            JSON.stringify(CREATE_INBOUNDSHIPMENT_CUSTOMERCARRYTYPE_PAYLOAD),
            CLIENT_ID,
            CLIENT_SECRET
        )
        console.log("\n\nReceiving Create Inbound Shipment Response Message  **********\n\n", safeStringify(result))
    })

    it('test_create_outbound_shipment_carriertype', async function () {
        console.log("\n\nSending Create Outbound Shipment Request Message  **********\n\n")
        const result = await shipmentTemplate.createShipment(
            JSON.stringify(CREATE_OUTBOUNDSHIPMENT_CARRIERTYPE_PAYLOAD),
            CLIENT_ID,
            CLIENT_SECRET
        )
        console.log("\n\nReceiving Create Outbound Shipment Response Message  **********\n\n", safeStringify(result))
    })

    it('test_create_outbound_shipment_customercarrytype', async function () {
        console.log("\n\nSending Create Outbound Shipment Request Message  **********\n\n")
        const result = await shipmentTemplate.createShipment(
            JSON.stringify(CREATE_OUTBOUNDSHIPMENT_CUSTOMERCARRYTYPE_PAYLOAD),
            CLIENT_ID,
            CLIENT_SECRET
        )
        console.log("\n\nReceiving Create Outbound Shipment Response Message  **********\n\n", safeStringify(result))
    })

    it('test_update_inbound_shipment', async function () {
        console.log("\n\nSending Update Inbound Shipment Request Message  **********\n\n")
        const result = await shipmentTemplate.updateShipment(
            JSON.stringify(UPDATE_INBOUNDSHIPMENT_PAYLOAD),
            CLIENT_ID,
            CLIENT_SECRET
        )
        console.log("\n\nReceiving Update Inbound Shipment Response Message  **********\n\n", safeStringify(result))
    })

    it('test_update_outbound_shipment', async function () {
        console.log("\n\nSending Update Outbound Shipment Request Message  **********\n\n")
        const result = await shipmentTemplate.updateShipment(
            JSON.stringify(UPDATE_OUTBOUNDSHIPMENT_PAYLOAD),
            CLIENT_ID,
            CLIENT_SECRET
        )
        console.log("\n\nReceiving Update Outbound Shipment Response Message  **********\n\n", safeStringify(result))
    })

    it('test_cancel_shipment', async function () {
        console.log("\n\nSending Cancel Shipment Request Message  **********\n\n")
        const result = await shipmentTemplate.cancelShipment(
            JSON.stringify(CANCEL_SHIPMENT_PAYLOAD),
            CLIENT_ID,
            CLIENT_SECRET
        )
        console.log("\n\nReceiving Cancel Shipment Response Message  **********\n\n", safeStringify(result))
    })

    it('test_shipment_notifications_open', async function () {
        console.log("\n\nSending Shipment Notification Request Message  **********\n\n")
        //(customerReferenceNumber, orderNumber, activityID, state - Open, InProgress, Pending Customer Input, Cancelled, Closed)
        const result = await shipmentTemplate.getNotifications(null, ORDER_NUMBER, null, NOTIFICATION_OPEN)
        console.log("\n\nReceiving Shipment Notification Response Message  **********\n\n", safeStringify(result))
    })

    it('test_create_crossConnect', async function () {
        console.log("\n\nSending Create crossConnect Request Message  **********\n\n")
        const result = await crossConnectTemplate.createCrossConnect(
            JSON.stringify(CREATE_CROSSCONNECT_PAYLOAD),
            CLIENT_ID,
            CLIENT_SECRET
        )
        console.log("\n\nReceiving Create crossConnect Response Message  **********\n\n", safeStringify(result))
    })

    it('test_crossConnect_notifications_open', async function () {
        console.log("\n\nSending crossConnect Notification Request Message  **********\n\n")
        //(customerReferenceNumber, orderNumber, activityID, state - Open, InProgress, Pending Customer Input, Cancelled, Closed)
        const result = await crossConnectTemplate.getNotifications(null, ORDER_NUMBER, null, NOTIFICATION_OPEN)
        console.log("\n\nReceiving crossConnect Notification Response Message  **********\n\n", safeStringify(result))
    })

})
