import requests
from bs4 import BeautifulSoup

def athlete_szn_pbs(full_name, athlete_url):

    headers = {
        "User-Agent": "Mozilla/5.0 (USPORTS scraper personal project)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    }

    response = requests.get(athlete_url, headers=headers, timeout=30)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find("table", class_="athleteBest")
    if not table:
        print(f"No PB table found for {full_name}")
        return {}
    
    pbs = {}

    rows = []
    for tr in table.find_all("tr"):
        class_list = tr.get("class")
        if class_list and class_list[0].startswith("athleteBest"):
            rows.append(tr)

    for row in rows:
        tds = row.find_all("td")
        if len(tds) < 3:
            continue

        event = tds[0].get_text(strip=True)
        course = tds[1].get_text(strip=True)
        time_link = tds[2].find("a")
        time = time_link.get_text(strip=True)

        if course == "25m" and time:
            event_clean = " ".join(event.split())
            pbs[event_clean] = time
        
    if not pbs:
        print(f"No SCM times found for this season for {full_name}")

    return pbs

if __name__ == "__main__":
    athlete_name = "Charles Bertrand"
    athlete_url = "https://www.swimrankings.net/index.php?page=athleteDetail&athleteId=4781841&pbest=2026"

    pbs = athlete_szn_pbs(athlete_name, athlete_url)

    if pbs:
        print("\nSCM Season Bests:")
        for event, time in pbs.items():
            print(f"{event}: {time}")