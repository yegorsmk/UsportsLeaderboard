import requests
from bs4 import BeautifulSoup

def scrape_rosters(roster_url):
    response = requests.get(roster_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    athletes = []

    names = soup.select('.sidearm-table-player-name')

    for tag in names:
        name = tag.get_text(strip=True)

        if name:
            athletes.append(name)

    return athletes

if __name__ == "__main__":
    url = "https://mcgillathletics.ca/sports/swimming-mens/roster"
    roster = scrape_rosters(url)

    for name in roster:
        print(name)
    
    print(f"\nTotal athletes found: {len(roster)}")