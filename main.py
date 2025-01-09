import requests
import os
from dotenv import load_dotenv

load_dotenv()
CANVAS_TOKEN = os.getenv("CANVAS_TOKEN")
CANVAS_URL = url = os.getenv("CANVAS_URL")

h = {"Authorization": f"Bearer {CANVAS_TOKEN}"}
p = {"per_page": 1000}

# gets the courses using the student's Canvas token
course_list = {}
while url: # O(P * C). P = # of pages, C = # of courses
    r = requests.get(url, headers=h, params=p)
    if r.status_code == 200:
        courses = r.json()

        for course in courses:
            if course.get("id") and course.get("name"):
                course_list[course.get("id")] = course.get("name")

        url = None
        for link in r.headers.get("link").split(","): # breaks into separate links
            if 'rel="next"' in link: # rel = relation, looks for the "next" page/relation
                url = link.split(";")[0].strip("<>") # gets the clean url of the "next" page which is the first link

        print(f"{course_list}\n")
    else:
        print(f"Failed to get the courses for URL:{url} - Status:{r.status_code}")

# gets the assignments using the course ids and names
assignment_list = {}
for course_id in course_list.keys():
    url = f"{CANVAS_URL}/{course_id}/assignments"
    r = requests.get(url, headers=h, params=p)
    
    if r.status_code == 200:
        assignments = r.json()
        print(f"Assignments for course: {course_list[course_id]}")
        for assignment in assignments:
            if assignment.get("id") and assignment.get("name") and assignment.get("due_at"):
                assignment_list[assignment.get("id")] = f"{assignment.get("name")} due at {assignment.get("due_at", "No due")}"
                print(f"- {assignment_list[assignment.get("id")]}")
    else:
        print(f"Failed to get the assignments for ID:{course_id} - Status:{r.status_code}")