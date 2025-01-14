import canvas
import googletasks
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("CANVAS_URL")

def main():
    courses = canvas.get_canvas_courses(url)
    assignments = canvas.get_canvas_assignments(courses)
    googletasks.add_tasks(assignments)

if __name__ == "__main__":
    main()