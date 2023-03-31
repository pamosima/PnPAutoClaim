# Cisco DNA Center PnP Onboarding Automation using Webhook Notification
This repository contains a set of scripts that automate the process of onboarding devices using Plug and Play (PnP) in Cisco DNA Center. The scripts address use cases where devices are onboarded without knowing the serial number in advance, which is a common scenario when a site has a specific IP subnet allocated to it.

The scripts utilize the webhook notification option of Cisco DNA Center's "unclaimed" process. When a device contacts DNAC, information such as its IP address and serial number is sent via webhook to our Flask application. The application then maps the IP subnet to a configuration file that includes parameter mapping to variables, and claims the device based on its IP address.

To streamline the onboarding process, we have leveraged multiple scripts available on the [CiscoDevNet/DNAC-onboarding-tools GitHub repository](https://github.com/CiscoDevNet/DNAC-onboarding-tools). Our scripts provide an efficient and automated solution to onboard devices in Cisco DNA Center, improving network provisioning time and reducing manual effort.

Feel free to contribute to this repository and enhance the automation process further.

## Requirements
Create a virtual environment and install the packages according to the requirements.txt

```
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## How to test
### 1. Import Test Sites
Import Test Sites to Cisco DNA Center using `/test_files/Test_Sites.csv`

### 2. Import CLI Template
Import Test Sites to Cisco DNA Center using `/test_files/C9k_Onboarding-Template.json`

### 3. Import Test Devices
Import Test Sites to Cisco DNA Center using `/test_files/Test_DeviceImportTemplate.csv`

### 4. Send notification to webhook

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
