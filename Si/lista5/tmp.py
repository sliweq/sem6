import random
from collections import defaultdict
from get_data import get_celebrities 

def create_matching_pairs(celebrities,n):
    pairs = []
    while len(pairs) < n:
        person = random.choice(list(celebrities.keys()))
        if len(celebrities[person]) < 2:
            continue
        img1, img2 = random.sample(celebrities[person], 2)
        pairs.append((img1, img2, 1))
    return pairs

def create_non_matching_pairs(celebrities,n):
    pairs = []
    people = list(celebrities.keys())
    while len(pairs) < n:
        p1, p2 = random.sample(people, 2)
        img1 = random.choice(celebrities[p1])
        img2 = random.choice(celebrities[p2])
        pairs.append((img1, img2, 0))
    return pairs

def create_test_pairs(celebrities, train_sets, n):
    pairs = []
    used_photos = set()
    for train_set in train_sets:
        for img1, img2, label in train_set:
            used_photos.add(img1)
            used_photos.add(img2)
    while len(pairs) < n//2:
        p1, p2 = random.sample(list(celebrities.keys()), 2)
        img1 = random.choice(celebrities[p1])
        img2 = random.choice(celebrities[p2])
        if img1 not in used_photos and img2 not in used_photos:
            pairs.append((img1, img2, 0))
    while len(pairs) < n:
        person = random.choice(list(celebrities.keys()))
        if len(celebrities[person]) < 2:
            continue
        img1, img2 = random.sample(celebrities[person], 2)
        if img1 not in used_photos and img2 not in used_photos:
            pairs.append((img1, img2, 1))
    return pairs

def generate_datasets(train_sizes=[10, 100, 500, 1000, 5000], test_size=200):
    celebrities = get_celebrities() 

    all_datasets = {}
    for size in train_sizes:
        match = create_matching_pairs(celebrities,size // 2)
        nonmatch = create_non_matching_pairs(celebrities, size // 2)
        all_datasets[size] = match + nonmatch
        random.shuffle(all_datasets[size])
    
    test_set = create_test_pairs(celebrities, all_datasets.values(), test_size)
    random.shuffle(test_set)

    return all_datasets, test_set
