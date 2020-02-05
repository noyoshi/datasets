# inserts newlines into the bio dataset

import sys

def consume(lines, i):
    i += 1
    return i, lines[i-1]

filename = sys.argv[1]

sentences = []
sent = []
with open(filename, "r") as f:
    i = 0
    lines = f.readlines()
    while i < len(lines):
        i, line = consume(lines, i)
        word, tag = line.strip().split(" ")
        sent.append(word)
        if word == ".":
            sentences.append(list(sent))
            sent = []

print(len(sentences))

            # if sent[-1].isdigit() and i < len(lines) and lines[i].isdigit():
                # prev and next word are a number... odds 

