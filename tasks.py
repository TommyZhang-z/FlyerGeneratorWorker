import os
from dotenv import load_dotenv

load_dotenv(".env.local")

from celery import Celery

# Get Redis URL from environment or use default
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Initialize Celery app
app = Celery("tasks", broker=redis_url, backend=redis_url)


@app.task
def generate_report(task_data):
    print(f"Generating report: {task_data}")
    with open("report.txt", "w") as f:
        f.write(f"Generating report: {task_data}")
