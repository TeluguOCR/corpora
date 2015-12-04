#!/usr/bin/env python3

import os, sys, re

def unspace(text):
    """     Remove Arbitrary Spaces    """
    text = re.sub(r'  +',           ' ', text)
    text = re.sub(r'(?m)^ +',        '', text)
    text = re.sub(r'(?m) +$',        '', text)
    # text = re.sub(r'(?s)\n+',      '\n', text)
    return text

def remove_foreign(text):
    # text = re.sub(r'|', '।', text) # Remove pipes for danda
    # text = re.sub('॥',  '।।', text) # Double danta to two dandas
    # text = re.sub("ౘ", "చ", text)  
    # text = re.sub("ౙ", "జ", text)
    # text = re.sub("[–—]", "-", text)       # em, en dashes
    text = re.sub(r"[′‘’]", r"'", text)    # fancy single quotes
    text = re.sub(r'["“”″]', r'"', text)  # fancy double quotes
    text = re.sub(r'\u200D', '', text)
    text = re.sub(r'''[^ !(),\-.0-9=?'"ఁ-ఋఎ-్౦-౯।॥‌\n]''', " ", text)
    return unspace(text)

file_name = sys.argv[1]
with open("t" + file_name, 'w') as f:
    for line in open(file_name):
        line = remove_foreign(line)
        if line != '\n' and line != '':
            f.write(remove_foreign(line) )        
