# Equinix Messaging Gateway Templates &nbsp;&nbsp; ![Deprecated](https://img.shields.io/badge/status-deprecated-red?logo=github)

---

## Order Management Deprecation Notice
> [!NOTE]
> **Deprecation Notice**  
> The following Equinix Messaging Gateway features are being deprecated or removed.  
> Please review the status and important dates below:
>
> - After **1 April 2025**, EMG Order Management will continue to work, but will not be supported.
> - After **1 October 2025**, orders placed via EMG will not process.
> - EMG outbound notifications are not impacted.
>
> For migration guidance, see our [migration guide](#migration-guide) and REST APIs.  
> For questions, raise an API Support Case or email [api-support@equinix.com](mailto:api-support@equinix.com).

| Feature                    | Status      | End of Support | Discontinued      |
|----------------------------|-------------|----------------|-------------------|
| EMG Order Management       | **Deprecated**  | 1 April 2025   | 1 October 2025    |
| EMG Outbound Notifications | **Active**      | N/A            | N/A               |

---

## 📑 Table of Contents

- [Order Management Deprecation Notice](#order-management-deprecation-notice)
- [Overview](#📦overview)
- [Template Details](#📝template-details)
- [Requirements](#🔧requirements)
- [Prerequisites](#🛠️prerequisites)
- [How to Run Templates](#🚀how-to-run-templates)
  - [Node.js Templates](#nodejs-templates)
  - [Python Templates](#python-templates)
  - [Java Templates](#java-templates)
- [Tutorials](#🎓tutorials)
- [Migration Guide](#migration-guide)
  - [Introduction](#introduction)
  - [Alternatives](#alternatives)
  - [SmartHands Migration Guide](#smarthands-migration-guide)
  - [Examples](#working-example)
- [Support](#💬support)

---

## 📦Overview 

Equinix offers an event-driven system called **Equinix Messaging Gateway (EMG)**.  
The EMG system enables system-to-system integration from your in-house application to Platform Equinix.  

---

**Use EMG to:**

- Create, update, cancel orders and receive order status notifications for Equinix Products & Services (Cross Connect, Shipments, SmartHands, Trouble Tickets, Work Visit).
- Receive status notifications on provisioned Equinix Fabric Ports & Virtual Connections.
- Receive notifications for planned/unplanned maintenance at Equinix DataCenters.
- Receive billing notifications when your submitted order is closed and billing is started by Equinix.

---

Learn more about Equinix Messaging Gateway by visiting the [docs](https://docs.equinix.com/incidents-notifications/messaging-gateway/integrate-with-messaging-gateway), or watch the [EMG Overview Video](https://youtu.be/9netRhONlRg).

To subscribe to EMG, visit the [Messaging Gateway Settings](https://portal.equinix.com/developer-settings/messaging-gateway) page in the Equinix Developer Platform to get started. Watch this [video](https://youtu.be/jGYTi3Bn5YM) for the step-by-step guide on how to subscribe. Alternatively, you can also reach out to your Equinix Customer Success Manager.

---

## 📝Template Details

Equinix Messaging Gateway (EMG) Templates provide reference code to seamlessly integrate with EMG.
Templates are available in three versions: **Node.js**, **Python**, and **Java**.
You can refer, use, modify & extend EMG Templates based on your architecture & security policies.

---

**Included Templates:**

- **Order Templates** (create, update, cancel orders):
  - `/template-nodejs-v1`
  - `/template-python-v1`
  - `/template_java_v1`
- **Notification Templates** (receive notifications from Equinix):
  - `/template-nodejs-outgoing-notifications-v1`
  - `/template-python-outgoing-notifications-v1`
  - `/template-java-outgoing-notifications-v1`
- **Individual Service Templates**:
  - `/EquinixCrossConnectTemplate`
  - `/EquinixSmartHandsTemplate`
  - `/EquinixTroubleTicketTemplate`
  - `/EquinixWorkVisitTemplate`
  - `/EquinixShipmentsTemplate`
- **Test Client**: `/test/TestClient`
- **Configuration**: `/config/config`

---

## 🔧Requirements

### Node.js Templates &nbsp;![Node.js](https://img.shields.io/badge/Node.js-v10.16.2%2B-green?logo=node.js)
- [Node.js v10.16.2+](https://nodejs.org/en/download/)
- [Visual Studio Code](https://code.visualstudio.com/)

### Python Templates &nbsp;![Python](https://img.shields.io/badge/Python-v3.8.5%2B-blue?logo=python)
- [Python v3.8.5+](https://www.python.org/downloads/)
- [Azure SDK for Python v0.50.3+](https://azuresdkdocs.blob.core.windows.net/%24web/python/azure-servicebus/0.50.3/index.html)
- [pytest v6.0.1+](https://docs.pytest.org/en/stable/getting-started.html)
- [pytest-asyncio v0.14.0+](https://pypi.org/project/pytest-asyncio/)

### Java Templates &nbsp;![Java](https://img.shields.io/badge/Java-8%2B-orange?logo=java)
- Java 8 or above
- IntelliJ IDEA or Eclipse IDE

---

## 🛠️Prerequisites

1. An active EMG subscription ([Subscribe here](https://portal.equinix.com/developer-settings/messaging-gateway)).
2. Access to [Equinix Developer Platform](https://developer.equinix.com/) and [get your access token](https://developer.equinix.com/dev-docs/ecp/getting-started/getting-access-token#generating-client-id-and-client-secret).
3. Authorized permissions by your Master Administrator to order and receive notifications for Equinix Products & Services.

---

## 🚀How to Run Templates

### Node.js Templates
- Download & import the Node.JS EMG Template project to Visual Code.
- Run `npm install` from the root directory to install azure-bus package and other dependent libraries as per “_package.json_”.
- Search & Install “_Mocha Test Explorer_” plugin from Visual Code Marketplace.
- Select the EMG template project in Visual Code & click on Debug icon.
- When promoted, click on “_create a launch.json file_” and select “_Node.js_”. This will create “_.vscode_” folder.
- Right click on “_.vscode_” folder, create a new file call “_settings.json_” & insert below lines into the newly created file.
    ```sh
    {
      "mochaExplorer.files": [
          "test/*.js"
      ],
      "mochaExplorer.logpanel": true
    }
    ```
- Update _/config/config.js_ with EMG configurations (queues connection string etc.) provided by Equinix when you subscribe to EMG. Copy the YAML from your EMG subscription details on Equinix Developer Platform & override the place holders provide in the config file.
- Save all the files & restart Visual Code editor

#### Create/Update/Cancel Orders
- Update values of `CLIENT_ID` and `CLIENT_SECRET` with Consumer Key & Consumer Secret generated by you while subscribing to EMG through Equinix Developer Platform.
- Navigate to test/TestClient and run intended test for intended order operation for supported Equinix Product & Services.  
- You would need to update the request packet for each test with applicable values based on your Assets & presence within Equinix. Visit How To Guide to know about EMG request & response schemas for supported Equinix Products & Services
- On successful processing of the  of the Equinix order, output will be displayed on the Visual Code console. (Toggle to Test Explorer view)
- After creating an order, take note of the ServicerId displayed in the console, and replace the ORDER_NUMBER constant in TestClient to successfully run the test for update & cancel order operations.

#### Receive Notifications
- Download & import the Node.JS EMG Template project (/template-nodejs-outgoing-notifications-v1) to Visual Code.
- Update _/config/config.js_ with EMG configurations (queues connection string etc.) provided by Equinix when you subscribe to EMG. Copy the YAML from your EMG subscription details on Equinix Developer Platform & override the place holders provide in the config file.
- Save all the files & restart Visual Code editor
- Run `npm install` from the root directory to install azure-bus package and other dependent libraries as per “_package.json_”.
- Now open the Terminal window of Visual Code and execute the below command on the root location:
  - `node EquinixNotificationListener.js`
-	Above command would spin an indefinite listener on customer’s queue where messages would be received instantly whenever any new notification message pushed to the queue from Equinix. 

---

### Python Templates

#### SDK Setup

- Download & import the Python EMG Template project to Visual Code.
- Setting up environment
- Execute below command on the terminal to create a new virtual environment. 
    - `py -3 -m venv .venv`
- Activate the new virtual environment using the below command 
    - `.venv\scripts\activate`
- Install Azure Service Bus Package
    ```sh
    pip install azure-servicebus
    ```
- Install pytest framework to run Test Client:
    ```sh
    pip install pytest
    
    pip install pytest-asyncio
    ```
- Update _/config/config.py_ with EMG configurations (queues connection string etc.) provided by Equinix when you subscribe to EMG. Copy the YAML from your EMG subscription details on Equinix Developer Platform & override the place holders provide in the config file.

#### Create/Update/Cancel Orders

- Refer to the same steps as Node.js Templates.

#### Receive Notifications

- Download & import the Python EMG Template project (template-python-outgoing-notifications-v1) to Visual Code. 
- Install Azure Service Bus Package
  ```sh
  pip install azure-servicebus
  ```
- Install pytest framework to run Test Client:
  ```sh
  pip install pytest
  
  pip install pytest-asyncio
  ```
- Update _/config/config.py_ with EMG configurations (queues connection string etc.) provided by Equinix when you subscribe to EMG. Copy the YAML from your EMG subscription details on Equinix Developer Platform & override the place holders provide in the config file.
- Now open the Terminal window of Visual Code and execute the below command on the root location
  - `python equinix_notification_listener.py`
- Above command would spin an indefinite listener on customer’s queue where messages would be received instantly whenever any new notification message pushed to the queue from Equinix

---

### Java Templates

#### SDK Setup
- Download and import the Java Template project into the Java IDE of your choice - Intellij IDEA or Eclipse IDE
- Run the below script from with the parent folder _\template_java_v1_
    - `mvn install`
- Ensure all the dependent libraries are successful installed under ‘External Libraries’ of your project.
- Update _/config/config.java_ with EMG configurations (queues connection string etc.) provided by Equinix when you subscribe to EMG. Copy the YAML from your EMG subscription details on Equinix Developer Platform & override the placeholders provide in the config file.

#### Create/Update/Cancel Orders

- Refer to the same steps as Node.js Templates.

#### Receive Notifications

- Download and import the Java Template project (template-java-outgoing-notifications-v1)  into the Java IDE of your choice - Intellij IDEA or Eclipse IDE
- Run the below script from with the parent folder _\template-java-outgoing-notifications-v1_  
    - `mvn install`
- Ensure all the dependent libraries are successfully installed under ‘External Libraries’ of your project.
- Update _/config/config.java_ with EMG configurations (queues connection string etc.) provided by Equinix when you subscribe to EMG. Copy the YAML from your EMG subscription details on Equinix Developer Platform & override the place holders provide in the config file.
- Now click on the Debug icon next to “_EquinixNotificationListener_” drop down. 
- This would open a new terminal and spin an indefinite listener on customer’s queue where messages would be received instantly whenever any new notification message pushed to the queue from Equinix.

---

## 🎓Tutorials

- [Create Order through EMG using Node.js Templates](https://youtu.be/RK3b1vO0tuk)
- [Create Order through EMG using Python Templates](https://youtu.be/iVyYZOUwuag)
- [Receive EMG Network Notifications](https://youtu.be/hGNEq4KQ4gA)
- [Receive EMG DataCenter Notifications](https://youtu.be/CdfmjxaSm9U)
- [Receive EMG Billing Notifications](https://youtu.be/lvRYIry97fA)

---

## Migration Guide

### Introduction

This guide helps you migrate from EMG Order Management to REST APIs.  
**Important Dates:**  
- Deprecation Start Date: October 1, 2024  
- End of Support Date: April 1, 2025  
- End of Life: October 1, 2025

#### Deprecation

EMG Order Management API services are deprecated.  
While existing features may still work, they will not receive updates or bug fixes.  
Please migrate to the recommended REST APIs.

---

### Alternatives

| EMG Feature             | Migration to REST APIs                                                                                                                                                                                   |
|-------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Supporting Functionalities** | [Orders API](https://docs.equinix.com/api-catalog/ordersv2/): Retrieve information on specific orders, such as order status and associated order notes.<br>[Lookup API](https://docs.equinix.com/api-catalog/lookupv2/): Retrieve the location of specific service (e.g., Work Visit/Shipment), Patch Panel details and associated port data.<br>[Attachments API](https://docs.equinix.com/api-catalog/attachmentsv1/): Upload required documents for your orders. |
| **Inbound/Outbound Shipments** | [Shipments API](https://docs.equinix.com/api-catalog/shipmentsv1): Create inbound/outbound shipments, modify your shipment order.<br>[Orders API](https://docs.equinix.com/api-catalog/ordersv2/): Cancel your shipment order, add additional notes to your shipment order. |
| **Work Visit**             | [Work Visit API](https://docs.equinix.com/api-catalog/workvisitv1): Schedule onsite visit, modify your work visit schedule.<br>[Orders API](https://docs.equinix.com/api-catalog/ordersv2/): Cancel your work visit, add additional notes to your work visit. |
| **Smart Hands**            | [Smart Hands API](https://docs.equinix.com/api-catalog/smarthandsv1): Create Smart Hands order.<br>[Orders API](https://docs.equinix.com/api-catalog/ordersv2/): Cancel your smart hands order, add additional notes to your smart hands order, view and respond to order negotiations. |
| **Cross Connect**          | [Cross Connect API](https://docs.equinix.com/api-catalog/crossconnectsv2): Create Cross Connect order, modify Cross Connect.<br>[Orders API](https://docs.equinix.com/api-catalog/ordersv2/): Cancel your cross connect order, add additional notes to your cross connect order. |

### SmartHands Migration Guide

EMG supports the following SmartHands types.  
Use the provided operation codes and service attributes in payloads.

| Smarthands Type             | Description                           | Operation | ECP API Mapping                                         |
|-----------------------------|---------------------------------------|-----------|---------------------------------------------------------|
| Request photos/documentation| Request cage-related photos or documentation | `0000`      | https://api.equinix.com/v1/orders/smarthands/pictures   |
| SmartHand Other             | Request a Smart Hands order not listed above | `0001`      | https://api.equinix.com/v1/orders/smarthands/other      |
| SmartHand Cage Clean up     | Request a cage clean up               | `0002`      | https://api.equinix.com/v1/orders/smarthands/cageCleanup|
| SmartHand Shipment Unpack   | Unpack inbound shipment and dispose packaging | `0003`      | https://api.equinix.com/v1/orders/smarthands/shipmentUnpack|
| SmartHand Cage Escort       | Request IBX security escort           | `0004`      | https://api.equinix.com/v1/orders/smarthands/cageEscort |
| Equipment Install           | Request equipment installation        | `0005`      | https://api.equinix.com/v1/orders/smarthands/equipmentInstall|
| Request Cables              | Request cables                        | `0006`      | https://api.equinix.com/v1/orders/smarthands/cableRequest|
| Locate Packages             | Request package location              | `0007`      | https://api.equinix.com/v1/orders/smarthands/locatePackage|
| Run Patch Cables            | Request cables run between devices    | `0008`      | https://api.equinix.com/v1/orders/smarthands/runJumperCable|
| Patch Cable Install         | Request patch cable installation      | `0009`      | https://api.equinix.com/v1/orders/smarthands/patchCableInstall|
| Move Patch Cable            | Move patch cables between devices     | `0010`      | https://api.equinix.com/v1/orders/smarthands/moveJumperCable|
| Patch Cable Removal         | Remove patch cables                   | `0011`      | https://api.equinix.com/v1/orders/smarthands/patchCableRemoval|
| Large SmartHands Order      | Large cable/equipment requests        | `0012`      | https://api.equinix.com/v1/orders/smarthands/largeOrder |

---

### Working Example

#### How to Get ibxLocation Details
 • We could obtain ibx, cage, cabinet, account number using the below curl request, and fill into respective fields in ibxLocation.

```sh
curl --request GET \
  --url 'https://api.equinix.com/v1/orders/smarthands/locations?detail=false&ibxs=SOME_STRING_VALUE&cages=SOME_STRING_VALUE' \
  --header 'accept: application/json' \
  --header 'authorization: SOME_STRING_VALUE' \
  --header 'content-type: application/json'
```
**Response:**
```json
{
  "locations": [
    {
      "ibx": "AM1",
      "cages": [
        {
          "cage": "LD5:01:001MC3",
          "cageTypes": "Shared",
          "accounts": [
            {
              "number": "136008",
              "name": "Service Corporation",
              "isCreditHold": "false",
              "isPOBearing": "false",
              "cabinets": [
                {
                  "cabinet": "LD5:01:001MC3:0718",
                  "cabinetType": "string"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

#### How to Get Attachment ID
• We could upload the attachment via attachment API to obtain the attachment name & attachmentId.

```sh
curl --request POST \
  --url 'https://api.equinix.com/v1/attachments/file?purpose=SOME_STRING_VALUE' \
  --header 'accept: multipart/form-data' \
  --header 'authorization: SOME_STRING_VALUE' \
  --header 'content-type: multipart/form-data; boundary=---011000010111000001101001' \
  --form uploadFile=SOME_FILE_VALUE
```
**Response:**
```json
{
  "attachmentId": "56d10de6-f2c0-4edd-ba29-b70736aa2093",
  "attachmentName": "Example_Invoice.xlsx",
  "attachmentType": "xlsx",
  "attachmentSize": 259387,
  "createdDate": "2017-01-31T09:03:08.340Z",
  "createdBy": "john.doe@example.com",
  "lastUpdatedDate": "2017-04-06T17:10:44.807Z"
}
```

#### SmartHands Creation Example
**Endpoint:**  
`POST https://api.equinix.com/v1/orders/smarthands/other`

- The order number will be available in the `201 Created` response once successfully created.
- The mapping of EMG field values to API fields is described in “<>”.

```json
{
  "customerReferenceNumber": "RSS41244 <Task.RequestorId>",
  "ibxLocation": {
    "ibx": "AM1",
    "cages": [
      {
        "cage": "AM1:01:001MC3",
        "accountNumber": "12345",
        "cabinets": [
          "AM1:01:001MC3:0102"
        ]
      }
    ]
  },
  "contacts": [
    {
      "contactType": "ORDERING",
      "userName": "jondoe@test.com<Task.Body.CustomerContact>"
    },
    {
      "contactType": "NOTIFICATION",
      "userName": "jondoe@test.com< Task.Body.CustomerContact>"
    },
    {
      "contactType": "TECHNICAL",
      "name": "John Doe",
      "workPhone": "1111111",
      "workPhonePrefToCall": "ANYTIME",
      "mobilePhone": "1111111",
      "mobilePhonePrefToCall": "ANYTIME"
    }
  ],
  "schedule": {
    "scheduleType": "STANDARD",
    "requestedStartDate": "2017-04-05T12:00:00Z <RequestedStartDate>",
    "requestedCompletionDate": "2017-04-05T12:00:00Z <RequestedCompletionDate>"
  },
  "attachments": [
    {
      "id": "eb9ab7e9-3785-41e4-af24-112dff <attachmentId>",
      "name": "eb9ab7e9-3785-41e4-af24-asfsa5424 <attachmentName>"
    }
  ],
  "serviceDetails": {
    "scopeOfWork": "Scope of work<Task.Body.Description>"
  }
}
```
**Success Response:**
```json
{
    "OrderNumber": "1-190986534844"
}
```
---

## Schedule Types for Additional Notes

There are **3 types** of `scheduleType`:

1. **STANDARD**  
   - EMG defaults to standard when both `requestedStartDate` & `requestedCompletionDate` are null.
   - Standard turnaround time pending install base readiness.
   - Most requests are processed within 24 to 72 hours.
   - Requests are processed first come, first served unless expedited.
   - `requestedStartDate` and `requestedCompletionDate` are ignored for standard scheduling.

2. **EXPEDITED**  
   - EMG fills this type when `requestedCompletionDate` is >2hr and within 24 hrs from IBX time.
   - Equinix prioritizes your request and attempts to fulfill ASAP.
   - **Additional fees may apply.**
   - `requestedCompletionDate` is mandatory; `requestedStartDate` is ignored.

3. **SCHEDULED_MAINTENANCE**  
   - Schedule a request for a specific date and time, including today.
   - Both `requestedStartDate` and `requestedCompletionDate` are mandatory.

---

## Updating Smart Hands

Responding to 1Way & 2Way Notes, with `ServicerId` in EMG payload as the `orderId`.  
User can retrieve attachments using the attachment API as shown:

```bash
curl --request POST \
  --url https://api.equinix.com/colocations/v2/orders/{orderId}/notes \
  --header 'authorization: Bearer REPLACE_BEARER_TOKEN' \
  --header 'content-type: application/json' \
  --data '{
    "referenceId":"{orderId}",
    "text":"The text of the note",
    "attachments":[{"id":"c77c5f58-a7ea-4e88-9fc4-1a2900027425","name":"error-log"}]
  }'
```

**Example Payload:**

```json
{
  "text": "problem description <Task.Description>",
  "attachments": [
    {
      "id": "abae6f8c-e168-11ea-87d0-0242ac130003 <attachmentId>",
      "name": "problem_attachments <attachmentName>"
    }
  ]
}
```

## Steps to Reply to Order Negotiations

EMG provides a 1-step process to respond to order negotiation, requiring two API calls:

### 1. Get the `referenceId` to respond (replace `orderId` with `ServiceId`):

```bash
curl --request GET \
  --url https://api.equinix.com/colocations/v2/orders/{orderId}/negotiations \
  --header 'authorization: Bearer REPLACE_BEARER_TOKEN'
```

**Response Example:**
```json
[
  {
    "referenceId": "4-12312312132",
    "orderRequestedDateTime": "2020-08-25T10:24:10.282Z",
    "proposedDateTime": "2020-08-25T11:24:10.282Z",
    "expirationDateTime": "2020-08-25T09:24:10.282Z",
    "expedited": false,
    "createdDateTime": "2020-08-25T06:24:10.282Z",
    "message": "Due to multiple request, unable to process with requested time"
  }
]
```

### 2. Reply to Order Negotiation

Attach the `referenceId` from the first step and use the same EMG `servicerId` for the `orderId`:

Reply to negotiation:

```sh
curl --request POST \
  --url https://api.equinix.com/colocations/v2/orders/{orderId}/negotiations \
  --header 'authorization: Bearer REPLACE_BEARER_TOKEN' \
  --header 'content-type: application/json' \
  --data '{"referenceId":"4-9091830","action":"APPROVE","reason":"Cancelling the new time"}'
```
Enum: `"APPROVE"`, `"APPROVE_NON_EXPEDITE"`, `"CANCEL"`

---
## Cancelling Smart Hands

Using the `servicerId` for the `orderId` and the description for the reason, call the below API to cancel the order:

```bash
curl --request POST \
  --url https://api.equinix.com/colocations/v2/orders/{orderId}/cancel \
  --header 'authorization: Bearer REPLACE_BEARER_TOKEN' \
  --header 'content-type: application/json' \
  --data '{
    "reason":"string",
    "attachments":[{"id":"c77c5f58-a7ea-4e88-9fc4-1a2900027425","name":"error-log"}],
    "lineIds":["1-D89731S"]
  }'
```
## 💬Support
For questions, raise an API Support Case or email [api-support@equinix.com](mailto:api-support@equinix.com)
