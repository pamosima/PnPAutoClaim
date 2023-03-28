from logging import debug
from flask import Flask, request
from dnacentersdk import DNACenterAPI
import pandas as pd
import ipaddress

app = Flask(__name__)

api = DNACenterAPI(username='admin', 
                   password='C1sco12345', 
                   base_url="https://dnac.its-best.ch:443", 
                   version='2.3.3.0', 
                   verify=False)

file = pd.read_csv("work_files/mapping.txt", sep = ",")


@app.route('/claim', methods=['POST'])
def dnac_alert_received():
    if request.method == 'POST':
        dnac_notification = request.get_json()
        print(dnac_notification)
        
        # TODO: test if the right values are return form the webhook
        ip = dnac_notification['details']['ipAddress']
        #deviceName = dnac_notification['details']['deviceName']
        deviceId = dnac_notification['network']['deviceId'] #not sure if this is true
   
        #ip = "172.20.101.2" 
        #serialNo = "JAE231609EK"
        #deviceId=api.device_onboarding_pnp.get_device_list(serial_number=serialNo)[0]["id"]
        #print("deviceId="+deviceId)

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
        return("Webhook Recieved")


if __name__ == '__main__':
    
    app.run(host="0.0.0.0", port="9002", ssl_context="adhoc", debug=True)    
