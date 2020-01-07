#!/usr/bin/env python
# coding=utf-8
import pytest
from loadsim.read_subgroup import ReadSub

rs = ReadSub('/home/mtx/work/tree/groups_066/subhalo_tab_066.')

def test_NTask():
    rs.getheader(0)
    NTask = rs.header['NTask']
    for i in range(NTask):
        rs.getheader(i)
        n = rs.header['NTask']
        assert n == NTask


def test_TotNgroups():
    rs.getheader(0)
    NTask = rs.header['NTask']
    TotNg = 0
    for i in range(NTask):
        rs.getheader(i)
        TotNg += rs.header['Ngroups']
    assert TotNg == rs.header['TotNgroups']


def test_TotNsubs():
    rs.getheader(0)
    NTask = rs.header['NTask']
    TotNsubs = 0
    for i in range(NTask):
        rs.getheader(i)
        TotNsubs += rs.header['Nsubgroups']
    assert TotNsubs == rs.header['TotNsubgroups']


def test_TotNids():
    rs.getheader(0)
    NTask = rs.header['NTask']
    TotNids = 0
    for i in range(NTask):
        rs.getheader(i)
        TotNids += rs.header['Nids']
    assert TotNids == rs.header['TotNids']


