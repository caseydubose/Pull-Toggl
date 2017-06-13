import requests
from splinter import Browser
import time

'''
For this to work, you need to setup Toggl to have the name of project exactly as it is listed in Salesforce. 
For Admin Work, you need to list Thomson Reuters as the client and setup the respective tasks.
You'll also need to pull the API and Workspace ID from Toggl and create a cred file.
Finally, you will need to specifically update the field for data timeline to get the values that you want to upload. 
'''

#import Creds for Toggl & SF
timeentry = str('https://na31.salesforce.com/a0M/e')

signin = str('https://login.salesforce.com/')

with open('C:\\Users\\U0127576\Dropbox\Programming\Python\Credentials\\togglcreds.txt') as credFile:
    cred_lines = list(credFile)
_api_token = str(cred_lines[0]).rstrip()
_workspace_id = int(cred_lines[1])

with open('C:\\Users\\U0127576\Dropbox\Programming\Python\Credentials\sfcreds.txt') as SF_credfile:
    SF_credlines = list(SF_credfile)

#define data timeline
since = str("2017-04-01")
until = str("2017-04-24")

# #initialize browser
 browser = Browser('chrome')

#login to SF
 browser.visit('https://login.salesforce.com/')
 browser.find_by_id('password').first.fill(SF_credlines[1])
 browser.find_by_id('username').first.fill(SF_credlines[0])

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
    description = id['description']
    dur = id['dur']
    time = float((dur / (1000 * 60 * 60)) % 24)
    user = id['user']
    client = id['client']
    project = id['project']
    billable = id['is_billable']
    task = id['task']
    date = id['start']
    print(date + user + client + project + str(task) + description + str(billable))
#load into salesforce
    browser.visit(timeentry)
    browser.find_by_id("CF00N37000006A1dD").first.fill(project)
    browser.find_by_id('00N37000006A1dI').first.fill(date)
    browser.find_by_id('00N37000006A1dN').first.fill(dur)
    browser.find_by_id('CF00N37000006ADRZ').first.click()
    browser.find_by_id('CF00N37000006ADRZ').first.fill(user)
    browser.find_by_id('00N37000006A1dc').first.fill(description)
    browser.find_by_id('00N37000006A1dS').first.click()
#decision tree for the service categories
    if billable == str("True"):
        browser.find_by_id('00N37000006A1dS').select("Billable")
        browser.find_by_name('save').first.click()
    elif client == str("Thomson Reuters"):
        browser.find_by_id('00N37000006A1dS').select("Non-Billable")
        browser.find_by_id('00N37000006A1dX').select(task)
        browser.find_by_name('save').first.click()
    else:
        browser.find_by_id('00N37000006A1dS').select("Operations")
        browser.find_by_id('00N37000006A1dX').select("Client Travel")
        browser.find_by_name('save').first.click()
    time.sleep(1)
    with open("C:\\Users\\U0127576\Dropbox\Programming\Python\Salesforce Timesheet\TimesheetLog.txt", "a") as myfile:
        myfile.write('Row #' + str(reader.line_num) + " | " + row['Project'] + " | " + row['Description'] + " | " + row['Date'])
        myfile.write("\n")



