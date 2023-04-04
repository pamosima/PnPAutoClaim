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

from flask import Flask, request
from dnacentersdk import DNACenterAPI
import pandas as pd
import ipaddress

app = Flask(__name__)

file = pd.read_csv("work_files/mapping.csv", sep = ",")


@app.route('/claim', methods=['POST'])
def dnac_alert_received():
    if request.method == 'POST':
        dnac_notification = request.get_json()
        print(dnac_notification)
        
        ip = dnac_notification['details']['ipAddress']
        serialNo = dnac_notification['details']['deviceName']
        dnacIP =  dnac_notification['dnacIP']
        
        api = DNACenterAPI(base_url="https://"+dnacIP+":443", 
                   version='2.3.3.0', 
                   verify=False)

        deviceId = api.device_onboarding_pnp.get_device_list(serial_number=serialNo)[0]["id"]

        for inx, row in file.iterrows(): 
            if ipaddress.ip_address(ip) in ipaddress.ip_network(row['subnet']):
            
                print(row) 

                siteId = api.sites.get_site(name=str(row["site"]))["response"][0]["id"]
                
                hostname = str(row["hostname_prefix"])+"-"+serialNo[-3:].lower()
                print("hostname="+hostname)
                
                if str(row["type"]) == "Default":
                    templateId = api.configuration_templates.get_templates_details(name=str(row["templateName"]))["response"][0]["id"]
                    configInfo = {'configId': templateId, 
                                'configParameters': [{'key': 'HOSTNAME', 'value': hostname},
                                                    {'key': 'P2P_ONBOARDING_IP_ADDRESS', 'value': str(row["P2P_ONBOARDING_IP_ADDRESS"])},
                                                    {'key': 'P2P_ONBOARDING_GW', 'value': str(row["P2P_ONBOARDING_GW"])},
                                                    {'key': 'P2P_ONBOARDING_VLAN', 'value': str(int(row["P2P_ONBOARDING_VLAN"]))}]}
                    api.device_onboarding_pnp.claim_a_device_to_a_site(configInfo=configInfo, 
                                                    hostname=hostname,  
                                                    deviceId=deviceId, 
                                                    siteId=siteId, 
                                                    type=str(row["type"]))
                elif str(row["type"]) == "AccessPoint":
                    api.device_onboarding_pnp.claim_a_device_to_a_site(hostname=hostname,  
                                                    deviceId=deviceId, 
                                                    siteId=siteId, 
                                                    type=str(row["type"]),
                                                    rfProfile=str(row["rfProfile"]))
                

        return("Webhook Recieved")


if __name__ == '__main__':
    
    app.run(host="0.0.0.0", port="9002", ssl_context="adhoc")    
