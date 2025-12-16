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

    return name

if __name__ == "__main__":
    test_names = [
        "EleanoreAubin",
        "Yegor Semenyuk",
        "Adam         Al                   Seafan"
    ]

    for n in test_names:
        print(f"Raw: '{n}' -> Normalized: '{name_normalize(n)}'")