import requests
from bs4 import BeautifulSoup

def unk_roster_scraper(roster_url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/121.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive",
    }

    response = requests.get(roster_url, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, 'html.parser')

    athletes = []

    names = soup.select('.avatar-card__title, .name, td a[href^="/natation/alignement/"], .player-name-social-row')

    for tag in names:
        name = tag.get_text(strip=True)

        if name:
            athletes.append(name)

    return athletes


# if __name__ == "__main__":
#     url = "https://teams.geegees.ca/sports/swim/2025-26/mroster"
#     roster = unk_roster_scraper(url)

#     for name in roster:
#         print(name)
    
#     print(f"\nTotal athletes found: {len(roster)}")