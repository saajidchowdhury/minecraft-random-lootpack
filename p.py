"""
This script creates the directory random_pack, which is our custom Minecraft 1.21.11 datapack
where all the loot tables have been randomly permuted.
"""
import shutil
import glob
import json
import random


#Given loot_table json substructure x, f(x) returns x with all conditions removed
#and all children under alternatives listed directly as entries
def f(x):
    if isinstance(x, list):
        ans = []
        for xitem in x:
            if isinstance(xitem, dict) and "children" in xitem:
                for child in f(xitem["children"]):
                    ans.append(child)
            else:
                ans.append(f(xitem))
    elif isinstance(x, dict): #assume that children is caught above, so x doesn't contain children
        ans = {}
        for key,value in x.items():
            if key != "conditions":
                ans[key] = f(value)
    else:
        ans = x
    return ans


#Given the original Minecraft 1.21.11 loot_tables, extracts and applies f to all the pools
shutil.unpack_archive("loot_table_original.zip")
pools = []
for path in glob.glob("loot_table_original/**/*.json", recursive=True):
    file = open(path, 'r')
    j = json.loads(file.read().rstrip())
    if "pools" in f(j):
        pools.append(f(j)["pools"])
    file.close()


#Shuffles the pools and assigns them to all loot_table json files in our custom datapack, random_pack
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


print("Done.")


