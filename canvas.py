import requests
import os
from dotenv import load_dotenv
from datetime import date, datetime
from dateutil import tz

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
                    # nested dict
                    # course id: {
                    #   course name: str
                    #   course assignments: []
                    # }
                    course_list[course.get("id")] = {
                        "course_name": course.get("name"),
                        "assignments": [],
                    }

            url = None
            for link in r.headers.get("link").split(","): # breaks into separate links
                if 'rel="next"' in link: # rel = relation, looks for the "next" page/relation
                    url = link.split(";")[0].strip("<>") # gets the clean url of the "next" page which is the first link
        else:
            print(f"Failed to get the courses for URL:{url} - Status:{r.status_code}")

    return course_list

def get_canvas_assignments(course_list):
    # gets the assignments' ids, names, and due dates and adds it along with the course's id and name
    today = date.today()
    local_time_zone = tz.tzlocal()

    for course_id in course_list: # O(C * A). C = # of courses, A = # of assignments
        url = f"{CANVAS_URL}/{course_id}/assignments" # creates a new url to get the course's assignments
        r = requests.get(url, headers=h, params=p)
        
        if r.status_code == 200:
            assignments = r.json()
            print(f"Assignments for course: {course_list[course_id]["course_name"]}")

            if len(assignments) != 0: # there is an "Assignments" tab
                latest_assignment = assignments[-1].get("due_at")
                # ignores old assignments
                if latest_assignment is None or date.fromisoformat(latest_assignment[:10]) < today:
                    course_list[course_id]["assignments"] = "No assignments"
                    print(f"- {course_list[course_id]["assignments"]}")
                    continue

                for assignment in assignments:
                    if assignment.get("id") and assignment.get("name"):
                        if assignment.get("due_at"):
                            due_date = datetime.fromisoformat(assignment.get("due_at"))
                        else: # if there is an assignment but no due date, then set due date for today
                            due_date = datetime.now()

                        due_date = due_date.astimezone(local_time_zone) # gets the operating system's local time zone
                        due_date_str = due_date.strftime("%Y-%m-%dT%H:%M:%SZ") # formats the date to be JSON serializable

                        # course id: {
                        #   course name: str
                        #   course assignments: [
                        #       [assignment id, assignment name, assignment due date]
                        #   ]
                        # }
                        if due_date.date() >= today:
                            course_list[course_id]["assignments"].append([assignment.get("id"), assignment.get("name"), due_date_str])
                            print(f"- {assignment.get("name")} due at {due_date}")
            else: # no "Assignments" tab
                course_list[course_id]["assignments"] = "No assignments"
                print(f"- {course_list[course_id]["assignments"]}")
        else:
            print(f"Failed to get the assignments for ID:{course_id} - Status:{r.status_code}")
    
    return course_list

if __name__ == "__main__":
    get_canvas_assignments(get_canvas_courses(url))