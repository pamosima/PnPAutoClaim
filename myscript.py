
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
# Create a DNACenterAPI connection object; it uses DNA Center username and password, with DNA Center API version 1.2.10
# The base_url used by default is `from dnacentersdk.config import DEFAULT_BASE_URL`
api = DNACenterAPI(username='admin', password='C1sco12345', base_url="https://dnac.its-best.ch:443", version='2.3.3.0', verify=False)

site ="Global/Denner/Aargau/Store-101/Store-101-1"
templateName = "C9k_Onboarding-Template"
p2p_onboarding_ip_address = "172.20.10.2"
p2p_onboarding_gw = "172.20.10.1"
p2p_onbarding_vlan = "20"
hostname = "store010-s20006"

siteId=api.sites.get_site(name=site)["response"][0]["id"]
deviceId=api.device_onboarding_pnp.get_device_list(serial_number="JAE231609EK")[0]["id"]
templateId=api.configuration_templates.get_templates_details(name=templateName)["response"][0]["id"]
print("siteId="+siteId)
print("deviceId="+deviceId)
print("templateId="+templateId)

api.device_onboarding_pnp.claim_a_device_to_a_site(configInfo={'configId': templateId, 'configParameters': [{'key': 'HOSTNAME', 'value': hostname},{'key': 'P2P_ONBOARDING_IP_ADDRESS', 'value': p2p_onboarding_ip_address},{'key': 'P2P_ONBOARDING_GW', 'value': p2p_onboarding_gw},{'key': 'P2P_ONBOARDING_VLAN', 'value': p2p_onbarding_vlan}]}, hostname=hostname,  deviceId=deviceId, siteId=siteId, type="Default")