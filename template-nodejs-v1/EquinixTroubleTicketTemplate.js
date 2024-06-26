/** EQUINIX MESSAGING GATEWAY TROUBLETICKET TEMPLATE */

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
const messageUtil = require('./util/MessageUtil');

/**
  * Sends the create Trouble Ticket message to Equinix Messaging Gateway.
  *
  * @param requestJSON - Message to send.
  * @param clientID - Equinix issued clientID.
  * @param clientSecret - Equinix issued clientSecret.
  * @returns responseJSON - Received response message
  * @throws error if Equinix Messaging Gateway returns an error while processing the message.
  */
const createTroubleTicket = async (requestJSON, clientID, clientSecret) =>{
    var JSONObj = JSON.parse(requestJSON);
    var responseJSON = await messageUtil.messageProcessor(JSONObj, messageUtil.CREATE_OPERATION, messageUtil.TICKET_TYPE_BREAKFIX, clientID, clientSecret, false);
    return responseJSON;
}

/**
  * Sends the create Trouble Ticket message to Equinix Messaging Gateway.
  *
  * @param requestJSON - Message to send.
  * @param oauthToken - OAuth token used for authentication.
  * @returns responseJSON - Received response message
  * @throws error if Equinix Messaging Gateway returns an error while processing the message.
  */
 const createTroubleTicketUsingOAuth = async (requestJSON, oauthToken) =>{
  var JSONObj = JSON.parse(requestJSON);
  var responseJSON = await messageUtil.messageProcessor(JSONObj, messageUtil.CREATE_OPERATION, messageUtil.TICKET_TYPE_BREAKFIX, null, oauthToken, true);
  return responseJSON;
}

/**
  * Sends the update Trouble Ticket message to Equinix Messaging Gateway.
  *
  * @param requestJSON - Message to send.
  * @param clientID - Equinix issued clientID.
  * @param clientSecret - Equinix issued clientSecret.
  * @returns responseJSON - Received response message
  * @throws error if Equinix Messaging Gateway returns an error while processing the message.
  */
const updateTroubleTicket = async (requestJSON, clientID, clientSecret) =>{
    var JSONObj = JSON.parse(requestJSON);
    var responseJSON = await messageUtil.messageProcessor(JSONObj, messageUtil.UPDATE_OPERATION, messageUtil.TICKET_TYPE_BREAKFIX, clientID, clientSecret, false);
    return responseJSON;
}

/**
  * Sends the update Trouble Ticket message to Equinix Messaging Gateway.
  *
  * @param requestJSON - Message to send.
  * @param oauthToken - OAuth token used for authentication.
  * @returns responseJSON - Received response message
  * @throws error if Equinix Messaging Gateway returns an error while processing the message.
  */
 const updateTroubleTicketUsingOAuth = async (requestJSON, oauthToken) =>{
  var JSONObj = JSON.parse(requestJSON);
  var responseJSON = await messageUtil.messageProcessor(JSONObj, messageUtil.UPDATE_OPERATION, messageUtil.TICKET_TYPE_BREAKFIX, null, oauthToken, true);
  return responseJSON;
}

/**
  * Sends the cancel Trouble Ticket message to Equinix Messaging Gateway.
  *
  * @param requestJSON - Message to send.
  * @param clientID - Equinix issued clientID.
  * @param clientSecret - Equinix issued clientSecret.
  * @returns responseJSON - Received response message
  * @throws error if Equinix Messaging Gateway returns an error while processing the message.
  */
const cancelTroubleTicket = async (requestJSON, clientID, clientSecret) =>{
    var JSONObj = JSON.parse(requestJSON);
    var responseJSON = await messageUtil.messageProcessor(JSONObj, messageUtil.CANCEL_OPERATION, messageUtil.TICKET_TYPE_BREAKFIX, clientID, clientSecret, false);
    return responseJSON;
}

/**
  * Sends the cancel Trouble Ticket message to Equinix Messaging Gateway.
  *
  * @param requestJSON - Message to send.
  * @param oauthToken - OAuth token used for authentication.
  * @returns responseJSON - Received response message
  * @throws error if Equinix Messaging Gateway returns an error while processing the message.
  */
 const cancelTroubleTicketUsingOAuth = async (requestJSON, oauthToken) =>{
  var JSONObj = JSON.parse(requestJSON);
  var responseJSON = await messageUtil.messageProcessor(JSONObj, messageUtil.CANCEL_OPERATION, messageUtil.TICKET_TYPE_BREAKFIX, null, oauthToken, true);
  return responseJSON;
}


 /**
  * Receive ticket notifications from Equinix Messaging Gateway that matches the provided filter criteria.
  *
  * @param requestorId - Customer Reference Number of the Trouble Ticket.
  * @param servicerId – Ticket Number of the Trouble Ticket.
  * @param activityId - Activity Number of the Trouble Ticket.
  * @param ticketState - State of the Trouble Ticket (ex: Open, InProgress, Pending Customer Input, Cancelled, Closed).
  * @returns notificationMsg - Received notification message.
  * @throws error if Equinix Messaging Gateway returns an error while retrieving notification.
  */
const getNotifications = async (requestorId, servicerId, activityId, ticketState) => {
    var filterCriteria = {
        ResourceType : messageUtil.TICKET_TYPE_BREAKFIX,
        RequestorId: requestorId ,
        ServicerId: servicerId ,
        Activity: activityId,
        State: ticketState
    };
    
    var notificationMsg = await messageUtil.readFromQueue(null, filterCriteria);
    if(notificationMsg.Body.Attachments && notificationMsg.Body.Attachments.length > 0){
      notificationMsg.Body.Attachments = await messageUtil.downloadAllAttachments(notificationMsg.Body.Attachments);
    }

    return notificationMsg;
}

module.exports = {
    createTroubleTicket: createTroubleTicket,
    createTroubleTicketUsingOAuth: createTroubleTicketUsingOAuth,
    updateTroubleTicket: updateTroubleTicket,
    updateTroubleTicketUsingOAuth: updateTroubleTicketUsingOAuth,
    cancelTroubleTicket: cancelTroubleTicket,
    cancelTroubleTicketUsingOAuth: cancelTroubleTicketUsingOAuth,
    getNotifications: getNotifications
}