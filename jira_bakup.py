#!/usr/local/bin/python2.7
import easywebdav
import time
import requests
import requests, requests.utils, pickle
import subprocess
import json
import os, os.path

user = "" # username for jira cloud
pw = "" # password for jira cloud
jiraCloud = "" # url for jira cloud
webDav = easywebdav.connect(jiraCloud, username=user, password=pw, protocol="https")
currTime = time.strftime("%Y%m%d")
backupName = "webdav/backupmanager/JIRA-backup-"+currTime+".zip"

s = requests.session() # start a persistent session
def startSession():

	resp = s.get("https://"+jiraCloud+"/Dashboard.jspa", auth=(user, pw))

	if resp.status_code is not 200:
		exit(1)
startSession()

def runBackup():

	postHeaders = {'X-Atlassian-Token': 'no-check', 'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/json'} 
	dataLoad = { 'cbAttachments': 'true' }
	postBak = s.post("https://"+jiraCloud+"/rest/obm/1.0/runbackup", data=json.dumps(dataLoad), headers=postHeaders)	
	# print postBak.status_code
	# print postBak.text

runBackup()

def backupExists():
	check =  webDav.exists(backupName)
	if check == True:
		return 0
	else:
		return 1

def sendToSlack(result):

	if result == 0:
		backupRes = "Succeeded"
	else:
		backupRes = "Failed"

	slackApi = ""
	slackData = { "text": "Backup for Jira Cloud has "+backupRes+"." }
	slackPost = requests.post(slackApi, data=json.dumps(slackData))	

while True:

	if backupExists() == 0:
		fileSave =  "/media/jira_backup/JIRA-backup-"+currTime+".zip"
		webDav.download(backupName, fileSave)
		if os.path.exists(fileSave) == True and os.stat(fileSave).st_size > 2000000000:
			sendToSlack(0)
		else:
			sendToSlack(1)
		break
	else:
		time.sleep(60) # sleep for 60 sec
		print 1
		continue
