def jacard(txt1, txt2):
    words1 = set(txt1[0].split(' '))
    words2 = set(txt2[0].split(' '))
    return 1 - len(words1.intersection(words2)) / len(words1.union(words2))


def soronsen(txt1, txt2):
    words1 = set(txt1[0].split(' '))
    words2 = set(txt2[0].split(' '))
    return 1 - 2 * len(words1.intersection(words2)) / (len(words1) + len(words2))


def overlap(txt1, txt2):
    words1 = set(txt1[0].split(' '))
    words2 = set(txt2[0].split(' '))
    return 1 - len(words1.intersection(words2)) / (min(len(words1), len(words2)))
