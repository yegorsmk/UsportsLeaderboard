from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import time
import requests

def search_sr_athletes(name, szn_year, club_filter=None):
    # Split name into first and last
    parts = name.split()
    first_name = parts[0] if parts else ""
    last_name = " ".join(parts[1:]) if len(parts) > 1 else ""

    options = Options()
    options.add_argument("--headless=new")  # Run without browser window; remove to debug
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) using for personal USPORTS leaderboard project")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.swimrankings.net/index.php?page=athleteSelect&nationId=0&selectPage=SEARCH")

    try:
        wait = WebDriverWait(driver, 50)

        # Locate inputs
        last_name_input = wait.until(EC.presence_of_element_located((By.ID, "athlete_lastname")))
        first_name_input = driver.find_element(By.ID, "athlete_firstname")  # Assuming ID from typical structure

        # Fill names (typing triggers onkeyup)
        first_name_input.clear()
        first_name_input.send_keys(first_name)
        last_name_input.clear()
        last_name_input.send_keys(last_name)
        time.sleep(5)  # Allow JS to load results

        # Wait for table to populate
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "athleteSearch")))

        # Get table HTML
        table_html = driver.find_element(By.CLASS_NAME, "athleteSearch").get_attribute("outerHTML")

        # Parse with BS4 for rows
        soup = BeautifulSoup(table_html, 'lxml')
        rows = soup.find_all("tr")[1:]  # Skip header

        athletes = []
        for row in rows:
            name_cell = row.find("td", class_="name")
            if not name_cell:
                continue

            link = name_cell.find("a")
            if not link:
                continue

            href = link.get("href", "")
            id_match = re.search(r"athleteId=(\d+)", href)
            if not id_match:
                continue

            athlete_id = int(id_match.group(1))
            athlete_name = link.get_text(strip=True)
            club_td = row.find("td", class_="club")
            club = club_td.get_text(strip=True) if club_td else ""

            match_found = False
            if club_filter and club_filter.lower() not in club.lower():
                match_found = True
            else:
                match_found = check_meet_history_club(athlete_id, club_filter)
                time.sleep(2)

            if match_found:
                athletes.append({
                    "athlete_id": athlete_id,
                    "full_name": athlete_name,
                    "club": club,
                    "profile_url": f"https://www.swimrankings.net/index.php?page=athleteDetail&athleteId={athlete_id}&pbest={szn_year}",
                })

        return athletes

    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        driver.quit()


def check_meet_history_club(athlete_id, club_filter):

    meet_history_url = f"https://www.swimrankings.net/index.php?page=athleteDetail&athleteId={athlete_id}&athletePage=MEET"

    headers = {
        "User-Agent": "Mozilla/5.0 (USPORTS scraper personal project)",
    }

    try:
        response = requests.get(meet_history_url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch meet history for athlete {athlete_id}: {e}")
        return False
    
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find("table", class_="athleteMeet")
    if not table:
        print(f"No meet table for athlete {athlete_id}")
        return False
    
    club_tds = table.find_all("td", class_="club")
    for td in club_tds:
        club_text = td.get_text(strip=True).lower()
        if club_filter.lower() in club_text:
            return True
        
    return False
    


if __name__ == "__main__":
    norm_name = "Charles Bertrand"
    uni_club = "Universite de Montreal"
    szn_year = 2026
    candidates = search_sr_athletes(norm_name, szn_year, club_filter=uni_club)
    
    if candidates:
        matched = candidates[0]  # Since one result
        athlete_id = matched["athlete_id"]
        profile_url = matched["profile_url"]
        print(f"Matched Athlete ID: {athlete_id}, Profile URL: {profile_url}")
    else:
        print("No matches found")