# Templates for Equinix Messaging Gateway

<a name="Order-Management-Deprecation-Notice"/>

> [!NOTE]
> **Deprecation Notice**
>
> The following Equinix Messaging Gateway features are being deprecated or removed.  
> Please review the status and important dates below:
>
> | Feature                      | Status      | End of Support     | Discontinued         |
> |------------------------------|-------------|--------------------|----------------------|
> | EMG Order Management         | Deprecated  | 1 April 2025       | 1 October 2025       |
> | EMG Outbound Notifications   | Active      | N/A                | N/A                  |
>
> - After 1 April 2025, EMG Order Management will continue to work, but will not be supported.
> - After 1 October 2025, orders placed via EMG will not process.
> - EMG outbound notifications are not impacted.
>
> For migration guidance, see our [migration guide](https://developer.equinix.com/dev-docs/emg/order-management/migration-guide) and REST APIs.
> For questions, raise an API Support Case or email <api-support@equinix.com>.

Equinix offers an event-driven system called **_Equinix Messaging Gateway (EMG)_**. The EMG system enables system-to-system integration from your in-house application to Platform Equinix. Use EMG to:
-	Create/update/cancel orders & receive order status notifications for subscribed Equinix Products & Services - Cross Connect, Shipments, SmartHands, Trouble Tickets, Work Visit.
-	Receive status notifications on provisioned Equinix Fabric Ports & Virtual Connections 
-	Receive notifications for planned/unplanned maintenance at Equinix DataCenters
-	Billing Notifications when your submitted order is closed & billing is started by Equinix 

Learn more about Equinix Messaging Gateway by visiting this [link](https://docs.equinix.com/incidents-notifications/messaging-gateway/integrate-with-messaging-gateway), or you can watch the EMG Overview video [here](https://youtu.be/9netRhONlRg).

To subscribe to EMG, visit the [Messaging Gateway Settings](https://portal.equinix.com/developer-settings/messaging-gateway) page in the Equinix Developer Platform to get started. Watch this [video](https://youtu.be/jGYTi3Bn5YM) for the step-by-step guide on how to subscribe. Alternatively, you can also reach out to your Equinix Customer Success Manager.

Equinix Messaging Gateway (EMG) Templates provide reference code to seamlessly integrate with EMG. These Templates are available in three versions – Node.js, Python and Java. You can refer, use, modify & extend EMG Templates based on your architecture & security policies.   

---

## Template Details

The Templates includes:

1.  Order Templates with sample code for order management - create, update & cancel orders with Equinix:
    - `/template-nodejs-v1`
    - `/template-python-v1`
    - `/template_java_v1`

2.  Notification Templates with sample code to receive notifications from Equinix:
    - `/template-nodejs-outgoing-notifications-v1`
    - `/template-python-outgoing-notifications-v1`
    - `/template-java-outgoing-notifications-v1`

3.  Order Templates includes individual templates with sample code to create/update/cancel Equinix orders for supported Equinix Orders & Services:
    - `/EquinixCrossConnectTemplate`
    - `/EquinixSmartHandsTemplate`
    - `/EquinixTroubleTicketTemplate`
    - `/EquinixWorkVisitTemplate`
    - `/EquinixShipmentsTemplate`

4.  Order Templates also includes TestClient with sample code on how to send request & receive response from EMG Templates using EMG message schemas. Visit How To Guide to know about EMG request & response schemas for supported Equinix Products & Services
    - `/test/TestClient`

5.  Configurations for EMG queues. These configurations will be provided by Equinix when you subscribe to EMG. Copy the YAML from your EMG subscription details on Equinix Developer Platform & override the place holders provide in config file at below location:
    - `/config/config`

## Requirements

1.  Node.js Templates
    - [Node.js](https://nodejs.org/en/download/) v10.16.2+
    - [Visual Studio Code](https://code.visualstudio.com/)

2.  Python Templates:
    - [Python](https://www.python.org/downloads/) - v3.8.5+
    - [Azure SDK for Python](https://azuresdkdocs.blob.core.windows.net/%24web/python/azure-servicebus/0.50.3/index.html) - v0.50.3+
    - [pytest](https://docs.pytest.org/en/stable/getting-started.html) - v6.0.1+
    - [pytest-asyncio](https://pypi.org/project/pytest-asyncio/) - v0.14.0+

3.  Java Templates
    - Java 8 & above
    - IntelliJ IDEA or Eclipse IDE

## Prerequisites

1. An existing subscription with EMG is required in order to use our Templates. Visit the [Subscriptions](https://developer.equinix.com/subscriptions) page in the Equinix Developer Platform to get started. Alternatively, you can also reach out to your Equinix Customer Success Manager.
2. Visit [Equinix Developer Platform](https://developer.equinix.com/) & follow the [steps](https://developer.equinix.com/dev-docs/ecp/getting-started/getting-access-token#generating-client-id-and-client-secret) to generate Equinix Client ID and Client Secret keys.
3. You must have authorized permissions by your Master Administrator to order and receive notifications for Equinix Products & Services.

## How to Run EMG Templates

1.  Node.js Templates:
    1.  SDK Setup:
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
    2. Create/Update/Cancel Orders through EMG for supported Equinix Product & Services.  
        - Update values of `CLIENT_ID` and `CLIENT_SECRET` with Consumer Key & Consumer Secret generated by you while subscribing to EMG through Equinix Developer Platform.
        - Navigate to test/TestClient and run intended test for intended order operation for supported Equinix Product & Services.  
        - You would need to update the request packet for each test with applicable values based on your Assets & presence within Equinix. Visit How To Guide to know about EMG request & response schemas for supported Equinix Products & Services
        - On successful processing of the  of the Equinix order, output will be displayed on the Visual Code console. (Toggle to Test Explorer view)
        - After creating an order, take note of the ServicerId displayed in the console, and replace the ORDER_NUMBER constant in TestClient to successfully run the test for update & cancel order operations.
    3. Receive Notifications from EMG:
        - Download & import the Node.JS EMG Template project (/template-nodejs-outgoing-notifications-v1) to Visual Code.
        - Update _/config/config.js_ with EMG configurations (queues connection string etc.) provided by Equinix when you subscribe to EMG. Copy the YAML from your EMG subscription details on Equinix Developer Platform & override the place holders provide in the config file.
        - Save all the files & restart Visual Code editor
        - Run `npm install` from the root directory to install azure-bus package and other dependent libraries as per “_package.json_”.
        - Now open the Terminal window of Visual Code and execute the below command on the root location:
            - `node EquinixNotificationListener.js`
        -	Above command would spin an indefinite listener on customer’s queue where messages would be received instantly whenever any new notification message pushed to the queue from Equinix. 

2.  Python Templates:
    1.  SDK Setup:
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

    2. Create/Update/Cancel Orders through EMG for supported Equinix Product & Services.
        - *(Refer to the same section in Node.js Templates)*

    3. Receive Notifications from EMG:
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

3.  Java Templates
    1.  SDK Setup:
        - Download and import the Java Template project into the Java IDE of your choice - Intellij IDEA or Eclipse IDE
        - Run the below script from with the parent folder _\template_java_v1_
            - `mvn install`
        - Ensure all the dependent libraries are successful installed under ‘External Libraries’ of your project.
        - Update _/config/config.java_ with EMG configurations (queues connection string etc.) provided by Equinix when you subscribe to EMG. Copy the YAML from your EMG subscription details on Equinix Developer Platform & override the placeholders provide in the config file.
    2. Create/Update/Cancel Orders through EMG for supported Equinix Product & Services.
        - *(Refer to the same section in Node.js Templates)*

    3. Receive Notifications from EMG:
        - Download and import the Java Template project (template-java-outgoing-notifications-v1)  into the Java IDE of your choice - Intellij IDEA or Eclipse IDE
        - Run the below script from with the parent folder _\template-java-outgoing-notifications-v1_  
            - `mvn install`
        - Ensure all the dependent libraries are successfully installed under ‘External Libraries’ of your project.
        - Update _/config/config.java_ with EMG configurations (queues connection string etc.) provided by Equinix when you subscribe to EMG. Copy the YAML from your EMG subscription details on Equinix Developer Platform & override the place holders provide in the config file.
        - Now click on the Debug icon next to “_EquinixNotificationListener_” drop down. 
        - This would open a new terminal and spin an indefinite listener on customer’s queue where messages would be received instantly whenever any new notification message pushed to the queue from Equinix.

## Tutorials
See the links below for the tutorials on how to use our EMG Templates for different scenarios:

- [Create Order through EMG using EMG Node.JS Templates](https://youtu.be/RK3b1vO0tuk)
- [Create Order through EMG using EMG Python Templates](https://youtu.be/iVyYZOUwuag)
- [Receive EMG Network Notifications](https://youtu.be/hGNEq4KQ4gA)
- [Receive EMG DataCenter Notifications](https://youtu.be/CdfmjxaSm9U)
- [Receive EMG Billing Notifications](https://youtu.be/lvRYIry97fA)

### Migration Guide
#### Introduction
This guide helps you migrate from EMG Order Management to REST APIs. It provides instructions on transitioning your order management workflows and explains the APIs you can use in the migration process.

##### Deprecation
We deprecated the API services related to the Order Management feature. While the feature may still work, it is no longer recommended for use and will not receive updates or bug fixes. Users are encouraged to migrate to REST API alternatives during this transition period.

Timelines:
 * Deprecation Start Date: October 1, 2024
 * End of Support Date: April 1, 2025
 * End of Life: October 1, 2025

### Alternatives

Due to decommissioning the Order Management, we recommend migrating to available REST API alternatives for the following EMG features: General (Orders, Lookup, and Attachments), Shipments, Work Visit, Smart Hands, Cross Connect, and Managed Services.

#### Mapping EMG to REST APIs
The sections below show how to map the EMG Order Management features to REST APIs.

EMG Feature	Migration to REST APIs	API Reference Details
Supporting Functionalities

##### Orders API

With the Orders API, you can:
 * Retrieve information on specific orders, such as order status and associated order notes	
 
 Visit Orders Beta API documentation

#####	Lookup API

With the Lookup API, you can:
 * Retrieve the location of specific service, for example, Work Visit/Shipment
 * Retrieve Patch Panel details and associated port data	Visit Lookup API documentation

#####	Attachments API

With the Attachments API, you can:
 * Upload required documents for your orders	Attachments APIs use v1

Visit Attachments API documentation

##### Inbound/Outbound Shipments	

With the Shipments API, you can:

 * Create inbound/outbound shipments
 * Modify your shipment order
The Orders API allows you to:
 * Cancel your shipment order
 * Add additional notes to your shipment order	Visit Shipments API documentation
Work Visit	With the Work Visit API, you can:

 * Schedule onsite visit
 * Modify your work visit schedule
The Orders API allows you to:
 * Cancel your work visit
 * Add additional notes to your work visit	See Work Visit API documentation
Smart Hands	With the Smart Hands API, you can:

 * Create Smart Hands order
The Orders API allows you to:
 * Cancel your smart hands order
 * Add additional notes to your smart hands order
 * View and respond to order negotiations	Smart Hands APIs use v1

Visit Smart Hands API documentation
Cross Connect	With the Cross Connect API, you can:

 * Create Cross Connect order
 * Modify Cross Connect
The Orders API allows you to:
 * Cancel your cross connect order API
 * Add additional notes to your cross connect order API	Visit Cross Connect API documentation

#### SmartHands Migration Guide
Equinix Messaging Gateway supports below SmartHands types. The below Operation Code and Service Attributes are passed in the request payload to indicate the SmartHands type. Refer to column ECP API mapping for the equivalent SmartHands API to be called for placing respective smarthands types. EMG uses direct mapping to service details attribute used in SmartHands API service details; the only difference is that EMG uses pascal casing while ECP uses camel casing for service details attribute.

| Smarthands Type | Description | Operation | Service Details Attribute | Mandatory/Optional | Type | Example | ECP API Mapping |
|---|---|---|---|---|---|---|---|
| **Request photos/documentation** | Request an Equinix Data Center Technician to provide cage-related pictures or documentation | `0000` | | | | | `https://api.equinix.com/v1/orders/smarthands/picturesDocument` |
| | | | `CameraProvidedBy` | Optional - If `documentOnly` is `true`<br>Mandatory - If `documentOnly` is `false` | String | Expected Values: `Equinix`, `Customer` | |
| | | | `OnDateAndTime` | Optional - If `documentOnly` is `true`<br>Mandatory - If `documentOnly` is `false` | Boolean | Expected Values: `true`, `false` | |
| | | | `DocumentOnly` | Optional | Boolean | Expected Values: `true`, `false` | |
| | | | `Summary` | Optional - If `documentOnly` is `true`<br>Mandatory - If `documentOnly` is `false` | String | `"Cage 10 photo requested"` | |
| **SmartHand Other** | Request a Smart Hands order not listed here | `0001` | | | | | `https://api.equinix.com/v1/orders/smarthands/other` |
| **SmartHand Cage Clean up** | Request an Equinix Data Center Technician to clean your cage | `0002` | | | | | `https://api.equinix.com/v1/orders/smarthands/cageCleanup` |
| | | | `PermissionToDiscardBoxes` | Optional | Boolean | Expected Values: `true`, `false` | |
| | | | `DampMoistMopRequired` | Optional | Boolean | Expected Values: `true`, `false` | |
| **SmartHand Shipment Unpack** | Request inbound shipment unpacking and packaging disposal to an Equinix Data Center Technician | `0003` | | | | | `https://api.equinix.com/v1/orders/smarthands/shipmentUnpack` |
| | | | `InboundShipmentId` | Optional | String | It's the Order Number for corresponding Inbound Shipment Order that customer would have placed for its incoming shipment that he/she needs to be unpacked.<br>`RequesterId` or `ServicerId` can be provided. | |
| | | | `CopyOfPackingSlipNeeded` | Optional | Boolean | Expected Values: `true`, `false`.<br>This will result in a photo being sent to customer or copy of Packing slip stored for later customer use. | |
| | | | `DiscardShipmentMaterial` | Optional | Boolean | Expected Values: `true`, `false` | |
| **SmartHand Cage Escort** | Request an Equinix IBX security escort for a visitor to access your cage | `0004` | | | | | `https://api.equinix.com/v1/orders/smarthands/cageEscort` |
| | | | `DurationVisit` | Optional | String | Expected Value: `"30 Minutes"`, `"60 Minutes"`, `"90 Minutes"`, `"2 Hours"`, `"2 Hours 30 Minutes"`, `"3 Hours"`, `"3 Hours 30 Minutes"`, `"4 Hours"`.<br>For longer hours, include 4 hours in the request schema and add details in the description field. | |
| | | | `OpenCabinetForVisitor` | Optional | Boolean | Expected Values: `true`, `false` | |
| | | | `SupervisionReqForVisitor` | Optional | Boolean | Expected Values: `true`, `false`.<br>Equinix personnel will be present for entire stay for supervised escort. | |
| | | | `WorkVisitId` | Optional | String | It's the Order Number for corresponding Work Visit Order that customer would have placed for its visitor who needs to be escorted by Equinix Data Center technician.<br>`RequesterId` or `ServicerId` can be provided. | |
| **Equipment Install** | Request equipment installation per your specifications by an Equinix Data Center Technician | `0005` | | | | | `https://api.equinix.com/v1/orders/smarthands/equipmentInstall` |
| | | | `DeviceLocation` | Optional | String | | |
| | | | `ElevationDrawingAttached` | Optional | Boolean | Expected Values: `true`, `false`.<br>Equinix Data Center Technician to review the drawings if available. | |
| | | | `InstallationPoint` | Optional | String | Textual definition of where to install equipment in cabinet. | |
| | | | `InstalledEquipmentPhotoRequired` | Optional | Boolean | Expected Values: `true`, `false`.<br>Equinix Data Center Technician will send the photos via 2Way. | |
| | | | `MountHardwareIncluded` | Optional | Boolean | Expected Values: `true`, `false`.<br>Equipment specific mounting hardware provided by customer. | |
| | | | `PatchDevices` | Optional | Boolean | Expected Values: `true`, `false`.<br>If this flag is sent as `"true"`, after hardware install, `patchinfo` will be used for further instructions on patching device. | |
| | | | `PatchingInfo` | Optional - If `PatchDevices` is `'N'`<br>Mandatory - If `PatchDevices` is `'Y'` | String | Dependent on `PatchDevices` for content being used in installation. | |
| | | | `PowerItOn` | Optional | Boolean | Expected Values: `true`, `false`.<br>If this flag is sent as `"true"`, power will be connected to cabinet after install hardware.<br>If this is true then `PatchInfo` is required. | |
| | | | `NeedSupportFromASubmarineCableStationEngineer` | Optional | Boolean | Expected Values: `true`, `false`.<br>Equinix Data Center Specific: Specially trained technician to be available for Equinix Data Centers which can directly access submarine cables. | |
| **Request Cables** | Request cables per your specifications | `0006` | | | | | `https://api.equinix.com/v1/orders/smarthands/cableRequest` |
| | | | `Summary` | Optional | String | Any additional details | |
| | | | `MediaType` | Mandatory - If `Quantity` = 1 | String | Expected Values : `[ Multi-mode 62.5mic, Multi-mode 50mic, Single-mode, Cat-5, Cat-6, Coax, POTS, T1, E1 ]` | |
| | | | `ConnectorType` | Mandatory - If `Quantity` = 1 | String | Expected Values: `[ RJ45, SC, LC, BNC, Other ]` | |
| | | | `Length` | Mandatory - If `Quantity` = 1 | String | User should specify units. Ex: `"20 ft"` | |
| | | | `Quantity` | Optional | String | Expected Values: `[ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, >10 ]` | |
| **Locate Packages** | Request the location of your packages at the Equinix Data Center | `0007` | | | | | `https://api.equinix.com/v1/orders/smarthands/locatePackage` |
| | | | `InboundShipmentId` | Optional | String | It's the Order Number for corresponding Inbound Shipment Order that customer would have placed for its incoming shipment that he/she needs to be located.<br>`RequesterId` or `ServicerId` can be provided. | |
| | | | `CarrierTrackingNumber` | Optional | String | `"323-12121"` | |
| | | | `PossibleLocation` | Optional | String | `"Near cabinet 1010"` | |
| | | | `PackageDescription` | Optional | String | `"It's small box with 1kg weight."` | |
| **Run Patch Cables** | Request cables to be run between devices by an Equinix Data Center Technician | `8` | | | | | `https://api.equinix.com/v1/orders/smarthands/runJumperCable` |
| | | | `Summary` | Optional | String | Any additional details | |
| | | | `Quantity` | Optional | String | Expected Values: `[ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 12+ ]` | |
| | | | `JumperType` | Mandatory - If `Quantity` = 1 | String | Expected Values: `[ Jumper, Pre-Wiring, Patch Cable, Other ]` | |
| | | | `MediaType` | Mandatory - If `Quantity` = 1 | String | Expected Values: `[ Multi-mode 62.5mic, Multi-mode 50mic, Single-mode, Cat-5, Cat-6, Coax, POTS, T1, E1 ]` | |
| | | | `Connector` | Mandatory - If `Quantity` = 1 | String | Expected Values: `[ RJ45, SC, LC, BNC, Other ]` | |
| | | | `CableId` | Optional | String | | |
| | | | `ProvideTxRxLightLevels` | Mandatory - If `Quantity` = 1 | Boolean | Expected Values: `true`, `false`.<br>When this flag is set to `"true"`, Equinix will report back to customer light levels when turned on. | |
| | | | `DeviceDetails` | Optional | Array of `DeviceDetails` | Though `DeviceDetails` is optional however if supplied all fields within need to be populated.<br>Ex: `[ { "Name": "Device Name", "Slot": "50", "Port": "50" } ]` | |
| **Patch Cable Install** | Request patch cable installations per your specifications by an Equinix Data Center Technician | `9` | | | | | `https://api.equinix.com/v1/orders/smarthands/patchCableInstall` |
| | | | `CrossConnects` | Optional | Array of `CableInstall` | `[ { "SerialNumber": "string", "DeviceCabinet": "string", "DeviceConnectorType": "string", "DeviceDetails": "string", "DevicePort": "string", "LightLinkVerification": true, //Optional "Description": "string" //Optional } ]` | |
| **Move Patch Cable** | Request patch cables to be moved between devices by an Equinix Data Center Technician | `10` | | | | | `https://api.equinix.com/v1/orders/smarthands/moveJumperCable` |
| | | | `Summary` | Optional | String | Any additional details | |
| | | | `Quantity` | Optional | String | Expected Values: `[ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 12+ ]` | |
| | | | `CableId` | Optional | String | `CableId` as stored in `AssetId` and `CrossConnect` `"A01-5-10"` OR `"None"` if not. | |
| | | | `CurrentDeviceDetails` | Mandatory - If `Quantity` = 1 | `DeviceDetails` Object | Though `DeviceDetails` is optional however if supplied all fields within need to be populated.<br>Ex: `[ { "Name": "Device Name", "Slot": "50", "Port": "50" } ]` | |
| | | | `NewDeviceDetails` | Mandatory - If `Quantity` = 1 | `DeviceDetails` Object | Though `DeviceDetails` is optional however if supplied all fields within need to be populated.<br>Ex: `[ { "Name": "Device Name", "Slot": "50", "Port": "50" } ]` | |
| **Patch Cable Removal** | Request patch cable removal per your specifications by an Equinix Data Center Technician | `11` | | | | | `https://api.equinix.com/v1/orders/smarthands/patchCableRemoval` |
| | | | `CrossConnects` | Optional | Array of `CableDeinstallDetail` | `[ { "SerialNumber": "string", "DeviceCabinet": "string", "DeviceConnectorType": "string", "DeviceDetails": "string", "DevicePort": "string", "RemoveCableWhileLive": true, //Optional "Description": "string" //Optional } ]` | |
| **Large SmartHands Order** | Request a `Large_SmartHands_order`.<br>Any cabling request greater than 24 cables. Maximum limit: 200 cables.<br>or Install Equipment build greater than 100 RU in total equipment size. Maximum limit: 500 RU’s.<br>It usually takes 2-3 business days for Equinix to review the request order and assign the earliest available schedule date. | `12` | | | | | `https://api.equinix.com/v1/orders/smarthands/largeOrder` |
| | | | `Description` | Mandatory | String | `Cabling request of 50 cables` | |

Working Example:
How to get ibxLocation details:
 * We could obtain ibx, cage, cabinet, account number using the below curl request, and fill into respective fields in ibxLocation.
```sh
$ curl --request GET \
  --url 'https://api.equinix.com/v1/orders/smarthands/locations?detail=false&ibxs=SOME_STRING_VALUE&cages=SOME_STRING_VALUE' \
  --header 'accept: application/json' \
  --header 'authorization: SOME_STRING_VALUE' \
  --header 'content-type: application/json'
Response:
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

How to get attachment id:
 * We could upload the attachment via attachment API to obtain the attachment name & attachmentId.
```sh
curl --request POST \
  --url 'https://api.equinix.com/v1/attachments/file?purpose=SOME_STRING_VALUE' \
  --header 'accept: multipart/form-data' \
  --header 'authorization: SOME_STRING_VALUE' \
  --header 'content-type: multipart/form-data; boundary=---011000010111000001101001' \
  --form uploadFile=SOME_FILE_VALUE
```


Response:
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

SmartHands Creation:

`POST https://api.equinix.com/v1/orders/smarthands/other`, order number will be available in the 201 response once successfully created.
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

Success 201Response:
```json
{
    "OrderNumber": "1-190986534844"
}
```
Additional notes:
 * There are 3 types of scheduleType:
 * STANDARD:
EMG defaults to standard when both requestedStartDate & requestedCompletionDate are null. Choose this option and we will complete your request in the standard turnaround time pending install base readiness. Most requests are processed within 24 to 72 hours. Requests will be processed on a first come, first served basis unless they are expedited. RequestedStartDate and requestedCompletionDate ignored for standard scheduling

EXPEDITED: EMG automatically fills this type for user when the requestedCompletionDate is >2hr and within 24 hrs from IBX time. Choose this option and Equinix will prioritize your request and attempt to fulfill it as soon as reasonably possible. Additional fees may apply. RequestedCompletionDate is mandatory for expedite scheduling. RequestedStartDate is ignored for expedite scheduling.

SCHEDULED_MAINTENANCE: Choose this option to schedule a request for a specific date and time, including today. RequestedStartDate and requestedCompletionDate are mandatory for schedule maintenance
 *  When AdditionalContacts object is provided, EMG would overide details of TECHNICAL CONTACT sent as part of "CustomerContact" attribute. You can send details of non-registered contacts with Equinix Customer Portal.
Update SmartHands:
Responding to 1Way & 2Way Notes, with ServicerId in EMG payload being the orderId. User could retrieve the attachments using the attachment Api as above:

```sh
$ curl --request POST \
  --url https://api.equinix.com/colocations/v2/orders/{orderId}/notes \
  --header 'authorization: Bearer REPLACE_BEARER_TOKEN' \
  --header 'content-type: application/json' \
  --data '{"referenceId":"{orderId}","text":"The text of the note","attachments":[{"id":"c77c5f58-a7ea-4e88-9fc4-1a2900027425","name":"error-log"}]}'
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

Steps to reply to order negotiations:
 * EMG provide a 1 step process to respond to order negotiation. It would require calling 2 APIs as below:
 * Getting the referenceId to respond, replacing orderId with ServiceId :

```sh
curl --request GET \
  --url https://api.equinix.com/colocations/v2/orders/{orderId}/negotiations \
  --header 'authorization: Bearer REPLACE_BEARER_TOKEN'
```
Response:
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




Replying to order negotiation, attaching the referenceId from first step and using the same EMG servicerId for the orderId:
```sh
curl --request POST \
  --url https://api.equinix.com/colocations/v2/orders/{orderId}/negotiations \
  --header 'authorization: Bearer REPLACE_BEARER_TOKEN' \
  --header 'content-type: application/json' \
  --data '{"referenceId":"4-9091830","action":"APPROVE","reason":"Cancelling the new time"}'
```
 * Enum: "APPROVE" "APPROVE_NON_EXPEDITE" "CANCEL". These enum action are originally filled inside the description field in EMG payload.

Use APPROVE to accept order with new proposed date, APPROVE_NON_EXPEDITE to accept order without expedite and CANCEL to cancel order
Cancelling Smarthands
 * Using the servicerId for the orderId as well as the description for the reason, call the below API to cancel the order:
```sh
curl --request POST \
  --url https://api.equinix.com/colocations/v2/orders/{orderId}/cancel \
  --header 'authorization: Bearer REPLACE_BEARER_TOKEN' \
  --header 'content-type: application/json' \
  --data '{"reason":"string","attachments":[{"id":"c77c5f58-a7ea-4e88-9fc4-1a2900027425","name":"error-log"}],"lineIds":["1-D89731S"]}'
```
