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
'Option Strict';
const safeStringify = require('fast-safe-stringify')
const { ServiceBusClient} = require("@azure/service-bus");
const config = require('../config/config');

function createServiceBusClient(connectionString) {
    var sbc = ServiceBusClient.createFromConnectionString(connectionString);
    return sbc;
}

function createTopicClient(sbc, topicName) {
    var topicClient = sbc.createTopicClient(topicName);

    return topicClient;
}

function getSender(client) {
    var sender = client.createSender();

    return sender;
}
async function sendMessage(sender, message) {
    serializeBody(message);
    await sender.send(message);
}

async function closeSender(sender) {
    await sender.close();
}

async function closeServiceBusClient(sbc) {
    await sbc.close();
}

function serializeBody(msg) {
    if (msg != null && msg.body != null && msg.body.Body != null) {
            var jsonAsString = safeStringify(msg.body.Body);
            msg.body.Body = jsonAsString;
    }
}

async function sendMessageToQueue(payload, label) {
    try {
        var sbns = createServiceBusClient(config.EQUINIX_INCOMING_QUEUE_CONNECTION_STRING);
        var tc = createTopicClient(sbns, config.EQUINIX_INCOMING_QUEUE);
        var sender = getSender(tc);
        const messageToSend = {
            body: payload,
            label: label
        };
        await sendMessage(sender, messageToSend);
        await closeSender(sender);
        await closeServiceBusClient(sbns);
    } catch (e) {
        throw Error(
            safeStringify(formatError(400,e.message))
        );
    } 
}


module.exports = {
    createServiceBusClient: createServiceBusClient,
    closeServiceBusClient: closeServiceBusClient,
    createTopicClient: createTopicClient,
    getSender: getSender,
    sendMessage: sendMessage,
    closeSender: closeSender,
    sendMessageToQueue: sendMessageToQueue
}