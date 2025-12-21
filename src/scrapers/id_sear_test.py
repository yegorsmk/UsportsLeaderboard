import requests
from bs4 import BeautifulSoup
import re

def find_athlete_ids(full_name, nation="CAN"):
    # Split name more accurately (last name first word, first the rest? Wait, no — site uses separate fields)
    parts = full_name.split()
    first_name = parts[0]
    last_name = " ".join(parts[1:]) if len(parts) > 1 else ""

    params = {
        "page": "athleteSearch",
        "athleteFirstname": first_name,   # Common param name from libraries
        "athleteLastname": last_name,     # Or try "firstName"/"lastName" if this fails
        "nationId": nation,
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    }  # Fake browser to avoid blocks

    response = requests.get("https://www.swimrankings.net/index.php", params=params, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"URL used: {response.url}")  # Print this and paste into browser to compare

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Try common table classes
    table = soup.find('table', class_=re.compile(r'athlete|search|list', re.I))
    if not table:
        print("No table found — page HTML:", soup.prettify()[:1000])  # Debug
        return []

    links = soup.find_all('a', href=re.compile(r'athleteId=\d+'))
    ids = []
    for link in links:
        match = re.search(r'athleteId=(\d+)', link['href'])
        if match:
            name = link.get_text(strip=True)
            ids.append((match.group(1), name))
    
    return ids

# Test
print(find_athlete_ids("Yegor Semenyuk"))