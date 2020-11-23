# Templates for Equinix Messaging Gateway
Equinix Messaging Gateway (EMG) is an event-based communication channel for Platform Equinix. EMG automates the creation, update, and closure or cancellation of SmartHands, Trouble Ticket, Work Visit and Shipments tickets along with notification of statuses such as 2-Way Communications, technician notes and status advancement. The Templates provide sample code for customers to integrate with EMG. These Templates are available in two versions – node.js and python. 

---

## Template Details 

The Templates includes:

1. Template with sample code to integrate with EMG and create, update, cancel and get order status notifications for Equinix Ticket Types – SmartHands, Trouble Ticket, Work Visit.
 - EquinixSmartHandsTemplate
 - EquinixTroubleTicketTemplate
 - EquinixWorkVisitTemplate
 - EquinixShipmentsTemplate

2. TestClient with sample code on how to integrate with EMG Templates following EMG message schemas.
- /test/TestClient

3. Configurations for EMG queues. These configurations will be provided by Equinix during the onboarding process. 
- /config/config

## Requirements

1. Node.js Templates 
- [Node.js](https://nodejs.org/en/download/) v10.16.2+

2. Python Templates:

- [Python](https://www.python.org/downloads/) - v3.8.5+
- [Azure SDK for Python](https://azuresdkdocs.blob.core.windows.net/%24web/python/azure-servicebus/0.50.3/index.html) - v0.50.3+
- [pytest](https://docs.pytest.org/en/stable/getting-started.html) - v6.0.1+
- [pytest-asyncio](https://pypi.org/project/pytest-asyncio/) - v0.14.0+

3. Java Templates
- Java 8 & above
- IntelliJ IDEA or Eclipse IDE


## Prerequisites 
1. Visit [Equinix Developer Platform](https://developer.equinix.com/) & follow the [steps](https://developer.equinix.com/docs/ecp-getting-started#generating-client-id-and-client-secret-key) to generate Client ID and Client Secret keys.

2. Node.js Templates:
- Run "npm install" from the root directory to install azure-bus package and other dependent libraries as per “package.json”

3. Python Templates:
- Install Azure Service Bus Package
  ```sh
   pip install azure-servicebus
   ```
- Install pytest framework to run Test Client:
  ```sh
   pip install pytest
   
   pip install pytest-asyncio
   ```
3. Java Templates
- Download and import the Java Template project into the Java IDE of your choice - Intellij IDEA or Eclipse IDE
- Run the below script from with the parent folder \template_java_v1
  mvn install
- Ensure all the dependent libraries are successful installed under ‘External Libraries’ of your project.
   

## How to Run Test Client
1. Navigate to test/TestClient and run on individual tests to submit orders. 
2. After creating an order, take note of the ServicerId displayed in the console, and replace ORDER_NUMBER constant in TestClient 
3. Output will be displayed in the console.





 
