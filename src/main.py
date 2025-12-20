from scrapers import unk_roster_scraper, sidearm_roster_scraper
from utils import load_universities, name_normalize, db

    
def main():
    universities = load_universities.load_universities('data/universities.csv')

    for uni in universities:
        platform = uni['platform']
        roster_url = uni['roster_link']
        uni_name = uni['university_name']
        team_gender = uni['team_gender']

        print(f"\nScraping {uni_name} ({team_gender})")

        university_id = db.get_or_create_uni(uni_name, roster_url, platform, team_gender)

        if platform == "sidearm":
            athletes = sidearm_roster_scraper.sidearm_roster_scraper(roster_url)
        
        elif platform == "unk":
            athletes = unk_roster_scraper.unk_roster_scraper(roster_url)

        else:
            print(f"Unsupported platform: {platform}")
            continue

        print(f"Found {len(athletes)} athletes:")
        
        for name in athletes:
            norm_name = name_normalize.name_normalize(name)
            print(norm_name)

            athlete_id = db.get_or_create_athlete(norm_name)
            db.link_athlete_to_uni(athlete_id, university_id)

    print(f"All athletes stored into DB")

if __name__ == "__main__":
    main()