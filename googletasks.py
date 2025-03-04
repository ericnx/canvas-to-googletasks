# from Google workspace"s "Python quickstart"
import os
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/tasks"]

def authenticate():
    creds = None

    # first, check if the user has already been authorized with 
    # their access and refresh tokens.
    # ("token.json" is automatically created and stores the 
    # access and refresh tokens when being authorized for the first time)
    if os.path.exists("token.json"):
        # use the existing credentials from "token.json"
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # next, check for valid credentials
    if creds is None or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # refresh the access token
            creds.refresh(Request())
        else:
            # create the credentials from "credentials.json"
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0) # port=0 - any available port

        with open("token.json", "w") as token:
            # replaces the old "token.json" with new credentials
            token.write(creds.to_json())

    return build("tasks", "v1", credentials=creds)
        
def add_tasks(courses_and_assignments):
    service = authenticate()
    
    for course_id, course_data in courses_and_assignments.items():
        course_name = course_data.get("course_name")
        assignments = course_data.get("assignments")

        for assignment in assignments:
            if assignment and len(assignment) == 3 and check_duplicate(course_name, assignment) == False:
                due_time = assignment[2][11:16]
                # convert from 24hr time to 12hr time
                due_time = datetime.strptime(due_time, "%H:%M").strftime("%I:%M %p")
                task_body = {
                    "title": f"{assignment[1]} due at {due_time} ({course_name})",                        
                    "due": assignment[2]
                }
                service.tasks().insert(tasklist="@default", body=task_body).execute()
                print(f"Added task: {assignment[1]} ({course_name})")

def check_duplicate(course_name, assignment):
    service = authenticate()
    tasks = service.tasks().list(tasklist="@default", maxResults=100, showHidden=True).execute().get("items", [])

    if not tasks: # empty list
        return False
    
    for task in tasks:
        if assignment[1] in task.get("title") and course_name in task.get("title"):
            print(f"Didn't add duplicate task: {assignment[1]} ({course_name})")
            return True # found duplicate task
        
    return False # no duplicates

# for testing purposes
# deletes all uncompleted tasks
def delete():
    service = authenticate()
    tasks = service.tasks().list(tasklist="@default", maxResults=100).execute().get("items", [])

    for task in tasks:
        if task:
            service.tasks().delete(tasklist="@default", task=task["id"]).execute()
            print(f"Deleted task: {task["title"]}")

if __name__ == "__main__":
    delete()