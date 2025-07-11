# Equinix Messaging Gateway Templates &nbsp;&nbsp; ![Deprecated](https://img.shields.io/badge/status-deprecated-red?logo=github)

---

## Order Management Deprecation Notice

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

<table>
  <thead>
    <tr>
      <th>Feature</th>
      <th>Status</th>
      <th>End of Support</th>
      <th>Discontinued</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>EMG Order Management</td>
      <td><strong>Deprecated</strong></td>
      <td>1 April 2025</td>
      <td>1 October 2025</td>
    </tr>
    <tr>
      <td>EMG Outbound Notifications</td>
      <td><strong>Active</strong></td>
      <td>N/A</td>
      <td>N/A</td>
    </tr>
  </tbody>
</table>

---

## 📑 Table of Contents

- [⚠️ Order Management Deprecation Notice](#order-management-deprecation-notice)
- [📦 Overview](#overview)
- [📝 Template Details](#template-details)
- [🔧 Requirements](#requirements)
- [🛠️ Prerequisites](#prerequisites)
- [🚀 How to Run Templates](#how-to-run-templates)
  - [Node.js Templates](#nodejs-templates)
  - [Python Templates](#python-templates)
  - [Java Templates](#java-templates)
- [🎓 Tutorials](#tutorials)
- [Migration Guide](#migration-guide)
  - [Introduction](#introduction)
  - [Alternatives](#alternatives)
  - [SmartHands Migration Guide](#smarthands-migration-guide)
  - [Examples](#working-example)
- [💬 Support](#support)

---

## Overview 

Equinix offers an event-driven system called **Equinix Messaging Gateway (EMG)**.  
The EMG system enables system-to-system integration from your in-house application to Platform Equinix.  

---

**Use EMG to:**

<ul>
  <li>Create, update, cancel orders and receive order status notifications for Equinix Products & Services (Cross Connect, Shipments, SmartHands, Trouble Tickets, Work Visit).</li>
  <li>Receive status notifications on provisioned Equinix Fabric Ports & Virtual Connections.</li>
  <li>Receive notifications for planned/unplanned maintenance at Equinix DataCenters.</li>
  <li>Receive billing notifications when your submitted order is closed and billing is started by Equinix.</li>
</ul>

---

Learn more about Equinix Messaging Gateway by visiting the <a href="https://docs.equinix.com/incidents-notifications/messaging-gateway/integrate-with-messaging-gateway">docs</a>, or watch the <a href="https://youtu.be/RK3b1vO0tuk">EMG Overview Video</a>.

To subscribe to EMG, visit the <a href="https://portal.equinix.com/developer-settings/messaging-gateway">Messaging Gateway Settings</a> page in the Equinix Developer Platform to get started.

---

## Template Details

Equinix Messaging Gateway (EMG) Templates provide reference code to seamlessly integrate with EMG.  
Templates are available in three versions: **Node.js**, **Python**, and **Java**.

---

**Included Templates:**

<ul>
  <li><strong>Order Templates</strong> (create, update, cancel orders):
    <ul>
      <li>/template-nodejs-v1</li>
      <li>/template-python-v1</li>
      <li>/template_java_v1</li>
    </ul>
  </li>
  <li><strong>Notification Templates</strong> (receive notifications from Equinix):
    <ul>
      <li>/template-nodejs-outgoing-notifications-v1</li>
      <li>/template-python-outgoing-notifications-v1</li>
      <li>/template-java-outgoing-notifications-v1</li>
    </ul>
  </li>
  <li><strong>Individual Service Templates</strong>:
    <ul>
      <li>/EquinixCrossConnectTemplate</li>
      <li>/EquinixSmartHandsTemplate</li>
      <li>/EquinixTroubleTicketTemplate</li>
      <li>/EquinixWorkVisitTemplate</li>
      <li>/EquinixShipmentsTemplate</li>
    </ul>
  </li>
  <li><strong>Test Client</strong>: /test/TestClient</li>
  <li><strong>Configuration</strong>: /config/config</li>
</ul>

---

## Requirements

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

## Prerequisites

<ol>
  <li>An active EMG subscription (<a href="https://portal.equinix.com/developer-settings/messaging-gateway">Subscribe here</a>).</li>
  <li>Access to <a href="https://developer.equinix.com/">Equinix Developer Platform</a> and <a href="https://developer.equinix.com/dev-docs/ecp/getting-started/getting-access-token#generating-client-id-and-client-secret">get your access token</a>.</li>
  <li>Authorized permissions by your Master Administrator to order and receive notifications for Equinix Products & Services.</li>
</ol>

---

## How to Run Templates

### Node.js Templates

#### SDK Setup

```sh
npm install
```

- Import the Node.js EMG Template project into Visual Studio Code.
- Install the "Mocha Test Explorer" plugin from VS Code Marketplace.
- Add the following to `.vscode/settings.json`:
  ```json
  {
    "mochaExplorer.files": [
      "test/*.js"
    ],
    "mochaExplorer.logpanel": true
  }
  ```
- Update `/config/config.js` with EMG configurations provided by Equinix.

#### Create/Update/Cancel Orders

- Update `CLIENT_ID` and `CLIENT_SECRET` with your credentials from the Developer Platform.
- Run the intended test in `/test/TestClient` for the desired order operation.
- Update the request packet in each test with your relevant asset values.

#### Receive Notifications

```sh
node EquinixNotificationListener.js
```

---

### Python Templates

#### SDK Setup

```sh
py -3 -m venv .venv
.venv\scripts\activate
pip install azure-servicebus pytest pytest-asyncio
```

- Import the Python EMG Template project into Visual Studio Code.
- Update `/config/config.py` with EMG configurations provided by Equinix.

#### Create/Update/Cancel Orders

- Refer to the same steps as Node.js Templates.

#### Receive Notifications

```sh
python equinix_notification_listener.py
```

---

### Java Templates

#### SDK Setup

```sh
mvn install
```

- Import the Java EMG Template project into your preferred IDE.
- Update `/config/config.java` with EMG configurations provided by Equinix.

#### Create/Update/Cancel Orders

- Refer to the same steps as Node.js Templates.

#### Receive Notifications

- Run:
  ```sh
  mvn install
  ```
- Start the notification listener in your IDE.

---

## Tutorials

<ul>
  <li><a href="https://youtu.be/RK3b1vO0tuk">Create Order through EMG using Node.js Templates</a></li>
  <li><a href="https://youtu.be/iVyYZOUwuag">Create Order through EMG using Python Templates</a></li>
  <li><a href="https://youtu.be/hGNEq4KQ4gA">Receive EMG Network Notifications</a></li>
  <li><a href="https://youtu.be/CdfmjxaSm9U">Receive EMG DataCenter Notifications</a></li>
  <li><a href="https://youtu.be/lvRYIry97fA">Receive EMG Billing Notifications</a></li>
</ul>

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

<table>
  <thead>
    <tr>
      <th>EMG Feature</th>
      <th>Migration to REST APIs</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Supporting Functionalities</strong></td>
      <td>
        <a href="https://docs.equinix.com/api-catalog/ordersv2/">Orders API</a>: Retrieve information on specific orders, such as order status and associated order notes.<br>
        <a href="https://docs.equinix.com/api-catalog/lookupv2/">Lookup API</a>: Retrieve the location of specific service (e.g., Work Visit/Shipment), Patch Panel details and associated port data.<br>
        <a href="https://docs.equinix.com/api-catalog/attachmentsv1/">Attachments API</a>: Upload required documents for your orders.
      </td>
    </tr>
    <tr>
      <td><strong>Inbound/Outbound Shipments</strong></td>
      <td>
        <a href="https://docs.equinix.com/api-catalog/shipmentsv1">Shipments API</a>: Create inbound/outbound shipments, modify your shipment order.<br>
        <a href="https://docs.equinix.com/api-catalog/ordersv2/">Orders API</a>: Cancel your shipment order, add additional notes to your shipment order.
      </td>
    </tr>
    <tr>
      <td><strong>Work Visit</strong></td>
      <td>
        <a href="https://docs.equinix.com/api-catalog/workvisitv1">Work Visit API</a>: Schedule onsite visit, modify your work visit schedule.<br>
        <a href="https://docs.equinix.com/api-catalog/ordersv2/">Orders API</a>: Cancel your work visit, add additional notes to your work visit.
      </td>
    </tr>
    <tr>
      <td><strong>Smart Hands</strong></td>
      <td>
        <a href="https://docs.equinix.com/api-catalog/smarthandsv1">Smart Hands API</a>: Create Smart Hands order.<br>
        <a href="https://docs.equinix.com/api-catalog/ordersv2/">Orders API</a>: Cancel your smart hands order, add additional notes to your smart hands order, view and respond to order negotiations.
      </td>
    </tr>
    <tr>
      <td><strong>Cross Connect</strong></td>
      <td>
        <a href="https://docs.equinix.com/api-catalog/crossconnectsv2">Cross Connect API</a>: Create Cross Connect order, modify Cross Connect.<br>
        <a href="https://docs.equinix.com/api-catalog/ordersv2/">Orders API</a>: Cancel your cross connect order, add additional notes to your cross connect order.
      </td>
    </tr>
  </tbody>
</table>

### SmartHands Migration Guide

EMG supports the following SmartHands types.  
Use the provided operation codes and service attributes in payloads.

<table>
  <thead>
    <tr>
      <th>Smarthands Type</th>
      <th>Description</th>
      <th>Operation</th>
      <th>ECP API Mapping</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Request photos/documentation</td>
      <td>Request cage-related photos or documentation</td>
      <td><code>0000</code></td>
      <td>https://api.equinix.com/v1/orders/smarthands/pictures</td>
    </tr>
    <tr>
      <td>SmartHand Other</td>
      <td>Request a Smart Hands order not listed above</td>
      <td><code>0001</code></td>
      <td>https://api.equinix.com/v1/orders/smarthands/other</td>
    </tr>
    <tr>
      <td>SmartHand Cage Clean up</td>
      <td>Request a cage clean up</td>
      <td><code>0002</code></td>
      <td>https://api.equinix.com/v1/orders/smarthands/cageCleanup</td>
    </tr>
    <tr>
      <td>SmartHand Shipment Unpack</td>
      <td>Unpack inbound shipment and dispose packaging</td>
      <td><code>0003</code></td>
      <td>https://api.equinix.com/v1/orders/smarthands/shipmentUnpack</td>
    </tr>
    <tr>
      <td>SmartHand Cage Escort</td>
      <td>Request IBX security escort</td>
      <td><code>0004</code></td>
      <td>https://api.equinix.com/v1/orders/smarthands/cageEscort</td>
    </tr>
    <tr>
      <td>Equipment Install</td>
      <td>Request equipment installation</td>
      <td><code>0005</code></td>
      <td>https://api.equinix.com/v1/orders/smarthands/equipmentInstall</td>
    </tr>
    <tr>
      <td>Request Cables</td>
      <td>Request cables</td>
      <td><code>0006</code></td>
      <td>https://api.equinix.com/v1/orders/smarthands/cableRequest</td>
    </tr>
    <tr>
      <td>Locate Packages</td>
      <td>Request package location</td>
      <td><code>0007</code></td>
      <td>https://api.equinix.com/v1/orders/smarthands/locatePackage</td>
    </tr>
    <tr>
      <td>Run Patch Cables</td>
      <td>Request cables run between devices</td>
      <td><code>0008</code></td>
      <td>https://api.equinix.com/v1/orders/smarthands/runJumperCable</td>
    </tr>
    <tr>
      <td>Patch Cable Install</td>
      <td>Request patch cable installation</td>
      <td><code>0009</code></td>
      <td>https://api.equinix.com/v1/orders/smarthands/patchCableInstall</td>
    </tr>
    <tr>
      <td>Move Patch Cable</td>
      <td>Move patch cables between devices</td>
      <td><code>0010</code></td>
      <td>https://api.equinix.com/v1/orders/smarthands/moveJumperCable</td>
    </tr>
    <tr>
      <td>Patch Cable Removal</td>
      <td>Remove patch cables</td>
      <td><code>0011</code></td>
      <td>https://api.equinix.com/v1/orders/smarthands/patchCableRemoval</td>
    </tr>
    <tr>
      <td>Large SmartHands Order</td>
      <td>Large cable/equipment requests</td>
      <td><code>0012</code></td>
      <td>https://api.equinix.com/v1/orders/smarthands/largeOrder</td>
    </tr>
  </tbody>
</table>

---

### Working Example

#### How to Get ibxLocation Details

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

#### Update SmartHands

Replying to order negotiations:

```sh
curl --request GET \
  --url https://api.equinix.com/colocations/v2/orders/{orderId}/negotiations \
  --header 'authorization: Bearer REPLACE_BEARER_TOKEN'
```
**Response:**
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

## 💬 Support
For questions, raise an API Support Case or email [api-support@equinix.com](mailto:api-support@equinix.com).
