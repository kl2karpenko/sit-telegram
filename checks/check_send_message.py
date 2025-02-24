import requests

url = "https://telegram-service-sit-307026759423.us-central1.run.app"

data = {
    "message": "Hello from Python!"
}

response = requests.post(url, json=data)

print(response.text)  # Prints the response from your Cloud Function