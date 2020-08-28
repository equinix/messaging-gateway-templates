'Option Strict';
const safeStringify = require('fast-safe-stringify')
const { ServiceBusClient} = require("@azure/service-bus");


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

module.exports = {
    createServiceBusClient: createServiceBusClient,
    closeServiceBusClient: closeServiceBusClient,
    createTopicClient: createTopicClient,
    getSender: getSender,
    sendMessage: sendMessage,
    closeSender: closeSender
}