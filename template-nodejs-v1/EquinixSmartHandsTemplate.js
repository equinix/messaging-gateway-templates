/** EQUINIX MESSAGING GATEWAY SMARTHANDS TEMPLATE **/

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
  * Sends the create SmartHands message to Equinix Messaging Gateway.
  *
  * @param requestJSON - Message to send.
  * @param clientID - Equinix issued clientID.
  * @param clientSecret - Equinix issued clientSecret.
  * @returns responseJSON - Received response message.
  * @throws error if Equinix Messaging Gateway returns an error while processing the message.
  */
const createSmartHands = async (requestJSON, clientID, clientSecret) => {
    var JSONObj = JSON.parse(requestJSON);
    var responseJSON = await messageUtil.messageProcessor(JSONObj, messageUtil.CREATE_OPERATION, messageUtil.TICKET_TYPE_SMARTHANDS, clientID, clientSecret);
    return responseJSON;
}

/**
  * Sends the update SmartHands message to Equinix Messaging Gateway.
  *
  * @param requestJSON - Message to send.
  * @param clientID - Equinix issued clientID.
  * @param clientSecret - Equinix issued clientSecret.
  * @returns responseJSON - Received response message
  * @throws error if Equinix Messaging Gateway returns an error while processing the message.
  */
const updateSmartHands = async (requestJSON, clientID, clientSecret) => {
    var JSONObj = JSON.parse(requestJSON);
    var responseJSON = await messageUtil.messageProcessor(JSONObj, messageUtil.UPDATE_OPERATION, messageUtil.TICKET_TYPE_SMARTHANDS, clientID, clientSecret);
    return responseJSON;
}

/**
  * Sends the cancel SmartHands message to Equinix Messaging Gateway.
  *
  * @param requestJSON - Message to send.
  * @param clientID - Equinix issued clientID.
  * @param clientSecret - Equinix issued clientSecret.
  * @returns responseJSON - Received response message
  * @throws error if Equinix Messaging Gateway returns an error while processing the message.
  */
const cancelSmartHands = async (requestJSON, clientID, clientSecret) => {
    var JSONObj = JSON.parse(requestJSON);
    var responseJSON = await messageUtil.messageProcessor(JSONObj, messageUtil.CANCEL_OPERATION, messageUtil.TICKET_TYPE_SMARTHANDS, clientID, clientSecret);
    return responseJSON;
}

/**
  * Receive ticket notifications from Equinix Messaging Gateway that matches the provided filter criteria.
  *
  * @param requestorId - Customer Reference Number of the SmartHands ticket.
  * @param servicerId – Ticket Number of the SmartHands ticket.
  * @param activityId - Activity Number of the SmartHands ticket.
  * @param ticketState - State of the SmartHands ticket (ex: Open, InProgress, Pending Customer Input, Cancelled, Closed).
  * @returns notificationMsg - Received notification message.
  * @throws error if Equinix Messaging Gateway returns an error while retrieving notification.
  */
const getNotifications = async (requestorId, servicerId, activityId, ticketState) => {
    var filterCriteria = {
        ResourceType: messageUtil.TICKET_TYPE_SMARTHANDS,
        RequestorId: requestorId,
        ServicerId: servicerId,
        Activity: activityId,
        State: ticketState
    };

    var notificationMsg = await messageUtil.readFromQueue(null, filterCriteria);
    return notificationMsg;
}


module.exports = {
    createSmartHands: createSmartHands,
    updateSmartHands: updateSmartHands,
    cancelSmartHands: cancelSmartHands,
    getNotifications: getNotifications
}