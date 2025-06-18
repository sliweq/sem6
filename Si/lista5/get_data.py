def get_celebrities():
    img_dir = "img_align_celeba"
    identity_file = "identity_CelebA.txt"

    with open(identity_file, 'r') as f:
        lines = f.readlines()

    celebrities = {}

    for i in lines:
        record = i.strip().split(" ")
        if celebrities.get(record[1]) is None:
            celebrities[record[1]] = []
        celebrities[record[1]].append(record[0])
    
    return celebrities
