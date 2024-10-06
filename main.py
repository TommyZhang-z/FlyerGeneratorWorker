from tasks import generate_flyer

# Test variables
flyer_id = "TEST002"
suburb = "Austral"
address = "10 Circinus St"
lot = "565"
price = "$750,000"
land_size = 100
house_size = 100
lot_width = 100
land_price = "$500,000"
rego = "Registered"
facade = "PALM 21 ND"
floorplan = "Standard Plan"
facade_file_url = (
    "https://drive.google.com/uc?id=10T_oSsXE3zw_e6np0Z9jKd9atwBytfQ4&export=download"
)
floorplan_file_url = (
    "https://drive.google.com/uc?export=download&id=1QU6PpSOG-KODKFaGoOdCnJMoiH4fXGbH"
)
bedroom = 6
bathroom = 4
parking_slot = 2

# Call the function directly
output_pdf = generate_flyer(
    flyer_id,
    suburb,
    address,
    lot,
    price,
    land_size,
    house_size,
    lot_width,
    land_price,
    rego,
    facade,
    floorplan,
    facade_file_url,
    floorplan_file_url,
    bedroom,
    bathroom,
    parking_slot,
)

# print(f"Flyer generated: {output_pdf}")

# Note: In a production environment, you typically wouldn't use .get()
# to wait for results, as it defeats the purpose of asynchronous tasks.
# Instead, you'd usually set up a callback or use a results backend to
# handle task completion.
