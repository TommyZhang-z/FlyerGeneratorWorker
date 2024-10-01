import os
from dotenv import load_dotenv

load_dotenv(".env.local")

from celery import Celery

# Get Redis URL from environment or use default
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Initialize Celery app
app = Celery("tasks", broker=redis_url, backend=redis_url)


# ID	Suburb	Address	Lot	Price	Rego	Facade	FloorPlan	Facade File	Floorplan File	Bedroom	Bathroom	Parking Slot
@app.task
def generate_flyer(
    flyer_id,
    suburb,
    address,
    lot,
    price,
    rego,
    facade,
    floorplan,
    facade_file,
    floorplan_file,
    bedroom,
    bathroom,
    parking_slot,
):
    print(f"Generating flyer: {flyer_id}")
    # prin facade_file and floorplan_file
    print(facade_file)
    print(floorplan_file)
