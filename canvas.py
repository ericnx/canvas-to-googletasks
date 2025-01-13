import requests
import os
from dotenv import load_dotenv
from datetime import date

load_dotenv()
CANVAS_TOKEN = os.getenv("CANVAS_TOKEN")
CANVAS_URL = url = os.getenv("CANVAS_URL")

h = {"Authorization": f"Bearer {CANVAS_TOKEN}"}
p = {"per_page": 1000}

def get_canvas_courses(url):
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

    return course_list

def get_canvas_assignments(course_list):
    # gets the assignments' ids, names, and due dates
    assignment_list = {}
    today = date.today()

    for course_id in course_list.keys(): # O(C * A). C = # of courses, A = # of assignments
        url = f"{CANVAS_URL}/{course_id}/assignments" # creates a new url to get the course's assignments
        r = requests.get(url, headers=h, params=p)
        
        if r.status_code == 200:
            assignments = r.json()
            print(f"Assignments for course: {course_list[course_id]}")

            latest_assignment = assignments[-1].get("due_at")
            if latest_assignment is None or date.fromisoformat(latest_assignment[:10]) < today:
                print("- No assignments")
                continue

            for assignment in assignments:
                if assignment.get("id") and assignment.get("name") and assignment.get("due_at"):
                    if date.fromisoformat(assignment.get("due_at")[:10]) >= today: # only get today's or future assignments
                        assignment_list[assignment.get("id")] = f"{assignment.get("name")} due at {assignment.get("due_at", "No due date")}"
                        print(f"- {assignment_list[assignment.get("id")]}")   
        else:
            print(f"Failed to get the assignments for ID:{course_id} - Status:{r.status_code}")
    
    print()
    return assignment_list

if __name__ == "__main__":
    get_canvas_assignments(get_canvas_courses(url))