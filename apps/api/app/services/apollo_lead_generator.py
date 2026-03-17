import os
import requests
from dotenv import load_dotenv

load_dotenv()

APOLLO_API_KEY = os.getenv("APOLLO_API_KEY")


def generate_leads_from_apollo(icp, limit=50):

    url = "https://api.apollo.io/v1/mixed_people/search"

    payload = {
        "api_key": APOLLO_API_KEY,
        "q_organization_industries": [icp.industry],
        "person_titles": [icp.job_titles],
        "q_organization_locations": [icp.location],
        "page": 1,
        "per_page": limit
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print(f"Apollo API Error {response.status_code}: {response.text}")
        return []

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print(f"Apollo API returned non-JSON response: {response.text}")
        return []

    leads = []

    for person in data.get("people", []):

        lead = {
            "first_name": person.get("first_name"),
            "last_name": person.get("last_name"),
            "email": person.get("email"),
            "company": person.get("organization", {}).get("name"),
            "job_title": person.get("title"),
            "linkedin": person.get("linkedin_url")
        }

        leads.append(lead)

    return leads