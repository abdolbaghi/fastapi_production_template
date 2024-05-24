
json = {
  "uid": "food_list", # Unique identifier for your index
  "primaryKey": "name",
  "fields": ["name","calory", "tags", "ingredients"] # List of searchable attributes
}

import requests

# Replace with your Meilisearch server address and port
host = "http://<YOUR_HOST>"
port = 7700

# Define the data for the POST request
data = {
    "uid": "food_list",
    "primaryKey": "name",
    "fields": ["name", "calory", "tags", "ingredients"]
}

# Set the headers for the request
headers = {'Content-Type': 'application/json','X-Meili-Api-Key': api_key}

# Construct the URL
url = f"{host}:{port}/indexes"

# Send the POST request
response = requests.post(url, json=data, headers=headers)

# Check for successful response (status code 200)
if response.status_code == 200:
  print("Index created successfully!")
else:
  print(f"Error creating index: {response.text}")