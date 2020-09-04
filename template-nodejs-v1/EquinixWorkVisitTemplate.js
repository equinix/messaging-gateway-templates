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

/**
  * Sends the given create WorkVisit message to Equinix Incoming Queue.
  *
  * @param requestJSON - Message to send.
  * @param clientID - Equinix issued clientID.
  * @param clientSecret - Equinix issued clientSecret.
  * @returns serviceBusResponse - Received response message
  * @throws error if the service returns an error while processing message.
  */
const createWorkVisit = async (requestJSON, clientID, clientSecret) => {
  var JSONObj = JSON.parse(requestJSON);
  var serviceBusResponse = await messageUtil.messageProcessor(JSONObj, "Create", "WorkVisit", clientID, clientSecret);
  return serviceBusResponse;
}

/**
* Sends the given update WorkVisit message to Equinix Incoming Queue.
*
* @param requestJSON - Message to send.
* @param clientID - Equinix issued clientID.
* @param clientSecret - Equinix issued clientSecret.
* @returns serviceBusResponse - Received response message
* @throws error if the service returns an error while processing message.
*/
const updateWorkVisit = async (requestJSON, clientID, clientSecret) => {
  var JSONObj = JSON.parse(requestJSON);
  var serviceBusResponse = await messageUtil.messageProcessor(JSONObj, "Update", "WorkVisit", clientID, clientSecret);
  return serviceBusResponse
}

/**
* Sends the given cancel WorkVisit message to Equinix Incoming Queue.
*
* @param requestJSON - Message to send.
* @param clientID - Equinix issued clientID.
* @param clientSecret - Equinix issued clientSecret.
* @returns serviceBusResponse - Received response message
* @throws error if the service returns an error while processing message.
*/
const cancelWorkVisit = async (requestJSON, clientID, clientSecret) => {
  var JSONObj = JSON.parse(requestJSON);
  var serviceBusResponse = await messageUtil.messageProcessor(JSONObj, "Cancelled", "WorkVisit", clientID, clientSecret);
  return serviceBusResponse;
}


/**
  * Sends the given create WorkVisit message to Equinix Incoming Queue as per API Schema.
  *
  * @param requestJSON - Message to send.
  * @param clientID - Equinix issued clientID.
  * @param clientSecret - Equinix issued clientSecret.
  * @returns serviceBusResponse - Received response message
  * @throws error if the service returns an error while processing message.
  */
const createWorkVisitExtn = async (requestJSON, clientID, clientSecret) => {
  var jsonObj = JSON.parse(requestJSON);
  var JSONObj = await createWorkVisitHelper(JSON.parse(requestJSON));
  var serviceBusResponse = await messageUtil.messageProcessor(JSONObj, "Create", "WorkVisit", clientID, clientSecret);
  return processCreateResponse(serviceBusResponse, jsonObj);
}

/**
  * Sends the given update WorkVisit message to Equinix Incoming Queue as per API Schema.
  *
  * @param requestJSON - Message to send.
  * @param clientID - Equinix issued clientID.
  * @param clientSecret - Equinix issued clientSecret.
  * @returns serviceBusResponse - Received response message
  * @throws error if the service returns an error while processing message.
  */
const updateWorkVisitExtn = async (requestJSON, clientID, clientSecret) => {
  var JSONObj = await updateWorkVisitHelper(JSON.parse(requestJSON));
  var serviceBusResponse = await messageUtil.messageProcessor(JSONObj, "Update", "WorkVisit", clientID, clientSecret);
  return processReponse(serviceBusResponse)
}

/**
  * Sends the given cancel WorkVisit message to Equinix Incoming Queue as per API Schema.
  *
  * @param requestJSON - Message to send.
  * @param clientID - Equinix issued clientID.
  * @param clientSecret - Equinix issued clientSecret.
  * @returns serviceBusResponse - Received response message
  * @throws error if the service returns an error while processing message.
  */
const cancelWorkVisitExtn = async (requestJSON, clientID, clientSecret) => {
  var JSONObj = await cancelWorkVisitHelper(JSON.parse(requestJSON));
  var serviceBusResponse = await messageUtil.messageProcessor(JSONObj, "Cancelled", "WorkVisit", clientID, clientSecret);
  return processReponse(serviceBusResponse);
}

/**
  * Receive WorkVisit notification that matches the filter criteria from Equinix Outgoing Queue.
  *
  * @param customerReferenceNumber - Customer Reference Number used for searching WorkVisit order
  * @param servicerId - Order used for searching WorkVisit order
  * @param activityId - Activity ID used for searching WorkVisit Activity
  * @param state - WorkVisit states (eg: Open, InProgress, Cancelled, Closed)
  * @returns queueMsg - Received response message
  * @throws error if the service returns an error while retrieving notification.
  */
const getNotifications = async (customerReferenceNumber, servicerId, activityId, state) => {
  var filterCriteria = {
    ResourceType: 'WorkVisit',
    RequestorId: customerReferenceNumber,
    ServicerId: servicerId,
    Activity: activityId,
    State: state
  };

  var queueMsg = await messageUtil.readFromQueue(null, filterCriteria);
  return queueMsg;
}

const createWorkVisitHelper = (params) => {
  return new Promise((resolve, reject) => {
    var vistorArray = []
    var temp = {
      FirstName: "Test FirstName",
      LastName: "Test LastName",
      CompanyName: "Test Company"
    }
    for (let visitor of params.serviceDetails.visitors) {
      temp.FirstName = visitor.firstName,
        temp.LastName = visitor.lastName,
        temp.CompanyName = visitor.company

      vistorArray.push(temp)
    }
    var response = {
      CustomerContact: params.contacts[0].userName,
      RequestorId: params.customerReferenceNumber,
      RequestorIdUnique: false,
      Location: params.ibxLocation.cages[0].cage,
      Attachments: params.attachments,
      Description: params.serviceDetails.additionalDetails,
      ServiceDetails: {
        StartDateTime: params.serviceDetails.schedule.startDateTime,
        EndDateTime: params.serviceDetails.schedule.endDateTime,
        OpenCabinet: params.serviceDetails.openCabinet,
        Visitors: vistorArray
      }
    };
    resolve(response);
  })
}

const updateWorkVisitHelper = (params) => {
  return new Promise((resolve, reject) => {
    var response = {
      ServicerId: params.orderNumber,
      Attachments: params.attachments,
      Description: params.serviceDetails.additionalDetails,
      ServiceDetails: {
        StartDateTime: params.serviceDetails.startDateTime,
        EndDateTime: params.serviceDetails.endDateTime,
        OpenCabinet: params.serviceDetails.openCabinet,
        Visitors: params.serviceDetails.visitors
      }
    };
    resolve(response);
  })
}

const cancelWorkVisitHelper = (params) => {
  return new Promise((resolve, reject) => {
    var response = {
      State: "Cancelled",
      RequestorId: params.customerReferenceNumber,
      ServicerId: params.orderNumber,
      Attachments: params.attachments,
      Description: params.cancellationReason,
    };
    resolve(response);
  })
}

function processCreateResponse(serviceBusResponse, jsonObj) {
  if (serviceBusResponse.Body.StatusCode == 201) {
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
            "OrderNumber": serviceBusResponse.Body.ServicerId
          }
        }
      ]
    };
    res.statusCode = serviceBusResponse.Body.StatusCode;
    return res;
  } else {
    if (serviceBusResponse.Body.Description.includes("Processing failed with following error: ")) {

      var res = JSON.parse(serviceBusResponse.Body.Description.replace("Processing failed with following error: ", ""));
      res.statusCode = serviceBusResponse.Body.StatusCode;
      return res;


    } else {
      var res = {
        "errors": [{
          "code": serviceBusResponse.Body.StatusCode,
          "message": serviceBusResponse.Body.Description
        }]
      };
      res.statusCode = serviceBusResponse.Body.StatusCode;
      return res;

    }
  }
}

function processReponse(serviceBusResponse) {
  if (serviceBusResponse.Body.StatusCode == 202) {
    var res = {
      "status": "Success",
      "Description": serviceBusResponse.Body.Description,
      "errorCode": "",
      "errorMessage": ""
    };
    res.statusCode = serviceBusResponse.Body.StatusCode;
    return res;
  } else {
    if (serviceBusResponse.Body.Description.includes("Processing failed with following error: ")) {
      return JSON.parse(serviceBusResponse.Body.Description.replace("Processing failed with following error: ", ""));
    } else {
      return {
        "errors": [{
          "code": serviceBusResponse.Body.StatusCode,
          "message": serviceBusResponse.Body.Description
        }]
      }
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