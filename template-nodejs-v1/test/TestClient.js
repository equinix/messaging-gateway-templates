/** EQUINIX MESSAGING GATEWAY TEST CLIENT **/

/*************************************************************************
* 
* EQUINIX CONFIDENTIAL
* __________________
* 
*  © 2020 Equinix, Inc. All rights reserved.
* 
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the "Software"), to deal
* in the Software without restriction, including without limitation the rights
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
* copies of the Software, and to permit persons to whom the Software is
* furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included in
* all copies or substantial portions of the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
* OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
* THE SOFTWARE.
*
* Terms of Use: https://www.equinix.com/company/legal/terms/
*
*************************************************************************/


'use strict'
const workVisitTemplate = require('../EquinixWorkVisitTemplate')
const smartHandsTemplate = require('../EquinixSmartHandsTemplate')
const troubleTicketTemplate = require('../EquinixTroubleTicketTemplate')
const safeStringify = require('fast-safe-stringify');
const config = require('../config/config');

var ORDER_NUMBER = "<ORDER_NUMBER>";
var CLIENT_ID = "<CLIENT_ID>"; // Will be supplied by Customer
var CLIENT_SECRET = "<CLIENT_SECRET>"; // Will be supplied by Customer

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

const CREATE_SMARTHAND_PAYLOAD = {
    "CustomerContact": "<CUSTOMER_CONTACT>",
    "Attachments": [],
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
    "CallFromCage": false,
}

const CANCEL_TROUBLETICKET_PAYLOAD = {
    "Description": "Test description for TroubleTicket Cancel",
    "ServicerId": ORDER_NUMBER,
    "State": "Cancelled"
}

describe('EMG Template Test Suite', function () {
    this.timeout(10000000);
    it('#Create WorkVisit', async function () {
        console.log("\n\nSending Create WorkVisit Request Message  **********\n\n")
        const result = await workVisitTemplate.createWorkVisit(
            JSON.stringify(CREATE_WORKVISIT_PAYLOAD),
            CLIENT_ID,
            CLIENT_SECRET
        );
        console.log("\n\nReceiving Create WorkVisit Response Message  **********\n\n", safeStringify(result))
    })

    it('#Update WorkVisit', async function () {
        console.log("\n\nSending Update WorkVisit Request Message  **********\n\n")
        const result = await workVisitTemplate.updateWorkVisit(
            JSON.stringify(UPDATE_WORKVISIT_PAYLOAD),
            CLIENT_ID,
            CLIENT_SECRET
        )
        console.log("\n\nReceiving Update WorkVisit Response Message  **********\n\n", safeStringify(result))
    })

    it('#Cancel WorkVisit', async function () {
        console.log("\n\nSending Cancel WorkVisit Request Message  **********\n\n")
        const result = await workVisitTemplate.cancelWorkVisit(
            JSON.stringify(CANCEL_WORKVISIT_PAYLOAD),
            CLIENT_ID,
            CLIENT_SECRET
        )
        console.log("\n\nReceiving Cancel WorkVisit Response Message  **********\n\n", safeStringify(result))
    })

    it('#Get Notifications for WorkVisit, Open', async function () {
        console.log("\n\nSending WorkVisit Notification Request Message  **********\n\n")
        //(customerReferenceNumber, orderNumber, activityID, state - Open, InProgress, Cancelled, Closed)
        const result = await workVisitTemplate.getNotifications(null, ORDER_NUMBER, null, "Open")
        console.log("\n\nReceiving WorkVisit Notification Response Message  **********\n\n", safeStringify(result))
    })


    it('#Create SmartHands', async function () {
        console.log("\n\nSending Create SmartHands Request Message  **********\n\n")
        const result = await smartHandsTemplate.createSmartHands(
            JSON.stringify(CREATE_SMARTHAND_PAYLOAD),
            CLIENT_ID,
            CLIENT_SECRET
        )
        console.log("\n\nReceiving Create SmartHands Response Message  **********\n\n", safeStringify(result))
    })

    it('#Update SmartHands', async function () {
        console.log("\n\nSending Update SmartHands Request Message  **********\n\n")
        const result = await smartHandsTemplate.updateSmartHands(
            JSON.stringify(UPDATE_SMARTHAND_PAYLOAD),
            CLIENT_ID,
            CLIENT_SECRET
        )
        console.log("\n\nReceiving Update SmartHands Response Message  **********\n\n", safeStringify(result))
    })

    it('#Cancel SmartHands', async function () {
        console.log("\n\nSending Cancel SmartHands Request Message  **********\n\n")
        const result = await smartHandsTemplate.cancelSmartHands(
            JSON.stringify(CANCEL_SMARTHAND_PAYLOAD),
            CLIENT_ID,
            CLIENT_SECRET
        )
        console.log("\n\nReceiving Cancel SmartHands Response Message  **********\n\n", safeStringify(result))
    })

    it('#Get Notifications for SmartHands, Open', async function () {
        console.log("\n\nSending SmartHands Notification Request Message  **********\n\n")
        //(customerReferenceNumber, orderNumber, activityID, state - Open, InProgress, Pending Customer Input, Cancelled, Closed)
        const result = await smartHandsTemplate.getNotifications(null, ORDER_NUMBER, null, "Open")
        console.log("\n\nReceiving SmartHands Notification Response Message  **********\n\n", safeStringify(result))
    })

    it('#Create TroubleTicket', async function () {
        console.log("\n\nSending Create TroubleTicket Request Message  **********\n\n")
        const result = await troubleTicketTemplate.createTroubleTicket(
            JSON.stringify(CREATE_TROUBLETICKET_PAYLOAD),
            CLIENT_ID,
            CLIENT_SECRET
        )
        console.log("\n\nReceiving Create TroubleTicket Response Message  **********\n\n", safeStringify(result))
    })

    it('#Update TroubleTicket', async function () {
        console.log("\n\nSending Update TroubleTicket Request Message  **********\n\n")
        const result = await troubleTicketTemplate.updateTroubleTicket(
            JSON.stringify(UPDATE_TROUBLETICKET_PAYLOAD),
            CLIENT_ID,
            CLIENT_SECRET
        )
        console.log("\n\nReceiving Update TroubleTicket Response Message  **********\n\n", safeStringify(result))
    })

    it('#Cancel TroubleTicket', async function () {
        console.log("\n\nSending Cancel TroubleTicket Request Message  **********\n\n")
        const result = await troubleTicketTemplate.cancelTroubleTicket(
            JSON.stringify(CANCEL_TROUBLETICKET_PAYLOAD),
            CLIENT_ID,
            CLIENT_SECRET
        )
        console.log("\n\nReceiving Cancel TroubleTicket Response Message  **********\n\n", safeStringify(result))
    })

    it('#Get Notifications for TroubleTicket, Open', async function () {
        console.log("\n\nSending TroubleTicket Notification Request Message  **********\n\n")
        //(customerReferenceNumber, orderNumber, activityID, state - Open, InProgress, Pending Customer Input, Cancelled, Closed)
        const result = await troubleTicketTemplate.getNotifications(null, ORDER_NUMBER, null, "Open")
        console.log("\n\nReceiving TroubleTicket Notification Response Message  **********\n\n", safeStringify(result))
    })
})
