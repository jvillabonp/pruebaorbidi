import requests
from clickup import create_task

def create_contact(contact, access_token):
    url = "https://api.hubapi.com/crm/v3/objects/contacts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "properties": {
            "email": contact.email,
            "firstname": contact.firstname,
            "lastname": contact.lastname,
            "phone": contact.phone,
            "website": contact.website,
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

def sync_contacts(hubspot_access_token, clickup_access_token, clickup_list_id):
    hubspot_contacts = get_hubspot_contacts(hubspot_access_token)
    for contact in hubspot_contacts:
        if contact.get("estado_clickup") is None:
            create_task(contact, clickup_access_token, clickup_list_id)

def get_hubspot_contacts(access_token):
    url = "https://api.hubapi.com/crm/v3/objects/contacts?limit=100"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data.get("results", [])