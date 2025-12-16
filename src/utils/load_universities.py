import csv

def load_universities(csv_path):
    universities = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            universities.append(row)
        return universities