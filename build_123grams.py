#!/usr/bin/env python3
"""
    Project : Telugu OCR
    Author  : Rakeshvara Rao
    License : GNU GPL 3.0 or later

    This file outputs the trigram for given Telugu corpus.
    This uses module BantiParser
"""
import sys
import pickle
from collections import defaultdict, Counter
from text2glyphs import process_line

if len(sys.argv) < 2:
    print("""Usage:
        {0} out_file_prefix infile1 infile2 infile3 (etc.)
    Counts the unigram, bigram and trigram counts in the infiles and
    Writes them out to <out_file_prefix>.uni/bi/tri.pkl files.
    Also shows the counts in respective .txt files.
    """.format(sys.argv[0]))
    sys.exit()

out_file_prefix = sys.argv[1]

############################################# Build the dictionaries

beg_line, end_line = ' ', ' '
gram1 = Counter()
gram2 = defaultdict(Counter)
gram3 = defaultdict(lambda: defaultdict(Counter))

for txt_file_name in sys.argv[2:]:
    corpus = open(txt_file_name)
    iline = 0

    for line in corpus:
        line = beg_line + line.rstrip() + end_line
        glyps = process_line(line)

        for i in range(len(glyps)-2):
            a, b, c = glyps[i:i+3]
            gram1[a] += 1
            gram2[a][b] += 1
            gram3[a][b][c] += 1

        y, z = glyps[-2:]
        gram1[y] += 1
        gram1[z] += 1
        gram2[y][z] += 1

        iline += 1
        if iline % 1000 == 0:
            print(txt_file_name, iline)

    corpus.close()

############################################## Normalize
# Unigram
total = sum(gram1.values())
for a in gram1:
    gram1[a] /= total
gram1 = dict(gram1)

# Bigram
for a in gram2:
    total = sum(gram2[a].values())
    for b in gram2[a]:
        gram2[a][b] /= total
    gram2[a] = dict(gram2[a])

# Trigram
for a in gram3:
    for b in gram3[a]:
        total = sum(gram3[a][b].values())
        for c in gram3[a][b]:
            gram3[a][b][c] /= total
        gram3[a][b] = dict(gram3[a][b])


############################################## Dump Pickle
with open(out_file_prefix+'.uni.pkl', 'wb') as f:
    pickle.dump(dict(gram1), f)

with open(out_file_prefix+'.bi.pkl', 'wb') as f:
    pickle.dump(dict(gram2), f)

with open(out_file_prefix+'.tri.pkl', 'wb') as f:
    pickle.dump(dict(gram3), f)


############################################## Dump  txt
def sort(dic):
    return sorted(dic.items(),  key=lambda x: x[0])

# Unigram
with open(out_file_prefix+'.uni.txt', 'w') as funi:
    for a, count in sort(gram1):
        funi.write('\n{} : {}'.format(a, count))

# Bigram
with open(out_file_prefix+'.bi.txt', 'w') as fbi:
    for a, d in sort(gram2):
        fbi.write('\n{} {}: {}'.format('*'*40, a, len(d)))
        for b, count in sort(d):
            fbi.write('\n{} {} : {}'.format(a, b, count))

# Trigram
with open(out_file_prefix+'.tri.txt', 'w') as fout:
    for a, dd in sort(gram3):
        fout.write('\n\n{} {}: {}'.format('#'*60, a, len(dd)))
        for b, d in sort(dd):
            fout.write('\n{} {} {}: {}'.format('-'*30, a, b, len(d)))
            for c, count in sort(d):
                fout.write('\n{} {} {} : {:8.6f}'.format(a, b, c, count))