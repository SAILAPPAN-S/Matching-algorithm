def jaccard_interest_similarity(interests_a: list, interests_b: list) -> float:
    """Jaccard: |A ∩ B| / |A ∪ B|. Returns 0-1."""
    set_a = set(interests_a)
    set_b = set(interests_b)
    
    if not set_a or not set_b:
        return 0.0
    
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union

# TEST CASES
print("=== INTEREST JACCARD ===")
test_cases = [
    (["hiking", "coding", "travel"], ["travel", "yoga"], 0.25),  # 1/4
    (["music", "sports"], ["music", "sports"], 1.0),           # 2/2
    ([], ["coding"], 0.0),                                     # Empty
    (["solo"], [], 0.0),                                       # Empty
]

for a, b, expected in test_cases:
    result = jaccard_interest_similarity(a, b)
    print(f"{a} vs {b} → {result:.2%} {'✅' if abs(result - expected) < 0.01 else '❌'}")
