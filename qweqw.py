import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urljoin


def find_team_page(base_url):
    # Keywords to search for in the URLs
    keywords = ['team', 'people', 'about', 'staff', 'leadership', 'our-team', 'who-we-are']

    # Set up the web driver (Chrome in this example)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode to avoid opening a browser window
    driver = webdriver.Chrome(options=options)  # Ensure chromedriver is in PATH or specify its path

    try:
        # Navigate to the base URL
        driver.get(base_url)

        # Find all links (anchor tags with href attributes)
        links = driver.find_elements(By.TAG_NAME, 'a')

        # Loop through the links to find matching keywords
        for link in links:
            href = link.get_attribute('href')
            text = link.text.lower()

            # Skip empty or None hrefs
            if href:
                href_lower = href.lower()

                # Check if the href or link text contains any of the keywords
                if any(keyword in href_lower for keyword in keywords) or any(keyword in text for keyword in keywords):
                    # Join relative URLs with the base URL
                    full_url = urljoin(base_url, href)
                    print(f"Found possible team page: {full_url}")
                    return full_url

        print("No team/people page found.")
        return None

    finally:
        # Close the browser
        driver.quit()


def scrape_team_page(team_url):
    # Set up the web driver (Chrome in this example)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode to avoid opening a browser window
    driver = webdriver.Chrome(options=options)  # Ensure chromedriver is in PATH or specify its path

    try:
        # Navigate to the team page URL
        driver.get(team_url)

        # Assuming team member info is in some common tags, adjust as needed (e.g., div, article)
        team_members = driver.find_elements(By.CSS_SELECTOR, ".holder")  # Adjust the selector as needed

        # Loop through potential team members' elements
        for member in team_members:
            links = [link.get_attribute('href') for link in member.find_elements(By.CSS_SELECTOR, "ul.social-network-list li a")]

        return links

    finally:
        # Close the browser
        driver.quit()


def scrape_website_for_team(base_url):
    # First, find the team page URL
    team_url = find_team_page(base_url)

    # If a team page is found, scrape it; otherwise, return an empty result
    if team_url:
        return scrape_team_page(team_url)
    else:
        return {"team": []}


# Example usage
base_url = "https://a16z.com"  # Replace with your target domain
team_data = scrape_website_for_team(base_url)

# Print or save the result as JSON
print(json.dumps(team_data, indent=4))
