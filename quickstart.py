from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/tasks'

def main():
    # Api reference that I used for this is here: https://developers.google.com/tasks/v1/reference/

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('tasks', 'v1', http=creds.authorize(Http()))

    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # The grocery list name includes the date
    tasklist = {
        'title': 'Grocery List ' + date
        }

    # Create new task list
    result = service.tasklists().insert(body=tasklist).execute()

    tasklist_id = result['id']
    task = {
        'title': 'Grocery 1'
    }

    # Add new task to the list that was previously created
    results = service.tasks().insert(tasklist=tasklist_id, body=task).execute()

if __name__ == '__main__':
    main()