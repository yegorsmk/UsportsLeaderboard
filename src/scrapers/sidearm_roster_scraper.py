import requests
from bs4 import BeautifulSoup

def sidearm_roster_scraper(roster_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (USPORTS scraper personal project)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    }

    response = requests.get(roster_url, headers=headers, timeout=30)
    soup = BeautifulSoup(response.text, 'html.parser')

    athletes = []

    names = soup.select('.sidearm-roster-player-name a')

    for tag in names:
        name = tag.get_text(strip=True)

        if name:
            athletes.append(name)

    return athletes

# if __name__ == "__main__":
#     url = "https://govikesgo.com/sports/swimming-and-diving/roster"
#     roster = sidearm_roster_scraper(url)

#     for name in roster:
#         print(name)
    
#     print(f"\nTotal athletes found: {len(roster)}")