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
import org.json.JSONObject;
import config.*;

import java.time.Duration;
import java.time.ZoneOffset;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.UUID;
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
	public static JSONObject task_obj;

	public JSONObject messageProcessor(JSONObject JSONObj,String actionVerb, String ResourceType, String clientID, String clientSecret) throws Exception
	{
		if (actionVerb.equals("Cancelled")){
			actionVerb = "Update";
		}

		JSONObject messageInput = new JSONObject();
		JSONObject queueMsg = new JSONObject();
		messageInput = createPayload(JSONObj, actionVerb, ResourceType, SOURCE_ID, clientID, clientSecret);
		task_obj = new JSONObject(messageInput.get("Task").toString());
		String messageId = messageInput.getJSONObject("Task").get("Id").toString();
		System.out.println("\n\nMessage ID:   " + messageId +"\n\n");

		ServiceBusBase sbb = new ServiceBusBase();
		try {
			sbb.sendMessageToQueue(messageInput, "IOMA-Message");
		}
		catch (Exception e) {
			processErrorResponse(e.getMessage(),"send", task_obj);
		}
		try {
			return read_messages_from_queue(messageId,null);
		} catch (Exception e) {
			return processErrorResponse(e.getMessage(),"receive", task_obj);
		}

	}

	public JSONObject createPayload(JSONObject JSONObj, String actionVerb, String ResourceType, String SOURCE_ID, String ClientId, String ClientSecret)
	{
		String nowAsISO = ZonedDateTime.now( ZoneOffset.UTC ).format( DateTimeFormatter.ISO_INSTANT );
		UUID uuid=UUID.randomUUID();
		JSONObject parentObject = new JSONObject("{\n" +
				"    \"Task\": {\n" +
				"    \"Id\": \""+uuid+"\",\n" +
				"    \"Body\": "+JSONObj+",\n" +
				"    \"Verb\": \""+actionVerb+"\",\n" +
				"    \"Source\": \""+SOURCE_ID+"\",\n" +
				"    \"Version\": \"1.0\",\n" +
				"    \"Resource\": \""+ResourceType+"\",\n" +
				"    \"ContentType\": \"application/json\",\n" +
				"    \"CreateTimeUTC\": \""+nowAsISO+"\",\n" +
				"    \"OriginationId\": \"\",\n" +
				"    \"OriginationVerb\": \"\"\n" +
				"},\n" +
				"    \"Authentication\": {\n" +
				"    \"ClientId\": \""+ClientId+"\",\n" +
				"    \"ClientSecret\": \""+ClientSecret+"\",\n" +
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
			for(ServiceBusReceivedMessage message : messages){
				if (message == null) {
					return new JSONObject("{ \"Result\" : \"No Messages to Read from Queue\"}");
				}
				else if(filters != null){
					JSONObject json_temp = new JSONObject(message.getBody().toString());
					JSONObject json_obj = new JSONObject(json_temp.get("Task").toString());
					if (json_temp != null) {
						JSONObject body_json_obj =  new JSONObject(json_obj.get("Body").toString());
						List<JSONObject> task_list = new ArrayList<JSONObject>();
						task_list.add(json_obj);
						List<JSONObject> listcom=task_list.stream()
								.filter(!filters.get("ResourceType").equals("null")? json -> filters.get("ResourceType").toString().equalsIgnoreCase(json_obj.get("Resource").toString()): json->true)
								.filter(!filters.get("RequestorId").equals("null")? json -> filters.get("RequestorId").toString().equalsIgnoreCase(body_json_obj.get("RequestorId").toString()): json->true)
								.filter(!filters.get("ServicerId").equals("null")? json -> filters.get("ServicerId").toString().equalsIgnoreCase(body_json_obj.get("ServicerId").toString()): json->true)
								.filter(!filters.get("State").equals("null") ? json -> filters.get("State").toString().equalsIgnoreCase(body_json_obj.get("State").toString()) : json-> true)
								.collect(Collectors.toList());
						if(listcom.size() > 0)
						{
							ret_json_object[0] = json_temp;
							receiver.complete(message);
							return ret_json_object[0];
						}
					}
				} else {
					if(new JSONObject(new JSONObject(message.getBody().toString()).get("Task").toString()).get("OriginationId").toString().equalsIgnoreCase( messageId )){
						ret_json_object[0] = new JSONObject(message.getBody().toString());
						receiver.complete(message);
						return ret_json_object[0];
					}
				}
			}
			receiver.close();
		}
		JSONObject jsonObject = ret_json_object[0] != null ? ret_json_object[0] : new JSONObject("{ \"Result\" : \"No Messages to Read from Queue\"}");
		return jsonObject;
	}

	public static JSONObject formatErrorResponse (String StatusCode,String Description,JSONObject messageInput){
		UUID uuid=UUID.randomUUID();
		JSONObject jsonObject = new JSONObject("{\n" +
				"    \"Id\": \""+uuid+"\",\n" +
				"    \"Body\": {\n" +
				"    \"StatusCode\": \""+StatusCode+"\",\n" +
				"    \"Description\": \""+Description+"\"\n" +
				"},\n" +
				"    \"Verb\": \"Ack\",\n" +
				"    \"Source\": \""+SOURCE_ID+"\",\n" +
				"    \"Version\": \"1.0\",\n" +
				"    \"Resource\": \""+messageInput.get("Resource")+"\",\n" +
				"    \"ContentType\": \""+messageInput.get("ContentType")+"\",\n" +
				"    \"CreateTimeUTC\": \""+messageInput.get("CreateTimeUTC")+"\",\n" +
				"    \"OriginationId\": \"\",\n" +
				"    \"OriginationVerb\": \""+messageInput.get("Verb")+"\"\n" +
				"}\n");
		return jsonObject;
	}

	public static JSONObject processErrorResponse(String errorObj, String mode, JSONObject messageInput)
	{
		String[] errorpair = errorObj.split(",");
		HashMap<String, String> errormap = new HashMap<String, String>();
		for(int i=0;i< errorpair.length;i++) {
			String[] errorTemp = errorpair[i].split(":");
			if(errorTemp.length < 2)
				errormap.put(errorTemp[0].trim(),errorTemp[1].trim());
			else
				errormap.put(errorTemp[0].trim(), errorpair[i].substring(errorTemp[0].length()+1).trim());
		}
		if (errormap.containsKey("status-description"))
		{
			if (mode.equalsIgnoreCase("send")) {
				if (errormap.get("status-description").contains(INVALID_INCOMING_QUEUE_CONNECTION) ||
						errormap.get("status-description").contains(INVALID_TOKEN_SIGNATURE) ||
						errormap.get("status-description").contains(FAILED_ESTABLISH_CONNECTION)) {
					return formatErrorResponse(errormap.get("status-code"), "Error occured while sending message using connection string :"+EQUINIX_INCOMING_QUEUE_CONNECTION_STRING, messageInput);
				} else if (errormap.get("status-description").contains(INVALID_ENTITY)) {
					return formatErrorResponse(errormap.get("status-code"), "Error occured while sending message using queue name : "+EQUINIX_INCOMING_QUEUE, messageInput);
				} else {
					return formatErrorResponse("500", INTERNAL_SERVER_ERROR, messageInput);
				}
			} else if(mode.equalsIgnoreCase("receive")) {
				if (errormap.get("status-description").contains(INVALID_OUTGOING_QUEUE_CONNECTION) ||
						errormap.get("status-description").contains(INVALID_TOKEN_SIGNATURE) ||
						errormap.get("status-description").contains(FAILED_ESTABLISH_CONNECTION)) {
					return formatErrorResponse(errormap.get("status-code"), "Error occured while reading message using connection string :"+EQUINIX_OUTGOING_QUEUE_CONNECTION_STRING, messageInput);
				} else if (errormap.get("status-description").contains(INVALID_ENTITY)) {
					return formatErrorResponse(errormap.get("status-code"), "Error occured while reading message using queue name : "+EQUINIX_OUTGOING_QUEUE, messageInput);
				} else {
					return formatErrorResponse("500", INTERNAL_SERVER_ERROR, messageInput);
				}
			}
		} else {
			return formatErrorResponse("500", errorObj, messageInput);
		}
		return null;
	}
}




