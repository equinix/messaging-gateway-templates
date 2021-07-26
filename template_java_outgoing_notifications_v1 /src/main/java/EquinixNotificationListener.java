import com.azure.messaging.servicebus.ServiceBusClientBuilder;
import com.azure.messaging.servicebus.ServiceBusProcessorClient;
import com.azure.messaging.servicebus.ServiceBusReceivedMessage;
import com.azure.messaging.servicebus.ServiceBusReceivedMessageContext;
import org.apache.commons.io.IOUtils;
import org.json.JSONArray;
import org.json.JSONObject;
import config.config;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.util.Base64;




public class EquinixNotificationListener {
    static String connectionString = config.EQUINIX_OUTGOING_QUEUE_CONNECTION_STRING;
    static String queueName = config.EQUINIX_OUTGOING_QUEUE;
    static String fileStorageKey = config.FILE_STORAGE_DOWNLOAD_KEY;

    public static void main(String args[]) throws Exception{
        receiveMessages();
    }

    static void receiveMessages() throws InterruptedException
    {

        // Create an instance of the processor through the ServiceBusClientBuilder
        ServiceBusProcessorClient processorClient = new ServiceBusClientBuilder()
                .connectionString(connectionString)
                .processor()
                .queueName(queueName)
                .processMessage(EquinixNotificationListener::processMessage)
                .processError(context -> processError(context.getMessage()))
                .buildProcessorClient();

        System.out.println("Starting the processor");
        processorClient.start();
    }

    private static void processError(String errorMessage){
        System.out.println("Error Occurred "+ errorMessage);
    }

    private static void processMessage(ServiceBusReceivedMessageContext context)  {
        try{
            ServiceBusReceivedMessage message = context.getMessage();
            System.out.printf("Processing message. Session: %s, Sequence #: %s. Contents: %s%n", message.getMessageId(),
                    message.getSequenceNumber(), message.getBody());
            
            JSONObject jsonObject = new JSONObject(message.getBody().toString());
            JSONObject taskObject =  new JSONObject(jsonObject.getString("Task"));
            JSONObject bodyObject =  taskObject.getJSONObject("Body");
            jsonObject.put("Task", taskObject);
            if(!bodyObject.isNull("Attachments") && !bodyObject.getJSONArray("Attachments").isEmpty()){
                JSONArray newAttachments = downloadAllAttachments(bodyObject.getJSONArray("Attachments"));
                jsonObject.getJSONObject("Task").getJSONObject("Body").put("Attachments", newAttachments);
            }
            System.out.println("Message Received "+bodyObject);

            // Complete the message
            // context.complete();
        }catch (Exception e){
            System.out.println("Error Occurred "+ e.getMessage());
        }

    }
    public static JSONArray downloadAllAttachments(JSONArray attachments) throws IOException {
        JSONArray newAttachments = new JSONArray();
        for(int i = 0; i<attachments.length();i++){
            JSONObject attachment = attachments.getJSONObject(i);
            if(!attachment.has("Url")){
                newAttachments.put(attachment);
                continue;
            }
            String downloadUrl = attachment.getString("Url") + "?"+fileStorageKey;
            String base64 = downloadFile(downloadUrl);
            JSONObject json = new JSONObject();
            json.put("Name", attachment.get("Name"));
            json.put("Data", base64);
            newAttachments.put(json);
        }
        return newAttachments;
    }

    public static String downloadFile(String fileUrl) throws IOException {
        URL url = new URL(fileUrl);
        InputStream is = null;
        byte[] bytes = null;
        is = url.openStream ();
        bytes = IOUtils.toByteArray(is);
        is.close();
        return Base64.getEncoder().encodeToString(bytes);
    }
}
