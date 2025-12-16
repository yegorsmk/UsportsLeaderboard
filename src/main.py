from scrapers import unk_roster_scraper, sidearm_roster_scraper
from utils import load_universities, name_normalize
    
def main():
    universities = load_universities.load_universities('data/universities.csv')
    all_athletes = []

    for uni in universities:
        platform = uni['platform']
        roster_url = uni['roster_link']

        print(f"\nScraping {uni['university_name']} ({uni['team_gender']})")

        if platform == "sidearm":
            athletes = sidearm_roster_scraper.sidearm_roster_scraper(roster_url)
        
        elif platform == "unk":
            athletes = unk_roster_scraper.unk_roster_scraper(roster_url)

        else:
            print(f"Unsupported platform: {platform}")
            continue

        print(f"Found {len(athletes)} athletes:")
        for name in athletes:

            print(name_normalize.name_normalize(name))

        all_athletes.extend(athletes)

        print(f"Total athletes so far: {len(all_athletes)}")

if __name__ == "__main__":
    main()