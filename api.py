import requests as req

# The API endpoint
url = "http://127.0.0.1:8000"

# A GET request to the API
response = req.get(url)

# Print the response
response_json = response.json()
print(response_json)
