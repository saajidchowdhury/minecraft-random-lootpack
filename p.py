#!/usr/bin/env python
"""\
This script creates the directory random_pack, which is a Minecraft datapack
where all the loot tables have been randomly permuted.
"""
import glob
import random
import shutil
import json

def f(x):
    if isinstance(x, list):
        ans = []
        for i in range(len(x)):
            if isinstance(x[i], dict):
                if "children" in x[i]:
                    for e in f(x[i]["children"]):
                        ans.append(e)
                else:
                    ans.append(f(x[i]))
            else:
                ans.append(f(x[i]))
    elif isinstance(x, dict): #assume that children is caught above, so x doesn't contain children
        ans = {}
        for key,value in x.items():
            if key != "conditions":
                ans[key] = f(value)
    else:
        ans = x
    return ans


#https://stackoverflow.com/questions/1883980/find-the-nth-occurrence-of-substring-in-a-string
def find_nth(haystack: str, needle: str, n: int) -> int:
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

shutil.unpack_archive("loot_table_original.zip")
pools = []
for path in glob.glob("loot_table_original/**/*.json", recursive=True):
    file = open(path, 'r')
    j = json.loads(file.read().rstrip())
    if "pools" in f(j):
        pools.append(f(j)["pools"])
    file.close()

shutil.unpack_archive("random_pack.zip")
random.shuffle(pools)
k = 0
for path in glob.glob("random_pack/**/*.json", recursive=True):
    file = open(path, 'r')
    j = json.loads(file.read().rstrip())
    if "pools" in j:
        j["pools"] = pools[k]
        k += 1
    file.close()
    file = open(path, 'w')
    file.write(json.dumps(j, indent=2))
    file.close()


