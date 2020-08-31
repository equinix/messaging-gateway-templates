/** EQUINIX MESSAGING GATEWAY TEMPLATE **/

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
const safeStringify = require('fast-safe-stringify');
var sbb = require('./ServiceBusBase');
var uuid = require('uuid/v4');
const { ReceiveMode} = require("@azure/service-bus");
const config = require('../config/config');

const EQUINIX_INCOMING_QUEUE = config.EQUINIX_INCOMING_QUEUE;
const EQUINIX_INCOMING_QUEUE_CONNECTION_STRING = config.EQUINIX_INCOMING_QUEUE_CONNECTION_STRING;
const EQUINIX_OUTGOING_QUEUE = config.EQUINIX_OUTGOING_QUEUE;
const EQUINIX_OUTGOING_QUEUE_CONNECTION_STRING = config.EQUINIX_OUTGOING_QUEUE_CONNECTION_STRING;
const SOURCE_ID = config.SOURCE_ID;

const messageProcessor = async (JSONObj, actionVerb, ResourceType, clientID, clientSecret) => {    
    var messageInput = createPayload(JSONObj, actionVerb, ResourceType, SOURCE_ID, clientID, clientSecret);
    const messageId = JSON.parse(messageInput.Task).Id;
    console.log("Message ID:   ", messageId);
    try {
        await sendMessageToQueue(EQUINIX_INCOMING_QUEUE_CONNECTION_STRING, EQUINIX_INCOMING_QUEUE, messageInput, "IOMA-Message");
    } catch (e) {
        return processErrorResponse(e,EQUINIX_INCOMING_QUEUE_CONNECTION_STRING, EQUINIX_INCOMING_QUEUE, "send");
    }
    try {
        var queueMsg = await readFromQueue(messageId, null);
        return queueMsg;
    } catch (e) {
        return processErrorResponse(e,EQUINIX_OUTGOING_QUEUE_CONNECTION_STRING, EQUINIX_OUTGOING_QUEUE, "receive");
    }
}

function createPayload(JSONObj, actionVerb, ResourceType, SOURCE_ID, ClientId, ClientSecret){
    var messageInput = {
        Task: {
            Id: uuid(),
            Verb: (actionVerb == "Cancelled") ? "Update" : actionVerb,
            Source: SOURCE_ID,
            Version: "1.0",
            Resource: ResourceType,
            ContentType: "application/json",
            CreateTimeUTC: (new Date()).toISOString(),
            OriginationId: null,
            OriginationVerb: null,
            Body: JSONObj
        },
        Authentication: {
            "ClientId": ClientId,
            "ClientSecret": ClientSecret
        }
    };
    messageInput.Task = safeStringify(messageInput.Task);
    return messageInput;
}

async function sendMessageToQueue(connectionString, topic, payload, label) {
    try {
        var sbns = sbb.createServiceBusClient(connectionString);
        var tc = sbb.createTopicClient(sbns, topic);
        var sender = sbb.getSender(tc);
        const messageToSend = {
            body: payload,
            label: label
        };
        await sbb.sendMessage(sender, messageToSend);
        await sbb.closeSender(sender);
        await sbb.closeServiceBusClient(sbns);
    } catch (e) {
        throw Error(
            safeStringify(formatError(400,e.message))
        );
    } 
}

async function readFromQueue(messageId, filterCriteria) {
    var res;
    try {
        const sbc = sbb.createServiceBusClient(EQUINIX_OUTGOING_QUEUE_CONNECTION_STRING);
        const queueClient = sbc.createQueueClient(EQUINIX_OUTGOING_QUEUE);
        const receiver = queueClient.createReceiver(ReceiveMode.peekLock);
        for await (let message of receiver.getMessageIterator()) {
            if (message == undefined) {
                res = "No msgs to read";
                break;
            } else if (filterCriteria != null) {
                var JSONObj = JSON.parse(message.body.Task);
                var obj = [JSONObj];
                var result = obj
                .filter(a => filterCriteria.ResourceType!=null ?a.Resource == filterCriteria.ResourceType :a )
                .filter(a => filterCriteria.RequestorId!=null ?a.Body.RequestorId == filterCriteria.RequestorId: a)
                .filter(a => filterCriteria.ServicerId!=null ?a.Body.ServicerId == filterCriteria.ServicerId: a)
                .filter(a => filterCriteria.Activity!=null ? a.Body.Activity == filterCriteria.Activity: a)
                .filter(a => filterCriteria.State!=null ? a.Body.State == filterCriteria.State: a);

                if (result.length > 0) {
                    res = JSONObj;
                    await message.complete();
                    break;
                }
            } else {
                var JSONObj = JSON.parse(message.body.Task)
                if (JSONObj.OriginationId == messageId && JSONObj.Verb == "Ack") {
                    res = JSONObj;
                    await message.complete();
                    break;
                }
            }
        }
        await queueClient.close();
        await sbc.close();
        return res;
    }
    catch (e) {
        throw Error(
            safeStringify(formatError(400,e.message))
        );
    }
}

function formatError(StatusCode, Description){
    return {
        Body:{
            StatusCode: StatusCode,
            Description: Description
        }
    };
}
function formatErrorResponse (StatusCode, Description){
    return safeStringify( {
        errors: [{
            code: StatusCode,
            message: Description
        }]
    });
}

function processErrorResponse(errorObj, connectionString, entityName, mode) {
    var error = JSON.parse(errorObj.message);
    if (error.hasOwnProperty('Body')) {
        if (mode == 'send') {
            if (error.Body.Description == 'Missing Endpoint in Connection String.' ||
                (error.Body.Description).includes('The token has an invalid signature') ||
                (error.Body.Description).includes('getaddrinfo ENOTFOUND')) {
                return formatErrorResponse(error.Body.StatusCode, `'Invalid incoming queue connection string. Either Client Shared Key Name/Shared Key value is invalid`);
            } else if ((error.Body.Description).includes('The messaging entity')) {
                return formatErrorResponse(error.Body.StatusCode, `'Invalid connection string. Invalid incoming queue name for  ${entityName}`);
            } else {
                return formatErrorResponse(500, 'Internal Server Error');
            }
        } else if (mode == 'receive') {
            if (error.Body.Description == 'Missing Endpoint in Connection String.' ||
                (error.Body.Description).includes('The token has an invalid signature') ||
                (error.Body.Description).includes('getaddrinfo ENOTFOUND')) {
                return formatErrorResponse(error.Body.StatusCode, `Invalid outgoing queue connection string. Either Client Shared Key Name/Shared Key value is invalid`);
            } else if ((error.Body.Description).includes('The messaging entity')) {
                return formatErrorResponse(error.Body.StatusCode, `'Invalid connection string. Invalid outgoing queue name for ${entityName}`);
            } else {
                return formatErrorResponse(500, 'Internal Server Error');
            }
        }
    } else {
        return formatErrorResponse(500, e.message);
    }
}
module.exports = {
    messageProcessor: messageProcessor,
    sendMessageToQueue: sendMessageToQueue,
    readFromQueue : readFromQueue
};