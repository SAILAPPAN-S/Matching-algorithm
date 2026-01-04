import json
import math
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# LOAD DATA
def load_users(json_path="./Matching-algorithm/users.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


# INTEREST SIMILARITY (COSINE)
def interest_similarity(list_a, list_b):
    if not list_a or not list_b:
        return 0.0

    docs = [" ".join(list_a), " ".join(list_b)]
    vec = CountVectorizer().fit_transform(docs)
    sim = cosine_similarity(vec[0:1], vec[1:2])[0][0]
    return float(sim)



# AGE SCORE
def age_score(user, candidate):
    pref_min, pref_max = user["preferences"]["age_range"]
    c_age = candidate["age"]

    if pref_min <= c_age <= pref_max:
        return 1.0

    # decay outside range
    diff = min(abs(c_age - pref_min), abs(c_age - pref_max))
    return max(0.0, 1 - (diff / 10))  # 10-year decay window


# LOCATION SCORE (HAVERSINE DISTANCE)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (math.sin(dlat/2)**2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon/2)**2)

    return 2 * R * math.asin(math.sqrt(a))


def location_score(user, candidate):
    lat1, lon1 = user["location"]
    lat2, lon2 = candidate["location"]
    dist = haversine(lat1, lon1, lat2, lon2)

    max_dist = user["preferences"]["max_distance_km"]

    if dist >= max_dist:
        return 0.0

    return 1 - (dist / max_dist)


# LIFESTYLE SCORE
def lifestyle_score(list_a, list_b):
    if not list_a or not list_b:
        return 0.0

    set_a = set(list_a)
    set_b = set(list_b)

    if len(set_a) == 0:
        return 0.0

    overlap = len(set_a.intersection(set_b))
    return overlap / len(set_a)


# FINAL COMPATIBILITY SCORE

def compatibility(user, candidate):
    s_age = age_score(user, candidate)
    s_int = interest_similarity(user["interests"], candidate["interests"])
    s_loc = location_score(user, candidate)
    s_life = lifestyle_score(user["lifestyle"], candidate["lifestyle"])

    final = (
        s_age * 0.20 +
        s_int * 0.30 +
        s_loc * 0.25 +
        s_life * 0.25
    )

    return round(final * 100, 2)

# MATCH EXPLANATION
def generate_explanation(u, c):
    exp = []

    if interest_similarity(u["interests"], c["interests"]) > 0.6:
        exp.append("High interest overlap")
    else:
        exp.append("Some shared interests")

    if age_score(u, c) == 1:
        exp.append("Within your preferred age range")

    if location_score(u, c) > 0.6:
        exp.append("Near your location")

    if lifestyle_score(u["lifestyle"], c["lifestyle"]) > 0.5:
        exp.append("Good lifestyle compatibility")

    return ", ".join(exp)


def get_matches_for_single_user(users, target_id, top_k):
    # find user
    user = next((u for u in users if u["id"] == target_id), None)
    if not user:
        return {"error": "User not found"}

    scores = []

    for c in users:
        if c["id"] == user["id"]:
            continue

        score = compatibility(user, c)
        scores.append({
            "user_id": c["id"],
            "score": score,
            "explanation": generate_explanation(user, c)
        })

    scores = sorted(scores, key = lambda x: x["score"], reverse=True)
    return scores[:top_k]


def main():
    users = load_users("./Matching-algorithm/users.json")
    matches = get_matches_for_single_user(users, target_id=3, top_k=10)

    with open("top_matches.json", "w", encoding="utf-8") as f:
        json.dump(matches, f, indent=4)

    # print(matches)

if __name__ == "__main__":
    main()
