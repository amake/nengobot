from collections import defaultdict
import random
import cjkinfo


def parse_tsv(path):
    with open(path) as infile:
        tsv = infile.readlines()
    return {fields[0]: fields[1].split(',')
            for fields in (line.strip().split('\t') for line in tsv)}


nengo_data = parse_tsv('nengo.tsv')
nengo_unused_data = parse_tsv('nengo-unused.tsv')
chars = set(c for data in [nengo_data, nengo_unused_data]
            for n in data.keys() for c in n)
chars_joyo = chars & set(cjkinfo.joyo)
initials = set(n[0] for data in [nengo_data, nengo_unused_data]
               for n in data.keys())
initials_joyo = list(initials & set(cjkinfo.joyo))
finals = set(n[1] for data in [nengo_data, nengo_unused_data]
             for n in data.keys() if len(n) == 2)
finals_joyo = list(finals & set(cjkinfo.joyo))
readings_initial = defaultdict(set)
readings_final = defaultdict(set)
for data in [nengo_data, nengo_unused_data]:
    for n, rs in data.items():
        if len(n) == 2:
            for r in rs:
                print(r)
                rleft, rright = r.split(' ')
                readings_initial[n[0]].add(rleft)
                readings_final[n[1]].add(rright)


def romaji_initial(hira):
    return cjkinfo.hira2romaji[hira[0]][0]


def map_kana(from_str, to_str, c):
    idx = from_str.index(c)
    return to_str[idx]


ha_gyo = u'はひふへほ'
pa_gyo = u'ぱぴぷぺぽ'


def get_reading(initial, final):
    i = random.choice(list(readings_initial[initial]))
    f = random.choice(list(readings_final[final]))
    # Hack to fix up 半濁音
    if f[0] in pa_gyo and i[-1] not in u'んっ':
        f = map_kana(pa_gyo, ha_gyo, f[0]) + f[1:]
    if f[0] in ha_gyo and i[-1] in u'んっ':
        f = map_kana(ha_gyo, pa_gyo, f[0]) + f[1:]
    return i + f


romaji_blacklist = 'msth'


def generate():
    while True:
        i = random.choice(initials_joyo)
        f = random.choice(finals_joyo)
        if i != f:
            cand = i + f
            reading = get_reading(i, f)
            if cand not in nengo_data and romaji_initial(reading) not in romaji_blacklist:
                return cand, reading


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


if __name__ == '__main__':
    main()
