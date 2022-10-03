# Templates for Equinix Messaging Gateway
Equinix offers an event-driven system called **_Equinix Messaging Gateway (EMG)_**. The EMG system enables system-to-system integration from your in-house application to Platform Equinix. Use EMG to:
-	Create/update/cancel orders & receive order status notifications for subscribed Equinix Products & Services - Cross Connect, Shipments, SmartHands, Trouble Tickets, Work Visit.
-	Receive status notifications on provisioned Equinix Fabric Ports & Virtual Connections 
-	Receive notifications for planned/unplanned maintenance at Equinix DataCenters
-	Billing Notifications when your submitted order is closed & billing is started by Equinix 

Learn more about Equinix Messaging Gateway by visiting this [link](https://developer.equinix.com/docs?page=/dev-docs/emg/overview), or you can watch the EMG Overview video [here](https://youtu.be/9netRhONlRg).

To subscribe to EMG, visit the [Subscriptions](https://developer.equinix.com/subscriptions) page in the Equinix Developer Platform to get started. Watch this [video](https://youtu.be/jGYTi3Bn5YM) for the step-by-step guide on how to subscribe. Alternatively, you can also reach out to your Equinix Customer Success Manager.

Equinix Messaging Gateway (EMG) Templates provide reference code to seamlessly integrate with EMG. These Templates are available in three versions – Node.js, Python and Java. You can refer, use, modify & extend EMG Templates based on your architecture & security policies.  

---

## Template Details 

The Templates includes:

1.  Order Templates with sample code for order management - create, update & cancel orders with Equinix:
    -  /template-nodejs-v1

    -  /template-python-v1

    -  /template_java_v1

2. Notification Templates with sample code to receive notifications from Equinix:
    - /template-nodejs-outgoing-notifications-v1

    - /template-python-outgoing-notifications-v1

    - /template-java-outgoing-notifications-v1

3. Order Templates includes individual templates with sample code to create/update/cancel Equinix orders for supported Equinix Orders & Services:
    - /EquinixCrossConnectTemplate

    - /EquinixSmartHandsTemplate

    - /EquinixTroubleTicketTemplate

    - /EquinixWorkVisitTemplate

    - /EquinixShipmentsTemplate

4. Order Templates also includes TestClient with sample code on how to send request & receive response from EMG Templates using EMG message schemas. Visit How To Guide to know about EMG request & response schemas for supported Equinix Products & Services
    - /test/TestClient

5. Configurations for EMG queues. These configurations will be provided by Equinix when you subscribe to EMG. Copy the YAML from your EMG subscription details on Equinix Developer Platform & override the place holders provide in config file at below location:
    - /config/config

## Requirements

1. Node.js Templates 
    - [Node.js](https://nodejs.org/en/download/) v10.16.2+

    - Visual Code (https://code.visualstudio.com/)

2. Python Templates:
      - [Python](https://www.python.org/downloads/) - v3.8.5+

      - [Azure SDK for Python](https://azuresdkdocs.blob.core.windows.net/%24web/python/azure-servicebus/0.50.3/index.html) - v0.50.3+

    - [pytest](https://docs.pytest.org/en/stable/getting-started.html) - v6.0.1+

    - [pytest-asyncio](https://pypi.org/project/pytest-asyncio/) - v0.14.0+


3. Java Templates
    - Java 8 & above

    - IntelliJ IDEA or Eclipse IDE


## Prerequisites
1. An existing subscription with EMG is required in order to use our Templates. Visit the [Subscriptions](https://developer.equinix.com/subscriptions) page in the Equinix Developer Platform to get started. Alternatively, you can also reach out to your Equinix Customer Success Manager.
2. Visit [Equinix Developer Platform](https://developer.equinix.com/) & follow the [steps](https://developer.equinix.com/dev-docs/ecp/getting-started/getting-access-token#generating-client-id-and-client-secret) to generate Equinix Client ID and Client Secret keys.
3. You must have authorized permissions by your Master Administrator to order and receive notifications for Equinix Products & Services. 

## How to Run EMG Templates 
1. Node.js Templates:
    1. SDK Setup:
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

2. Python Templates:
    1. SDK Setup:
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

3. Java Templates
    1. SDK Setup:
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
