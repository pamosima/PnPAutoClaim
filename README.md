# Cisco DNA Center PnP Onboarding Automation using Webhook Notification
This repository contains a Python Flask application that automate the process of onboarding devices using Plug and Play (PnP) in Cisco DNA Center. The scripts address use cases where devices are onboarded without knowing the serial number in advance, which is a common scenario when a site has a specific IP subnet allocated to it.

The scripts utilize the webhook notification option of Cisco DNA Center's "unclaimed" process. When a device contacts DNAC, information such as its IP address and serial number is sent via webhook to our Flask application. The application then maps the IP subnet to a configuration file that includes parameter mapping to variables, and claims the device based on its IP address.

To streamline the onboarding process, we have leveraged multiple scripts available on the [CiscoDevNet/DNAC-onboarding-tools GitHub repository](https://github.com/CiscoDevNet/DNAC-onboarding-tools). Our scripts provide an efficient and automated solution to onboard devices in Cisco DNA Center, improving network provisioning time and reducing manual effort.

Feel free to contribute to this repository and enhance the automation process further.

## Requirements
### Python
Create a virtual environment and install the packages according to the requirements.txt

```
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```
Set credentials as environment variables
```
$ cat mycredentials.sh
DNA_CENTER_USERNAME=your_username_here
DNA_CENTER_PASSWORD=your_password_here
$ source mycredentials.sh
$ python flaskapp.py
```

### Cisco DNA Center 
```Minimum version > 2.3.3.x```

Choose **Platform > Developer Toolkit > Event Notifications > Notifications**

Click **+** to create a new notifaction

**Step 1 - Select Site and Events**

Search for ```Device waiting to be claimed```, select the notification and click **Next**

**Step 2 - Select Channels**

Choose the **Rest** as a notification channels and click **Next**

**Step 3 - REST Settings**

Click **here** to create a new setting instance. This opens the page below:

<img width="1428" alt="image" src="https://user-images.githubusercontent.com/16715420/229145264-73d4d477-a911-4e46-8ed6-64014d3524d4.png">

**System > Settings > External Services > Destinations**

Click add and fill in the details based on the example:

<img width="564" alt="image" src="https://user-images.githubusercontent.com/16715420/229144668-a1fd8487-d415-4a5a-9e02-ddb40e2c1eec.png">

Return to the **Step 3 - REST Settings** page, refresh the instance select the created instance:

<img width="1727" alt="image" src="https://user-images.githubusercontent.com/16715420/229145633-8c7f70d5-34af-4ac6-9608-0d3a7e872b0c.png">

Click on **Next**

**Step 4 - Name and Description**

Provide a name and short description for your notification and click on **Next**

<img width="1726" alt="image" src="https://user-images.githubusercontent.com/16715420/229146045-4a78d6d5-bab2-4b3b-a1a1-3433eb0741c6.png">

On the Summary page click on **Finish**

Done! Your new notification is complete.

## How to test
### 1. Import Test Sites
Choose **Design > Network Hierarchy** and click **Import Sites**
<img width="1396" alt="image" src="https://user-images.githubusercontent.com/16715420/229137139-7f9a62f6-42d6-493e-aa42-7a54b510fff7.png">
Choose a file or drag and drop to upload: `/test_files/Test_Sites.csv`
Click **Upload** and then **Import**

### 2. Import CLI Template
Choose **Tools > Template Editor** and click **Onboarding Configuration**

Hover over the project **Onboarding Configuration**, click the gear icon, and click **Import Template**

import the template from `/test_files/C9k_Onboarding-Template.json`

### 3. Import Test Devices
Choose **Provision > Network Devices > Plug and Play** and click on **Add Devices**
<img width="774" alt="image" src="https://user-images.githubusercontent.com/16715420/229139847-a7211914-7273-45c3-af69-a888fd0b29d9.png">

Select **Bulk Devices** and the devices using `/test_files/Test_DeviceImportTemplate.csv`

<img width="549" alt="image" src="https://user-images.githubusercontent.com/16715420/229140256-38efbcfe-d62e-4924-8805-67b73b64dae0.png">

Select the Devices and click on add

### 4. Send notification to webhook
Choose **Platform > Developer Toolkit > Event Notifications > Event Catalog**

Search for Device waiting to be claimed


Webhook Switch test payload

```
{
    "ipAddress": "172.20.101.2",
    "deviceName": "JAE231609EK"
}
```
Webhook AP test payload
```
{
    "ipAddress": "172.20.201.10",
    "deviceName": "FCW2433P1L7"
}
```

## Issues/Comments

Please post any issues or comments directly on GitHub.
