import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv 

load_dotenv()

#connect tp DB
def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

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
            team_gender = EXCLUDED.team_gender
        RETURNING id;
    """, (name, roster_url, platform, team_gender))

#get first row of query result
    university_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return university_id
    

def get_or_create_athlete(full_name):
    conn = get_connection()
    cur = conn.cursor()

#SQL code to execute
    cur.execute("""
        INSERT INTO athletes (full_name)
        VALUES(%s)
        ON CONFLICT (full_name) DO NOTHING
        RETURNING id;
    """, (full_name,))

    row = cur.fetchone()

    if row:
        athlete_id = row[0]
    else:
        cur.execute("SELECT id FROM athletes WHERE full_name = %s", (full_name,))
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
        INSERT INTO university_athletes(athlete_id, university_id)
        VALUES(%s, %s)
        ON CONFLICT (athlete_id, university_id) DO NOTHING;
    """, (athlete_id, university_id))

    conn.commit()
    cur.close()
    conn.close()
