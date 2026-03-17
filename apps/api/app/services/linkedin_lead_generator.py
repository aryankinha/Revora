from playwright.sync_api import sync_playwright

import os
from dotenv import load_dotenv

load_dotenv()

LINKEDIN_EMAIL = os.getenv("YOUR_EMAIL")
LINKEDIN_PASSWORD = os.getenv("YOUR_PASSWORD")

def generate_leads_from_linkedin(icp, limit=20):

    leads = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print("Navigating to LinkedIn login...")
        page.goto("https://www.linkedin.com/login")

        print("Filling credentials...")
        page.fill("#username", LINKEDIN_EMAIL)
        page.fill("#password", LINKEDIN_PASSWORD)

        print("Clicking submit...")
        page.click("button[type=submit]")
        print("Waiting 5s for login...")
        page.wait_for_timeout(5000)
        
        print("Checking if logged in successfully...")
        search_url = f"https://www.linkedin.com/search/results/people/?keywords={icp.job_titles}"

        print(f"Navigating to search URL: {search_url}")
        page.goto(search_url)

        print("Querying profiles...")
        profiles = page.query_selector_all(".entity-result")
        print(f"Found {len(profiles)} profiles.")

        for profile in profiles[:limit]:

            try:
                name_elem = profile.query_selector(".entity-result__title-text")
                name = name_elem.inner_text() if name_elem else "Unknown"
                link_elem = profile.query_selector("a")
                link = link_elem.get_attribute("href") if link_elem else ""
                
                print(f"Scraped profile: {name}")

                leads.append({
                    "first_name": name,
                    "last_name": "",
                    "email": "linkedin_profile@example.com",
                    "company": "",
                    "job_title": icp.job_titles,
                    "linkedin": link
                })
            except Exception as e:
                print(f"Error scraping a profile: {e}")

        browser.close()

    return leads