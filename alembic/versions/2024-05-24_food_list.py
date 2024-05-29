from src.database import MeiliSearch


# Define the data for the POST request
data = {
    "uid": "food_list",
    "primaryKey": "name"
    }

response = MeiliSearch.create_index(data)
print("Index created successfully!")