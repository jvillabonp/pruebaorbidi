import requests

def create_task(contact, access_token, list_id):
    url = f"https://api.clickup.com/api/v2/list/{list_id}/task"
    headers = {
        "Authorization": access_token,
        "Content-Type": "application/json",
    }
    payload = {
        "name": f"{contact['firstname']} {contact['lastname']}",
        "description": f"Email: {contact['email']}\nPhone: {contact['phone']}\nWebsite: {contact['website']}",
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
