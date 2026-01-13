import re

def name_normalize(raw_name):
    name = raw_name.strip()
    name = re.sub(r"\s+", " ", name)

    if " " not in name:
        name = re.sub(
            r"([a-zà-öø-ÿ])([A-ZÀ-ÖØ-Þ])",
            r"\1 \2",
            name
        )

    parts = name.split()

    if len(parts) <= 2:
        return name
    
    if any('-' in i for i in parts):
        return name
    
    first = parts[0]
    last = parts[-1]

    normalized = first + " " + last

    return normalized

if __name__ == "__main__":
    test_names = [
        "EleanoreAubin",
        "Yegor Semenyuk",
        "Adam         Al                   Seafan",
        "Charles-Antoine Boucher",
        "Karl Abou Ghannam"
    ]

    for n in test_names:
        print(f"Raw: '{n}' -> Normalized: '{name_normalize(n)}'")