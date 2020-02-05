# creates a training, testing, dev dataset

import random
import sys
import tqdm

filename = sys.argv[1]

sentences = []
sent = []
with open(filename, "r") as f:
    for line in tqdm.tqdm(f.readlines()):
        line = line.strip()
        if not line:
            if sent:
                sentences.append(list(sent))
                sent = []
            continue

        word, tag = line.split("\t")
        sent.append((word, tag))

random.shuffle(sentences)

x = 0.1
n = len(sentences)
offset = int(n * x)

dev = sentences[0:offset]
test = sentences[offset:offset*2]
train = sentences[offset*2:]

def write_sents(sents, f):
    for sent in sents:
        for word, tag in sent:
            f.write(f"{word} {tag}\n")
        f.write("\n")

for sents, name in [(dev, "dev"), (test, "test"), (train, "train")]:
    with open(f"{name}.txt", "w") as f:
        write_sents(sents, f)
        
