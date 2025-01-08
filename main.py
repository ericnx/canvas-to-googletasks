import requests
import os
from dotenv import load_dotenv

load_dotenv()
CANVAS_TOKEN = os.getenv("CANVAS_TOKEN")
CANVAS_URL = url = os.getenv("CANVAS_URL")

h = {"Authorization": f"Bearer {CANVAS_TOKEN}"}
p = {"include": ["term"]}

course_ids_and_names = []
while url:
    r = requests.get(url, headers=h, params=p)
    courses = r.json()

    for course in courses:
        course_id = course.get("id")
        course_name = course.get("name")
        if course_id and course_name:
            course_ids_and_names.append({"id": course_id, "name": course_name})
            
    url = None
    for link in r.headers.get("Link","").split(","):
        if 'rel="next"' in link:
            url = link.split(";")[0].strip("<>")

print(course_ids_and_names)