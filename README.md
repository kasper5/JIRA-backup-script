# JIRA-backup-script
Backup script for JIRA Cloud, written in Python. The script triggers a backup job and periodically checks if the backup has completed. When the backup file exists in the WebDAV share the script will download it and send a notification to a Slack channel or your private account. 
