# from Google workspace's "Python quickstart"
import os.path
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
        
def add_tasks():
    return

if __name__ == "__main__":
    authenticate()