import csv
import json
import ast

INPUT_CSV = "./Matching-algorithm/mock_user_dataset.csv"
OUTPUT_JSON = "users.json"

def parse_list_field(value):

    try:
        return ast.literal_eval(value)
    except:
        return []

def convert_csv_to_json():
    users = []

    with open(INPUT_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            user = {
                "id": int(row["user_id"]),
                "age": int(row["age"]),
                "city": row["city"],
                "location": [
                    float(row["lat"]),
                    float(row["lon"])
                ],
                "interests": parse_list_field(row["interests"]),
                "lifestyle": parse_list_field(row["lifestyle"]),
                "preferences": {
                    "age_range": [
                        int(row["pref_min_age"]),
                        int(row["pref_max_age"])
                    ],
                    "max_distance_km": int(row["pref_max_distance_km"])
                }
            }
            users.append(user)

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

    print(f"JSON file created: {OUTPUT_JSON}")


if __name__ == "__main__":
    convert_csv_to_json()
