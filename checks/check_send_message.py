import requests

# api_id = 27604095
# api_hash = '0fb35a13c5f5dc31e48637336294026e'
# phone_number = '+420774895021'  # Replace with your phone number

url = "https://telegram-message-handler-307026759423.us-central1.run.app"

data = {
    "api_id": 27604095,
    "api_hash": "0fb35a13c5f5dc31e48637336294026e",
    "phone_number": "+420774895021",
    "recipients": ["lkarpenko_pro"],
    "message": "Ahoj!!!"
}

headers = {
    "Authorization": f"Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Ijc2M2Y3YzRjZDI2YTFlYjJiMWIzOWE4OGY0NDM0ZDFmNGQ5YTM2OGIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIzMjU1NTk0MDU1OS5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsImF1ZCI6IjMyNTU1OTQwNTU5LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTAzMTYyNTA4MDkyNDcxNzc3OTUwIiwiaGQiOiJzY2FsZWluaXQub3JnIiwiZW1haWwiOiJzdXBwb3J0QHNjYWxlaW5pdC5vcmciLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6Im90M2hNc1NYWjlQQ0w3OWlqYWhabEEiLCJpYXQiOjE3NDA0MTk3MjUsImV4cCI6MTc0MDQyMzMyNX0.dYdgf8vd4QGZHDNwI9QYVNtWDOW6sqUOLwr3CSafEqz4Iu7m7jwES0--7leugAN1U8nVVMWRJcrITpF_syYTkmOb8ac9ayqH-s__CpI6g90zFRXnSkgVN1qfJJ2GVNm5cyBAfzBj4iZ7KXz1kIUMPOl0CqQBd_agrkcAJdoagMiFDTGjltn_jAvk1B9ppUPO5vCB14cyRbxA5EcuK9UfR3rQURyvjVx4Nhsm5Ym9kbIU-Jqbjdvpy9tCrXnyjLFfsvktFN1Pw50Jg37TTr2gkf5Aq7Xzco7AND-KXo1mmzFOENwkSwzzp0ptbF1HIU23enxeVTgcxuvl_rXSQjCfbg",
    "Content-Type": "application/json"
}

response = requests.post(url, json=data, headers=headers)

print(response.text)  # Prints the response from your Cloud Function