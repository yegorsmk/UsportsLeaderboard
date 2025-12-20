import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv 

load_dotenv()

DB_CONFIG = {
    "name": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "host": os.getenv("DB_HOST"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT"),
}

#connect tp DB
def get_connection():
    return psycopg2.connect(DB_CONFIG)

def get_or_create_uni(name, roster_url=None, platform=None, team_gender=None):
    conn = get_connection()
    cur = conn.cursor()

#SQL code to execute, if duplicate -> replace info with new
    cur.execute("""
        INSERT INTO universities (name, roster_url, platform, team_gender)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (name) DO UPDATE SET
            roster_url = EXCLUDED.roster_url,
            platform = EXCLUDED.platform,
            team_gender = EXCLUDED.team_gendeer
        RETURNING id;
    """, (name, roster_url, platform, team_gender))

#get first row of query result
    university_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return university_id
    

def get_or_create_athlete(first_name, last_name):
    conn = get_connection()
    cur = conn.cursor()

#SQL code to execute
    cur.execute("""
        INSERT INTO athletes (full_name)
        VALUES(%s)
        ON CONFLICT (full_name) DO NOTHING
        RETURNING id;
    """, (last_name))

    athlete_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return athlete_id
    
def link_athlete_to_uni(athlete_id, university_id):
    conn = get_connection()
    cur = conn.cursor()

#SQL code to execute
    cur.execute("""
        INSERT INTO universty_athletes(athlete_id, university_id)
        VALUES(%s, %s)
        ON CONFLICT (athlete_id, university_id) DO NOTHING;
    """, athlete_id, university_id)

    conn.commit()
    cur.close()
    conn.close()
