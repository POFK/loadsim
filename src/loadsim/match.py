#!/usr/bin/env python
# coding=utf-8
import numpy as np

from loadsim.read_snap import ReadSnapshot
from loadsim.read_ids import ReadIds

snapnum = 66
mostboundids = [12638380, 7881425]

# get subhalo particles by MostBoundID
rid = ReadIds('/home/mtx/work/tree/groups_066/subhalo_ids_066.')
subids = {}
for mid in mostboundids:
    subids[mid] = rid(mid)
#print(subids)

# read all particles from snapshot files
rs = ReadSnapshot(snap_base='/home/mtx/work/tree/snapdir_066/snap_066.')
ids, pos, vel, marr = rs()

# generage hash table
Pars = {}
for ind in range(len(ids)):
    Pars[ids[ind]] = ind

# match subhalo 12638380
print("="*80)
mbid = 12638380
print(rid.subtable[mbid])
print(rid.subtable[mbid].dtype)
index = []
for i in subids[mbid]:
    index.append(Pars[i])
par_pos = pos[index]
sub_mass = marr[index]
print(np.sum(sub_mass.astype(np.float64)))
np.save('test.npy', par_pos)
