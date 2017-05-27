import requests
from splinter import Browser
import time

#import Creds for Toggl & SF
with open('C:\\Users\\U0127576\Dropbox\Programming\Python\Credentials\\togglcreds.txt') as credFile:
    cred_lines = list(credFile)
_api_token = str(cred_lines[0]).rstrip()
_workspace_id = int(cred_lines[1])

#define data timeline
since = str("2017-04-01")
until = str("2017-04-24")

#pull toggl data
r = requests.get('https://toggl.com/reports/api/v2/details', auth=(_api_token, 'api_token'), params={
    'workspace_id': _workspace_id,
    'since': since,
    'until': until,
    'page': '1',
    'user_agent': 'api_test'
})

#loop through toggl data
data = r.json()
for id in data['data']:
    print(id)
    # description = id['description']
    # dur = id['dur']
    # user = id['user']
    # client = id['client']
    # project = id['project']
    # billable = id['is_billable']
    # task = id['task']
    # date = id['start']
    # print(date + user + client + project + str(task) + description + str(billable))

#  for project in data['data']:
#     for i in project['items']:
#         time_entry = i['title']['time_entry']
#         SOW = project['title']['project']
#         client = project['title']['client']
#         time = i['time']
#         hours = (time / (1000 * 60 * 60)) % 24
#         print(client + " " + SOW + " " + time_entry + ' ' + str(hours))
