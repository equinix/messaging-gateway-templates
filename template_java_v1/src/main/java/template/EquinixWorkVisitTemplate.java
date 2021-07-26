/** EQUINIX MESSAGING GATEWAY WORKVISIT TEMPLATE **/

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

package template;
import org.json.*;
import util.*;

public class EquinixWorkVisitTemplate {

	/**
	 * Sends the create WorkVisit message to Equinix Messaging Gateway.
	 *
	 * @param requestJSON - Message to send.
	 * @param clientID - Equinix issued clientID.
	 * @param clientSecret - Equinix issued clientSecrete
	 * @returns responseJSON - Received response message
	 * @throws Error if Equinix Messaging Gateway returns an error while processing the message.
	 */
	public JSONObject createWorkVisit(JSONObject requestJSON, String clientID, String clientSecret ) throws Exception
	{
		MessageUtil util = new MessageUtil();
		JSONObject responseJSON = util.messageProcessor(requestJSON,MessageUtil.CREATE_OPERATION,MessageUtil.TICKET_TYPE_WORKVISIT,clientID, clientSecret );
		return responseJSON;
	}

	/**
	 * Sends the update WorkVisit message to Equinix Messaging Gateway.
	 *
	 * @param requestJSON - Message to send.
	 * @param clientID - Equinix issued clientID.
	 * @param clientSecret - Equinix issued clientSecret.
	 * @returns responseJSON - Received response message
	 * @throws Error if Equinix Messaging Gateway returns an error while processing the message.
	 */
	public JSONObject updateWorkVisit(JSONObject requestJSON, String clientID, String clientSecret ) throws Exception
	{
		MessageUtil util = new MessageUtil();
		JSONObject responseJSON = util.messageProcessor(requestJSON,MessageUtil.UPDATE_OPERATION,MessageUtil.TICKET_TYPE_WORKVISIT, clientID, clientSecret );
		return responseJSON;
	}

	/**
	 * Sends the cancel WorkVisit message to Equinix Messaging Gateway.
	 *
	 * @param requestJSON - Message to send.
	 * @param clientID - Equinix issued clientID.
	 * @param clientSecret - Equinix issued clientSecret.
	 * @returns responseJSON - Received response message
	 * @throws Error if Equinix Messaging Gateway returns an error while processing the message.
	 */
	public JSONObject cancelWorkVisit(JSONObject requestJSON, String clientID, String clientSecret ) throws Exception
	{
		MessageUtil util = new MessageUtil();
		JSONObject responseJSON = util.messageProcessor(requestJSON,MessageUtil.CANCEL_OPERATION,MessageUtil.TICKET_TYPE_WORKVISIT,clientID, clientSecret );
		return responseJSON;
	}

	/**
	 * Receive ticket notifications from Equinix Messaging Gateway that matches the provided filter criteria.
	 *
	 * @param requestorId - Customer Reference Number of the WorkVisit ticket.
	 * @param servicerId – Ticket Number of the WorkVisit ticket.
	 * @param activityId - Activity Number of the WorkVisit ticket.
	 * @param ticketState - State of the WorkVisit ticket (ex: Open, InProgress, Pending Customer Input, Cancelled, Closed).
	 * @returns notificationMsg - Received notification message.
	 * @throws Error if Equinix Messaging Gateway returns an error while retrieving notification.
	 */
	public JSONObject getNotifications(String requestorId, String servicerId, String activityId, String ticketState ) throws Exception
	{
		MessageUtil util = new MessageUtil();
		JSONObject filterCriteria = new JSONObject("{ResourceType:"+util.TICKET_TYPE_WORKVISIT+",\n" +
				"RequestorId:"+requestorId+",\n" +
				"ServicerId:"+servicerId+",\n" +
				"Activity:"+activityId+",\n" +
				"State:"+ticketState+"\n" +
				"}");
		JSONObject notificationMsg = util.read_messages_from_queue(null ,filterCriteria);
		JSONObject taskObject = new JSONObject(notificationMsg.getString("Task"));
		JSONObject bodyObject = taskObject.getJSONObject("Body");
		notificationMsg.put("Task", taskObject);
		if(!bodyObject.isNull("Attachments") && !bodyObject.getJSONArray("Attachments").isEmpty()){
			JSONArray newAttachments = MessageUtil.downloadAllAttachments(bodyObject.getJSONArray("Attachments"));
			notificationMsg.getJSONObject("Task").getJSONObject("Body").put("Attachments", newAttachments);
		}
		return notificationMsg;
	}

}