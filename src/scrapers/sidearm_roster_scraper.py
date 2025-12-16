import requests
from bs4 import BeautifulSoup

def sidearm_roster_scraper(roster_url):
    response = requests.get(roster_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    athletes = []

    names = soup.select('.sidearm-roster-player-name a')

    for tag in names:
        name = tag.get_text(strip=True)

        if name:
            athletes.append(name)

    return athletes

if __name__ == "__main__":
    url = "https://mcgillathletics.ca/sports/swimming-mens/roster"
    roster = sidearm_roster_scraper(url)

    for name in roster:
        print(name)
    
    print(f"\nTotal athletes found: {len(roster)}")