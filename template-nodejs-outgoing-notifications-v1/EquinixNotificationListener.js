const { ServiceBusClient, ReceiveMode } = require("@azure/service-bus");
var config = require('./config/config');
const axios = require('axios')

function StartListener() {
    const sbClient = ServiceBusClient.createFromConnectionString(config.EQUINIX_OUTGOING_QUEUE_CONNECTION_STRING);
    // The createReceiver (receiveMode) method of Azure Service Bus SDK reads message from the queue and auto-deletes it post successfully reading the message.
    // To explicitly delete the message instead of auto delete, please use createReceiver (receiveMode) method as shown below:
    //const receiver = queueClient.createReceiver({receiveMode: ReceiveMode.peekLock});

    const queueClient = sbClient.createQueueClient(config.EQUINIX_OUTGOING_QUEUE);
    const receiver = queueClient.createReceiver({ receiveMode: ReceiveMode.receiveAndDelete });

    receiver.registerMessageHandler(
        async (message) => {
            try {
                // In this block, Customer can write custom code to process the message and push to database... 
                var task = JSON.parse(message.body.Task);
                if(task.Body.Attachments && task.Body.Attachments.length > 0){
                    task.Body.Attachments = await downloadAllAttachments(task.Body.Attachments);
                }

                console.log(`Received message: ${JSON.stringify(task)}`);
                // To explicitly delete the message instead of auto delete, please use message.complete() method as shown below in conjunction with createReceiver (queueName, receiveMode) mentioned above.
                //await message.complete();
            } catch (error) {
                console.log(`Error Occured while proceesing the received message: ${err}`);
            }
        },
        (err) => {
            console.log(`Error Occured: ${err}`);
        },
        {
            autoComplete: true,
            maxMessageAutoRenewLockDurationInSeconds: 300,
            maxConcurrentCalls: 1,
        }
    );
}
async function downloadAllAttachments(attachments){
    try{
        var newAttachments = [];
        for(var key in attachments){
            if(!attachments[key]['Url']){
                newAttachments.push(attachments[key]);
                continue;
            }
            var downloadURL= `${attachments[key].Url}?${config.FILE_STORAGE_DOWNLOAD_KEY}`;
            const response = await axios.get(downloadURL,{responseType: 'arraybuffer'});
            const buffer = Buffer.from(response.data, "utf-8").toString("base64");
            newAttachments.push({"Name": `${attachments[key].Name}`, "Data": buffer});
        }
        return newAttachments;
    }catch(e){
        console.log(`Error Occured while proceesing the received message: ${e}`);
    }
}

module.exports = {
    StartListener
}
//Starting the listener
StartListener();
