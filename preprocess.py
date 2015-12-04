import re
import sys

corpus_name = sys.argv[1]
corpus =  open(corpus_name)

exp = r"^(?:\w+\.)+\w+\s+\d\d\d\d/\d\d/\d\d\s+\d\s+\d\s+(.+)"
exp = re.compile(exp)

counts = {}

with open(sys.argv[1][:-4] + '_clean.txt', 'w') as fout:
	for line in corpus:
		match = exp.match(line)
		fout.write(match.group(1)+'\n')