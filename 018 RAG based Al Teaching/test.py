import requests

r = requests.get("http://localhost:11434/api/tags")

print("Status:", r.status_code)
print(r.text)