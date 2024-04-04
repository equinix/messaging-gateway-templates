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

package util;

import com.azure.core.util.IterableStream;
import com.azure.messaging.servicebus.ServiceBusClientBuilder;
import com.azure.messaging.servicebus.ServiceBusReceivedMessage;
import com.azure.messaging.servicebus.ServiceBusReceiverClient;
import com.azure.messaging.servicebus.models.ReceiveMode;
// import com.azure.storage.blob.BlobClient;
// import com.azure.storage.blob.BlobContainerClient;
// import com.azure.storage.blob.BlobServiceClient;
// import com.azure.storage.blob.BlobServiceClientBuilder;
import config.config;
import org.apache.commons.io.IOUtils;
import org.json.JSONArray;
import org.json.JSONObject;
import org.json.JSONTokener;

import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.nio.file.Files;
import java.time.Duration;
import java.time.ZoneOffset;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.stream.Collectors;

public class MessageUtil {

    public static String EQUINIX_INCOMING_QUEUE = config.EQUINIX_INCOMING_QUEUE;
    public static String EQUINIX_INCOMING_QUEUE_CONNECTION_STRING = config.EQUINIX_INCOMING_QUEUE_CONNECTION_STRING;
    public static String EQUINIX_OUTGOING_QUEUE = config.EQUINIX_OUTGOING_QUEUE;
    public static String EQUINIX_OUTGOING_QUEUE_CONNECTION_STRING = config.EQUINIX_OUTGOING_QUEUE_CONNECTION_STRING;
    public static String SOURCE_ID = config.SOURCE_ID;

    public static final String INVALID_TOKEN_SIGNATURE = "The token has an invalid signature";
    public static final String INVALID_INCOMING_QUEUE_CONNECTION = "Missing Endpoint in Connection String.";
    public static final String INVALID_ENTITY = "The messaging entity";
    public static final String INVALID_OUTGOING_QUEUE_CONNECTION = "Missing Endpoint in Connection String.";
    public static final String FAILED_ESTABLISH_CONNECTION = "getaddrinfo ENOTFOUND";
    public static final String INTERNAL_SERVER_ERROR = "Internal Server Error";

    public static final String CREATE_OPERATION = "Create";
    public static final String UPDATE_OPERATION = "Update";
    public static final String CANCEL_OPERATION = "Cancelled";
    public static final String TICKET_TYPE_SHIPPING = "Shipping";
    public static final String TICKET_TYPE_SMARTHANDS = "SmartHands";
    public static final String TICKET_TYPE_WORKVISIT = "WorkVisit";
    public static final String TICKET_TYPE_BREAKFIX = "BreakFix";
    public static final String TICKET_TYPE_CROSSCONNECT = "CrossConnect";
    public static JSONObject task_obj;

    public JSONObject messageProcessor(JSONObject JSONObj, String actionVerb, String ResourceType, String clientID, String clientSecret, Boolean isOAuthType) throws Exception {
        if (actionVerb.equals("Cancelled")) {
            actionVerb = "Update";
        }
        if (!JSONObj.isNull("Attachments") && !JSONObj.getJSONArray("Attachments").isEmpty()) {
            JSONObj.put("Attachments", uploadAllAttachments(JSONObj.getJSONArray("Attachments")));
        }

        if(!JSONObj.isNull("ConnectionDetails") && !JSONObj.getJSONArray("ConnectionDetails").isEmpty()){
            JSONArray ConnectionDetailsJSONArray = (JSONArray) new JSONTokener(JSONObj.get("ConnectionDetails").toString()).nextValue();
            for(int i = 0; i < ConnectionDetailsJSONArray.length(); i++){
                JSONObject jConnectionDetailObject = ConnectionDetailsJSONArray.getJSONObject(i);
                if(!jConnectionDetailObject.isNull("ZSide")) {
                    JSONObject zSideJSON = new JSONObject(jConnectionDetailObject.get("ZSide").toString());
                    if (!zSideJSON.isNull("LOAAttachment")) {
                        System.out.println(zSideJSON.get("LOAAttachment"));
                        JSONArray LOAAttachmentArray = new JSONArray();
                        LOAAttachmentArray.put(zSideJSON.get("LOAAttachment"));
                        JSONObject LOAAttachmentUpload = uploadAllAttachments(LOAAttachmentArray).getJSONObject(0);
                        zSideJSON.put("LOAAttachment", LOAAttachmentUpload);
                        jConnectionDetailObject.put("ZSide", zSideJSON);
                        ConnectionDetailsJSONArray.put(i,jConnectionDetailObject);
                        System.out.println(JSONObj);
                    }
                }
            }
            JSONObj.put("ConnectionDetails",ConnectionDetailsJSONArray);
        }
        JSONObject messageInput = null;
        if(isOAuthType){
            messageInput = createPayloadUsingOAuth(JSONObj, actionVerb, ResourceType, SOURCE_ID,clientSecret);
        }else{
            messageInput = createPayload(JSONObj, actionVerb, ResourceType, SOURCE_ID, clientID, clientSecret);
        }
        task_obj = new JSONObject(messageInput.get("Task").toString());
        String messageId = messageInput.getJSONObject("Task").get("Id").toString();
        System.out.println("\n\nMessage ID:   " + messageId + "\n\n");

        try {
            ServiceBusBase.sendMessageToQueue(messageInput, "IOMA-Message");
        } catch (Exception e) {
            return processErrorResponse(e.getMessage(), "send", task_obj);
        }
        try {
            return read_messages_from_queue(messageId, null);
        } catch (Exception e) {
            return processErrorResponse(e.getMessage(), "receive", task_obj);
        }

    }

    public JSONObject createPayload(JSONObject JSONObj, String actionVerb, String ResourceType, String SOURCE_ID, String ClientId, String ClientSecret) {
        String nowAsISO = ZonedDateTime.now(ZoneOffset.UTC).format(DateTimeFormatter.ISO_INSTANT);
        UUID uuid = UUID.randomUUID();
        JSONObject parentObject = new JSONObject("{\n" +
                "    \"Task\": {\n" +
                "    \"Id\": \"" + uuid + "\",\n" +
                "    \"Body\": " + JSONObj + ",\n" +
                "    \"Verb\": \"" + actionVerb + "\",\n" +
                "    \"Source\": \"" + SOURCE_ID + "\",\n" +
                "    \"Version\": \"1.0\",\n" +
                "    \"Resource\": \"" + ResourceType + "\",\n" +
                "    \"ContentType\": \"application/json\",\n" +
                "    \"CreateTimeUTC\": \"" + nowAsISO + "\",\n" +
                "    \"OriginationId\": \"\",\n" +
                "    \"OriginationVerb\": \"\"\n" +
                "},\n" +
                "    \"Authentication\": {\n" +
                "    \"ClientId\": \"" + ClientId + "\",\n" +
                "    \"ClientSecret\": \"" + ClientSecret + "\",\n" +
                "}\n" +
                "}");
        return parentObject;
    }

    public JSONObject createPayloadUsingOAuth(JSONObject JSONObj, String actionVerb, String ResourceType, String SOURCE_ID, String OAuthToken) {
        String nowAsISO = ZonedDateTime.now(ZoneOffset.UTC).format(DateTimeFormatter.ISO_INSTANT);
        UUID uuid = UUID.randomUUID();
        JSONObject parentObject = new JSONObject("{\n" +
                "    \"Task\": {\n" +
                "    \"Id\": \"" + uuid + "\",\n" +
                "    \"Body\": " + JSONObj + ",\n" +
                "    \"Verb\": \"" + actionVerb + "\",\n" +
                "    \"Source\": \"" + SOURCE_ID + "\",\n" +
                "    \"Version\": \"1.0\",\n" +
                "    \"Resource\": \"" + ResourceType + "\",\n" +
                "    \"ContentType\": \"application/json\",\n" +
                "    \"CreateTimeUTC\": \"" + nowAsISO + "\",\n" +
                "    \"OriginationId\": \"\",\n" +
                "    \"OriginationVerb\": \"\"\n" +
                "},\n" +
                "    \"Authentication\": {\n" +
                "    \"ClientId\": \"" + OAuthToken + "\",\n" +
                "}\n" +
                "}");
        return parentObject;
    }

    public static JSONObject read_messages_from_queue(String messageId, JSONObject filters) throws Exception {
        JSONObject[] ret_json_object = new JSONObject[1];
        String connectionString = config.EQUINIX_OUTGOING_QUEUE_CONNECTION_STRING;
        String queueName = config.EQUINIX_OUTGOING_QUEUE;
        for (int i = 0; i < 10; i++) {
            ServiceBusReceiverClient receiver = new ServiceBusClientBuilder()
                    .connectionString(connectionString)
                    .receiver().receiveMode(ReceiveMode.PEEK_LOCK)
                    .queueName(queueName)
                    .buildClient();
            IterableStream<ServiceBusReceivedMessage> messages = receiver.receiveMessages(5, Duration.ofSeconds(5));
            for (ServiceBusReceivedMessage message : messages) {
                if (message != null && message.getBody() != null) {
                    JSONObject json_temp = new JSONObject(message.getBody().toString());
                    if (json_temp.has("Task")) {
                        JSONObject json_obj = new JSONObject(json_temp.get("Task").toString());
                        if (filters != null && json_obj != null && json_obj.has("Body")) {
                            JSONObject body_json_obj = new JSONObject(json_obj.get("Body").toString());
                            if (!body_json_obj.has("RequestorId")) body_json_obj.put("RequestorId", "");
                            if (!body_json_obj.has("ServicerId")) body_json_obj.put("ServicerId", "");
                            if (!body_json_obj.has("State")) body_json_obj.put("State", "");
                            if (!body_json_obj.has("Activity")) body_json_obj.put("Activity", "");

                            List<JSONObject> listcom = Arrays.asList(json_obj).stream()
                                    .filter(!filters.get("ResourceType").equals(null) ? json -> filters.get("ResourceType").toString().equalsIgnoreCase(json_obj.get("Resource").toString()) : json -> true)
                                    .filter(!filters.get("RequestorId").equals(null) ? json -> filters.get("RequestorId").toString().equalsIgnoreCase(body_json_obj.get("RequestorId").toString()) : json -> true)
                                    .filter(!filters.get("ServicerId").equals(null) ? json -> filters.get("ServicerId").toString().equalsIgnoreCase(body_json_obj.get("ServicerId").toString()) : json -> true)
                                    .filter(!filters.get("State").equals(null) ? json -> filters.get("State").toString().equalsIgnoreCase(body_json_obj.get("State").toString()) : json -> true)
                                    .filter(!filters.get("Activity").equals(null) ? json -> filters.get("Activity").toString().equalsIgnoreCase(body_json_obj.get("Activity").toString()) : json -> true)
                                    .collect(Collectors.toList());
                            if (listcom.size() > 0) {
                                ret_json_object[0] = new JSONObject(json_temp.get("Task").toString());
                                receiver.complete(message);
                                return ret_json_object[0];
                            }
                        } else {
                            if (json_obj.get("OriginationId").toString().equalsIgnoreCase(messageId)) {
                                ret_json_object[0] = new JSONObject(json_temp.get("Task").toString());
                                receiver.complete(message);
                                return ret_json_object[0];
                            }
                        }
                    }
                }
            }
            receiver.close();
        }
        JSONObject jsonObject = ret_json_object[0] != null ? ret_json_object[0] : new JSONObject("{ \"Result\" : \"No Messages to Read from Queue\"}");
        return jsonObject;
    }

    public static JSONObject formatErrorResponse(String StatusCode, String Description, JSONObject messageInput) {
        UUID uuid = UUID.randomUUID();
        JSONObject jsonObject = new JSONObject("{\n" +
                "    \"Id\": \"" + uuid + "\",\n" +
                "    \"Body\": {\n" +
                "    \"StatusCode\": \"" + StatusCode + "\",\n" +
                "    \"Description\": \"" + Description + "\"\n" +
                "},\n" +
                "    \"Verb\": \"Ack\",\n" +
                "    \"Source\": \"" + SOURCE_ID + "\",\n" +
                "    \"Version\": \"1.0\",\n" +
                "    \"Resource\": \"" + messageInput.get("Resource") + "\",\n" +
                "    \"ContentType\": \"" + messageInput.get("ContentType") + "\",\n" +
                "    \"CreateTimeUTC\": \"" + messageInput.get("CreateTimeUTC") + "\",\n" +
                "    \"OriginationId\": \"\",\n" +
                "    \"OriginationVerb\": \"" + messageInput.get("Verb") + "\"\n" +
                "}\n");
        return jsonObject;
    }

    public static JSONObject processErrorResponse(String errorObj, String mode, JSONObject messageInput) {
        String[] errorpair = errorObj.split(",");
        HashMap<String, String> errormap = new HashMap<String, String>();
        for (int i = 0; i < errorpair.length; i++) {
            String[] errorTemp = errorpair[i].split(":");
            if (errorTemp.length < 2)
                errormap.put(errorTemp[0].trim(), errorTemp[i].trim());
            else
                errormap.put(errorTemp[0].trim(), errorpair[i].substring(errorTemp[0].length() + 1).trim());
        }
        if (errormap.containsKey("status-description")) {
            if (mode.equalsIgnoreCase("send")) {
                if (errormap.get("status-description").contains(INVALID_INCOMING_QUEUE_CONNECTION) ||
                        errormap.get("status-description").contains(INVALID_TOKEN_SIGNATURE) ||
                        errormap.get("status-description").contains(FAILED_ESTABLISH_CONNECTION)) {
                    return formatErrorResponse(errormap.get("status-code"), "Error occured while sending message using connection string :" + EQUINIX_INCOMING_QUEUE_CONNECTION_STRING, messageInput);
                } else if (errormap.get("status-description").contains(INVALID_ENTITY)) {
                    return formatErrorResponse(errormap.get("status-code"), "Error occured while sending message using queue name : " + EQUINIX_INCOMING_QUEUE, messageInput);
                } else {
                    return formatErrorResponse("500", INTERNAL_SERVER_ERROR, messageInput);
                }
            } else if (mode.equalsIgnoreCase("receive")) {
                if (errormap.get("status-description").contains(INVALID_OUTGOING_QUEUE_CONNECTION) ||
                        errormap.get("status-description").contains(INVALID_TOKEN_SIGNATURE) ||
                        errormap.get("status-description").contains(FAILED_ESTABLISH_CONNECTION)) {
                    return formatErrorResponse(errormap.get("status-code"), "Error occured while reading message using connection string :" + EQUINIX_OUTGOING_QUEUE_CONNECTION_STRING, messageInput);
                } else if (errormap.get("status-description").contains(INVALID_ENTITY)) {
                    return formatErrorResponse(errormap.get("status-code"), "Error occured while reading message using queue name : " + EQUINIX_OUTGOING_QUEUE, messageInput);
                } else {
                    return formatErrorResponse("500", INTERNAL_SERVER_ERROR, messageInput);
                }
            }
        } else {
            return formatErrorResponse("500", errorObj, messageInput);
        }
        return null;
    }

    public static JSONArray uploadAllAttachments(JSONArray attachments) throws IOException {
        JSONArray newAttachments = new JSONArray();
        for (int i = 0; i < attachments.length(); i++) {
            JSONObject attachment = attachments.getJSONObject(i);
            if (attachment.isNull("Data")) {
                newAttachments.put(attachment);
                break;
            }

            byte[] data = Base64.getDecoder().decode(attachment.getString("Data"));
            newAttachments.put(uploadFile(data, attachment.getString("Name")));
        }
        return newAttachments;
    }

    public static JSONObject uploadFile(byte[] bytes, String originalFilename) throws IOException {
        // int lastSplitIndex = originalFilename.lastIndexOf('.');
        // String fileName = originalFilename.substring(0, lastSplitIndex);
        // String[] fileSplit = originalFilename.split("\\.");
        // String fileExtension = fileSplit[fileSplit.length - 1];

        // String blobName = fileName + System.currentTimeMillis() + "." + fileExtension;

        // BlobServiceClient blobServiceClient = new BlobServiceClientBuilder().endpoint(config.FILE_STORAGE_URL).sasToken(config.FILE_STORAGE_UPLOAD_KEY).buildClient();
        // BlobContainerClient blobContainerClient = blobServiceClient.getBlobContainerClient(config.FILE_STORAGE_DIRECTORY);
        // BlobClient blobClient = blobContainerClient.getBlobClient(blobName);

        // InputStream fileStream = new ByteArrayInputStream(bytes);
        // blobClient.upload(fileStream, bytes.length);
        JSONObject json = new JSONObject();
        // json.put("Name", blobName);
        // json.put("Url", blobClient.getBlobUrl());
        return json;
    }

    public static String encodeFileToBase64(File file) {
        try {
            byte[] fileContent = Files.readAllBytes(file.toPath());
            return Base64.getEncoder().encodeToString(fileContent);
        } catch (IOException e) {
            throw new IllegalStateException("could not read file " + file, e);
        }
    }

    public static String encodeFileToBase64(String path) {
        File targetFile = new File(path);
        return encodeFileToBase64(targetFile);
    }

    public static JSONArray downloadAllAttachments(JSONArray attachments) throws IOException {
        JSONArray newAttachments = new JSONArray();
        for(int i = 0; i<attachments.length();i++){
            JSONObject attachment = attachments.getJSONObject(i);
            if(!attachment.has("Url")){
                newAttachments.put(attachment);
                continue;
            }
            String downloadUrl = attachment.getString("Url") + "?"+config.FILE_STORAGE_DOWNLOAD_KEY;
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




