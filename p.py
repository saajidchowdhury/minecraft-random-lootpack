#!/usr/bin/env python
"""\
This script creates the directory random_pack, which is a Minecraft datapack
where all the loot tables have been randomly permuted.
"""
import glob
import random
import shutil

#https://stackoverflow.com/questions/1883980/find-the-nth-occurrence-of-substring-in-a-string
def find_nth(haystack: str, needle: str, n: int) -> int:
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

shutil.unpack_archive("loot_table_original.zip")
items = []
for path in glob.glob('loot_table_original/**/*.json', recursive=True):
    file = open(path, 'r')
    for line in file:
        s = line.rstrip()
        if '\"name\": \"minecraft:' in s:
            i = find_nth(s, '\"', 3) + 1
            j = find_nth(s, '\"', 4) - 1
            items.append(s[i:j+1])
            print(s[i:j+1])
    file.close()

shutil.unpack_archive("random_pack.zip")
random.shuffle(items)
k = 0
for path in glob.glob('random_pack/**/*.json', recursive=True):
    file = open(path, 'r')
    contents = ""
    for line in file:
        s = line
        if '\"name\": \"minecraft:' in s:
            i = find_nth(s, '\"', 3) + 1
            j = find_nth(s, '\"', 4) - 1
            s = s[0:i] + items[k] + s[j+1:]
            k += 1
        contents += s
    file.close()
    file = open(path, 'w')
    file.write(contents)
    file.close()


