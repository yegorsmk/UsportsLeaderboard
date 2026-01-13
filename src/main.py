from scrapers import unk_roster_scraper, sidearm_roster_scraper, swimrankings_search, pbs_scraper
from utils import load_universities, name_normalize, db
import time

szn_year = 2026
    
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

            candidates = swimrankings_search.search_sr_athletes(norm_name, szn_year, uni_name)
            if not candidates:
                print(f"No SR match for {norm_name}")
                continue

            matched = candidates[0]
            sr_id = matched["athlete_id"]
            profile_url = matched["profile_url"]
            print(f"Matched SR ID: {sr_id}, Profile URL: {profile_url}")

            db.get_or_create_athlete(sr_id, norm_name, profile_url)
            db.link_athlete_to_uni(sr_id, university_id)

            pbs = pbs_scraper.athlete_szn_pbs(norm_name, profile_url)
            for event, result in pbs.items():
                db.insert_pb(sr_id, event, result, course='25m', season=szn_year)

            time.sleep(10)


    print(f"All athletes stored into DB")

    

if __name__ == "__main__":
    main()