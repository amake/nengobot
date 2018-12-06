from collections import defaultdict
import random
import cjkinfo

with open('nengo.tsv') as infile:
    tsv = infile.readlines()
data = {k: v.split(',')
        for k, v in (line.strip().split('\t') for line in tsv)}
chars = set(c for n in data.keys() for c in n)
chars_joyo = chars & set(cjkinfo.joyo)
initials_joyo = list(set(n[0] for n in data.keys()) & set(cjkinfo.joyo))
finals_joyo = list(set(n[1]
                       for n in data.keys() if len(n) == 2) & set(cjkinfo.joyo))
readings_initial = defaultdict(set)
readings_final = defaultdict(set)
for n, rs in data.items():
    if len(n) == 2:
        for r in rs:
            rleft, rright = r.split(' ')
            readings_initial[n[0]].add(rleft)
            readings_final[n[1]].add(rright)


def main():
    print('All nengo:', ','.join(data.keys()), '(%d)' % len(data))
    print('All chars:', ','.join(chars), '(%d)' % len(chars))
    print('All chars (joyo):', ','.join(chars_joyo), '(%d)' % len(chars_joyo))
    print('Initial chars (joyo):', ','.join(
        initials_joyo), '(%d)' % len(initials_joyo))
    print('Final chars (joyo):', ','.join(
        finals_joyo), '(%d)' % len(finals_joyo))
    print('Readings:', readings_initial, readings_final)
    for _ in range(0, 10):
        new_gengo, reading = generate()
        print(new_gengo, reading)


def romaji_initial(hira):
    return cjkinfo.hira2romaji[hira[0]][0]


romaji_blacklist = 'msth'


def generate():
    return do_gen(initials_joyo, finals_joyo, data.keys())


def do_gen(initials, finals, gold):
    while True:
        i = random.choice(initials)
        f = random.choice(finals)
        if i != f:
            cand = i + f
            reading = random.choice(
                list(readings_initial[i])) + random.choice(list(readings_final[f]))
            if cand not in gold and romaji_initial(reading) not in romaji_blacklist:
                return cand, reading


if __name__ == '__main__':
    main()
