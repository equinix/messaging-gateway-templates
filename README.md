Templates for Equinix Messaging Gateway
Equinix Messaging Gateway (EMG) is an event-based communication channel for Platform Equinix. EMG automates the creation, update, and closure or cancellation of SmartHands, Trouble Ticket, Work Visit and Shipments tickets along with notification of statuses such as 2-Way Communications, technician notes and status advancement. The Templates provide sample code for customers to integrate with EMG. These Templates are available in two versions – node.js and python. 

Template Details 
The Templates includes:
* Template with sample code to integrate with EMG and create, update, cancel and get order status notifications for Equinix Ticket Types – SmartHands, Trouble Ticket, Work Visit.
o EquinixSmartHandsTemplate
o EquinixTroubleTicketTemplate
o EquinixWorkVisitTemplate
* TestClient with sample code on how to integrate with EMG Templates following EMG message schemas.
o /test/TestClient
* Configurations for EMG queues. These configurations will be provided by Equinix during the onboarding process. 
o /config/config
Requirements
* Node.js Templates 
o Node.js Installation - v10.16.2+
* Python Templates:
o Python Installation - v3.8.5+ 
o Azure SDK for Python -v0.50.3+ 
o pytest -v6.0.1+  
o pytest-asyncio -v0.14.0+
Prerequisites 
* Visit Equinix Developer Platform & follow the steps to generate Client ID and Client Secret keys.
* Node.js Templates:
o Run "npm install" from the root directory to install azure-bus package and other dependent libraries as per “package.json”
* Python Templates:
o Install Azure Service Bus Package
pip install azure-servicebus
o Install pytest framework to run Test Client:
pip install pytest
pip install pytest-asyncio
How to Run Test Client
* Navigate to test/TestClient and run on individual tests to submit orders. 
* After creating an order, take note of the ServicerId displayed in the console, and replace ORDER_NUMBER constant in TestClient.js. 
* Output will be displayed in the console.




 
