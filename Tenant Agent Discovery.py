import requests
import json
import getpass
import yaml

from pprint import pprint

requests.packages.urllib3.disable_warnings() 

print("Started")

tenant_url = ''

def login_func():
    with open('config.yml','r') as yaml_file:
        yaml_data = yaml.safe_load(yaml_file)
    tenant_url = yaml_data['tenant']['url']
    print(f"Url: {tenant_url}")
    username = yaml_data['tenant']['username']
    print(f"Username: {username}")
    url = tenant_url + "/api/v1/auth/login"

    headers = {
        "Cache-Control": "no-cache",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }

    password = getpass.getpass(prompt = 'Enter your tenant password: ')
    data = {"username": "dpearce@accedian.com", "password": password}
    resp = requests.post(url, headers=headers, data=data, verify=False)
    resp.raise_for_status()
    token =(resp.headers['Authorization'])

    return token, tenant_url

def get_session_data (token, tenant_url):
    url = tenant_url + "/api/orchestrate/v3/agents/sessions"
    print(url)
    headers = {
        "Accept": "application/vnd.api+json",
        "Authorization": token,
    }

    resp = requests.get(url, headers=headers, verify=False)
    resp.raise_for_status()

    dataj = resp.json()

    length = len(dataj['data'])
    i=-1

    with open("status.log","w") as status_log:
        while i < length:
            agentId = dataj['data'][i]['attributes']['agentId']
            sessionId = dataj['data'][i]['attributes']['session']['sessionId']
            sessionType = dataj['data'][i]['attributes']['session']['sessionType']
            sessionName = dataj['data'][i]['attributes']['session']['sessionName']
            i +=1
            #pprint(agentId+ " " +sessionId)
            sessionMessage = ""
            url = tenant_url+"/api/orchestrate/v3/agents/sessionstatus/"+ str(sessionId)
        
            headers = {
                "Accept": "application/vnd.api+json",
                "Authorization": token,
                }
            resp = requests.get(url, headers=headers, verify=False)
            resp.raise_for_status()
            status = resp.json()

            sessionStatus = status['data']['attributes']['status']
            if sessionStatus == 'error':
                sessionMessage = status['data']['attributes']['statusMessage']
            print(f"Agent id: {agentId} Session Id: {sessionId} Session Name: {sessionName} Session Status: {sessionStatus}", file=status_log)

    status_log.close()
    return

data = login_func()
get_session_data(data[0],data[1])


print("Finished")
