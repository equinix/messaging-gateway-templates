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
const messageUtil = require('./util/MessageUtil');
const HttpStatus = require('http-status-codes');

/**
  * Sends the create WorkVisit message to Equinix Messaging Gateway.
  *
  * @param requestJSON - Message to send.
  * @param clientID - Equinix issued clientID.
  * @param clientSecret - Equinix issued clientSecret.
  * @returns responseJSON - Received response message
  * @throws error if Equinix Messaging Gateway returns an error while processing the message.
  */
const createWorkVisit = async (requestJSON, clientID, clientSecret) => {
  var JSONObj = JSON.parse(requestJSON);
  var responseJSON = await messageUtil.messageProcessor(JSONObj, messageUtil.CREATE_OPERATION, messageUtil.TICKET_TYPE_WORKVISIT, clientID, clientSecret);
  return responseJSON;
}

/**
* Sends the update WorkVisit message to Equinix Messaging Gateway.
*
* @param requestJSON - Message to send.
* @param clientID - Equinix issued clientID.
* @param clientSecret - Equinix issued clientSecret.
* @returns responseJSON - Received response message
* @throws error if Equinix Messaging Gateway returns an error while processing the message.
*/
const updateWorkVisit = async (requestJSON, clientID, clientSecret) => {
  var JSONObj = JSON.parse(requestJSON);
  var responseJSON = await messageUtil.messageProcessor(JSONObj, messageUtil.UPDATE_OPERATION, messageUtil.TICKET_TYPE_WORKVISIT, clientID, clientSecret);
  return responseJSON
}

/**
* Sends the cancel WorkVisit message to Equinix Messaging Gateway.
*
* @param requestJSON - Message to send.
* @param clientID - Equinix issued clientID.
* @param clientSecret - Equinix issued clientSecret.
* @returns responseJSON - Received response message
* @throws error if Equinix Messaging Gateway returns an error while processing the message.
*/
const cancelWorkVisit = async (requestJSON, clientID, clientSecret) => {
  var JSONObj = JSON.parse(requestJSON);
  var responseJSON = await messageUtil.messageProcessor(JSONObj, messageUtil.CANCEL_OPERATION, messageUtil.TICKET_TYPE_WORKVISIT, clientID, clientSecret);
  return responseJSON;
}


/**
  * Sends the create WorkVisit message to Equinix Messaging Gateway as per API Schema.
  *
  * @param requestJSON - Message to send.
  * @param clientID - Equinix issued clientID.
  * @param clientSecret - Equinix issued clientSecret.
  * @returns responseJSON - Received response message
  * @throws error if Equinix Messaging Gateway returns an error while processing the message.
  */
const createWorkVisitExtn = async (requestJSON, clientID, clientSecret) => {
  var jsonObj = JSON.parse(requestJSON);
  var JSONObj = createWorkVisitHelper(JSON.parse(requestJSON));
  var responseJSON = await messageUtil.messageProcessor(JSONObj, messageUtil.CREATE_OPERATION, messageUtil.TICKET_TYPE_WORKVISIT, clientID, clientSecret);
  return processCreateResponse(responseJSON, jsonObj);
}

/**
  * Sends the update WorkVisit message to Equinix Messaging Gateway as per API Schema.
  *
  * @param requestJSON - Message to send.
  * @param clientID - Equinix issued clientID.
  * @param clientSecret - Equinix issued clientSecret.
  * @returns responseJSON - Received response message
  * @throws error if Equinix Messaging Gateway returns an error while processing the message.
  */
const updateWorkVisitExtn = async (requestJSON, clientID, clientSecret) => {
  var JSONObj = updateWorkVisitHelper(JSON.parse(requestJSON));
  var responseJSON = await messageUtil.messageProcessor(JSONObj, messageUtil.UPDATE_OPERATION, messageUtil.TICKET_TYPE_WORKVISIT, clientID, clientSecret);
  return processReponse(responseJSON)
}

/**
  * Sends the cancel WorkVisit message to Equinix Messaging Gateway as per API Schema.
  *
  * @param requestJSON - Message to send.
  * @param clientID - Equinix issued clientID.
  * @param clientSecret - Equinix issued clientSecret.
  * @returns responseJSON - Received response message
  * @throws error if Equinix Messaging Gateway returns an error while processing the message.
  */
const cancelWorkVisitExtn = async (requestJSON, clientID, clientSecret) => {
  var JSONObj = cancelWorkVisitHelper(JSON.parse(requestJSON));
  var responseJSON = await messageUtil.messageProcessor(JSONObj, messageUtil.CANCEL_OPERATION, messageUtil.TICKET_TYPE_WORKVISIT, clientID, clientSecret);
  return processReponse(responseJSON);
}

/**
  * Receive ticket notifications from Equinix Messaging Gateway that matches the provided filter criteria.
  *
  * @param requestorId - Customer Reference Number of the WorkVisit ticket.
  * @param servicerId – Ticket Number of the WorkVisit ticket.
  * @param activityId - Activity Number of the WorkVisit ticket.
  * @param ticketState - State of the WorkVisit ticket (ex: Open, InProgress, Pending Customer Input, Cancelled, Closed).
  * @returns notificationMsg - Received notification message.
  * @throws error if Equinix Messaging Gateway returns an error while retrieving notification.
  */
const getNotifications = async (requestorId, servicerId, activityId, ticketState) => {
  var filterCriteria = {
    ResourceType: messageUtil.TICKET_TYPE_WORKVISIT,
    RequestorId: requestorId,
    ServicerId: servicerId,
    Activity: activityId,
    State: ticketState
  };

  var notificationMsg = await messageUtil.readFromQueue(null, filterCriteria);
  if(notificationMsg.Body.Attachments && notificationMsg.Body.Attachments.length > 0){
    notificationMsg.Body.Attachments = await messageUtil.downloadAllAttachments(notificationMsg.Body.Attachments);
  }

  return notificationMsg;
}

const createWorkVisitHelper = (params) => {
  var vistorArray = []
  var temp = {
    FirstName: "Test FirstName",
    LastName: "Test LastName",
    CompanyName: "Test Company"
  }
  if (params.hasOwnProperty('serviceDetails') && params.serviceDetails.hasOwnProperty('visitors')) {
    for (let visitor of params.serviceDetails.visitors) {
      temp.FirstName = (visitor.hasOwnProperty('firstName')) ? visitor.firstName : undefined,
        temp.LastName = (visitor.hasOwnProperty('lastName')) ? visitor.lastName : undefined,
        temp.CompanyName = (visitor.hasOwnProperty('company')) ? visitor.company : undefined

      vistorArray.push(temp);
    }
  }
  return map_create_workvisit(params, vistorArray);
}

const updateWorkVisitHelper = (params) => {
  return {
    ServicerId: (params.hasOwnProperty('orderNumber'))?params.orderNumber : undefined,
    Attachments: (params.hasOwnProperty('attachments'))?params.attachments : undefined,
    Description: (params.hasOwnProperty('serviceDetails') && params.serviceDetails.hasOwnProperty('additionalDetails'))? params.serviceDetails.additionalDetails : undefined,
    ServiceDetails: {
      StartDateTime: (params.hasOwnProperty('serviceDetails') && params.serviceDetails.hasOwnProperty('startDateTime'))? params.serviceDetails.startDateTime : undefined,
      EndDateTime: (params.hasOwnProperty('serviceDetails') && params.serviceDetails.hasOwnProperty('endDateTime'))? params.serviceDetails.endDateTime : undefined,
      OpenCabinet: (params.hasOwnProperty('serviceDetails') && params.serviceDetails.hasOwnProperty('openCabinet'))?params.serviceDetails.openCabinet : undefined,
      Visitors: (params.hasOwnProperty('serviceDetails') && params.serviceDetails.hasOwnProperty('visitors'))?params.serviceDetails.visitors : undefined
    }
  };
}

const cancelWorkVisitHelper = (params) => {
  return {
    State: "Cancelled",
    RequestorId: (params.hasOwnProperty('customerReferenceNumber'))?params.customerReferenceNumber: undefined,
    ServicerId: (params.hasOwnProperty('orderNumber'))?params.orderNumber: undefined,
    Attachments: (params.hasOwnProperty('attachments'))?params.attachments: undefined,
    Description: (params.hasOwnProperty('cancellationReason'))?params.cancellationReason: undefined,
  };
}

const map_create_workvisit= (params, vistorArray) =>{
  return {
    CustomerContact: (params.contacts[0].hasOwnProperty('userName'))?params.contacts[0].userName: undefined,
    RequestorId: (params.hasOwnProperty('customerReferenceNumber'))?params.customerReferenceNumber: undefined,
    RequestorIdUnique: false,
    Location: (params.hasOwnProperty('ibxLocation')&& params.ibxLocation.hasOwnProperty('cages') && params.ibxLocation.cages[0].hasOwnProperty('cage'))?params.ibxLocation.cages[0].cage: undefined,
    Attachments: (params.hasOwnProperty('attachments'))?params.attachments : undefined,
    Description: (params.hasOwnProperty('serviceDetails') && params.serviceDetails.hasOwnProperty('additionalDetails'))?params.serviceDetails.additionalDetails:undefined,
    ServiceDetails: {
      StartDateTime: (params.serviceDetails.hasOwnProperty('schedule') && params.serviceDetails.schedule.hasOwnProperty('startDateTime'))?params.serviceDetails.schedule.startDateTime: undefined,
      EndDateTime: (params.serviceDetails.hasOwnProperty('schedule') && params.serviceDetails.schedule.hasOwnProperty('endDateTime'))?params.serviceDetails.schedule.endDateTime: undefined,
      OpenCabinet: (params.serviceDetails.hasOwnProperty('openCabinet'))?params.serviceDetails.openCabinet : undefined,
      Visitors: vistorArray
    }
  };
}

function processCreateResponse(responseJSON, jsonObj) {
  if (responseJSON.Body.StatusCode == HttpStatus.CREATED) {
    var res = {
      "successes": [
        {
          "ibxLocation": {
            "ibxTime": null,
            "timezone": null,
            "ibx": null,
            "region": null,
            "address1": null,
            "city": null,
            "state": null,
            "country": null,
            "zipCode": null,
            "cageDetails": [
              {
                "cage": jsonObj.ibxLocation.cages[0].cage,
                "cageUSID": null,
                "systemName": null,
                "accountNumber": null,
                "cabinets": [
                  {
                    "cabinet": null
                  }
                ],
                "notes": [
                  {
                    "noteDescription": null,
                    "noteType": ""
                  }
                ],
                "multiCabinet": false
              }
            ]
          },
          "response": {
            "OrderNumber": responseJSON.Body.ServicerId
          }
        }
      ]
    };
    res.statusCode = responseJSON.Body.StatusCode;
    return res;
  } else {
    if (responseJSON.Body.Description.includes("Processing failed with following error: ")) {

      var res = JSON.parse(responseJSON.Body.Description.replace("Processing failed with following error: ", ""));
      res.statusCode = responseJSON.Body.StatusCode;
      return res;


    } else {
      var res = {
        "errors": [{
          "code": responseJSON.Body.StatusCode,
          "message": responseJSON.Body.Description
        }]
      };
      res.statusCode = responseJSON.Body.StatusCode;
      return res;

    }
  }
}

function processReponse(responseJSON) {
  if (responseJSON.hasOwnProperty('Body') && responseJSON.Body.hasOwnProperty('Description') && responseJSON.Body.hasOwnProperty('StatusCode')) {
    if (responseJSON.Body.StatusCode == HttpStatus.ACCEPTED) {
      var res = {
        "status": "Success",
        "Description": responseJSON.Body.Description,
        "errorCode": "",
        "errorMessage": ""
      };
      res.statusCode = responseJSON.Body.StatusCode;
      return res;
    } else {
      if (responseJSON.Body.Description.includes("Processing failed with following error: ")) {
        return JSON.parse(responseJSON.Body.Description.replace("Processing failed with following error: ", ""));
      } else {
        return {
          "errors": [{
            "code": responseJSON.Body.StatusCode,
            "message": responseJSON.Body.Description
          }]
        }
      }
    }
  }else{
    return {
      "errors": [{
        "code": StatusCodes.BAD_REQUEST,
        "message": "Null Exception"
      }]
    }
  }
}

module.exports = {
  createWorkVisit: createWorkVisit,
  updateWorkVisit: updateWorkVisit,
  cancelWorkVisit: cancelWorkVisit,
  createWorkVisitExtn: createWorkVisitExtn,
  updateWorkVisitExtn: updateWorkVisitExtn,
  cancelWorkVisitExtn: cancelWorkVisitExtn,
  getNotifications: getNotifications
}