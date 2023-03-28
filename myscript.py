#!/usr/bin/env python

# Copyright (c) 2021 Cisco and/or its affiliates.

# This software is licensed to you under the terms of the Cisco Sample
# Code License, Version 1.1 (the "License"). You may obtain a copy of the
# License at

#                https://developer.cisco.com/docs/licenses

# All use of the material herein must be in accordance with the terms of
# the License. All rights not expressly granted by the License are
# reserved. Unless required by applicable law or agreed to separately in
# writing, software distributed under the License is distributed on an "AS
# IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied.

from dnacentersdk import DNACenterAPI
import json
import pandas as pd
import ipaddress

# Create a DNACenterAPI connection object; it uses DNA Center username and password, with DNA Center API version 1.2.10
# The base_url used by default is `from dnacentersdk.config import DEFAULT_BASE_URL`
api = DNACenterAPI(username='admin', 
                   password='C1sco12345', 
                   base_url="https://dnac.its-best.ch:443", 
                   version='2.3.3.0', 
                   verify=False)

file = pd.read_csv("work_files/mapping.txt", sep = ",")

# get ip and serial no from webhook
ip = "172.20.101.2" 
serialNo = "JAE231609EK"

deviceId=api.device_onboarding_pnp.get_device_list(serial_number=serialNo)[0]["id"]
print("deviceId="+deviceId)

for inx, row in file.iterrows(): 
    if ipaddress.ip_address(ip) in ipaddress.ip_network(row['subnet']):
       
        print(row) 

        siteId = api.sites.get_site(name=str(row["site"]))["response"][0]["id"]
        templateId = api.configuration_templates.get_templates_details(name=str(row["templateName"]))["response"][0]["id"]

        configInfo2 = {'configId': templateId, 
                      'configParameters': [{'key': 'HOSTNAME', 'value': str(row["HOSTNAME"])},
                                           {'key': 'P2P_ONBOARDING_IP_ADDRESS', 'value': str(row["P2P_ONBOARDING_IP_ADDRESS"])},
                                           {'key': 'P2P_ONBOARDING_GW', 'value': str(row["P2P_ONBOARDING_GW"])},
                                           {'key': 'P2P_ONBOARDING_VLAN', 'value': str(row["P2P_ONBOARDING_VLAN"])}]}
        
        api.device_onboarding_pnp.claim_a_device_to_a_site(configInfo=configInfo2, 
                                                            hostname=str(row["HOSTNAME"]),  
                                                            deviceId=deviceId, 
                                                            siteId=siteId, 
                                                            type="Default")
