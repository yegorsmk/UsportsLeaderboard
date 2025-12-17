import swimrankings

athletes = swimrankings.Athletes(name="Yegor Semenyuk")

for athlete in athletes:
    print(f"Athlete: {athlete.full_name}, DOB: {athlete.birth_year}, Club: {athlete.club}")

    years = swimrankings.get_available_years()

    months = swimrankings.get_months_for_year(years[0])

    for name in months.items():
        print(f"Month: {name}")