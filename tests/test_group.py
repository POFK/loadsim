#!/usr/bin/env python
# coding=utf-8
import numpy as np
import pytest
from loadsim.read_subgroup import ReadSub


class TestGroup():
    def setup_method(self, method):
        self.rs = ReadSub('/home/mtx/work/tree/groups_066/subhalo_tab_066.')

    def teardown_method(self):
        del self.rs

    def test_NTask(self):
        self.rs.getheader(0)
        NTask = self.rs.header['NTask']
        for i in range(NTask):
            self.rs.getheader(i)
            n = self.rs.header['NTask']
            assert n == NTask

    def test_Len_Offset_one(self):
        gr, sub = self.rs.LoadOneFile(0)
        offset = [gr['GroupOffset'][0]]
        [offset.append(offset[i]+gr['GroupLen'][i]) for i in range(len(gr)-1)]
        offset = np.array(offset)
        assert not np.any(offset-gr['GroupOffset'])

    def test_Len_Offset_one2(self):
        gr, sub = self.rs.LoadData(0)
        offset = [gr['GroupOffset'][0]]
        [offset.append(offset[i]+gr['GroupLen'][i]) for i in range(len(gr)-1)]
        offset = np.array(offset)
        assert not np.any(offset-gr['GroupOffset'])

    def test_Len_Offset_all(self):
        gr, sub = self.rs.LoadData()
        offset = [gr['GroupOffset'][0]]
        [offset.append(offset[i]+gr['GroupLen'][i]) for i in range(len(gr)-1)]
        offset = np.array(offset)
        assert not np.any(offset-gr['GroupOffset'])

    def test_pos_all(self):
        """for phoenix"""
        gr, sub = self.rs.LoadData()
        assert gr['GroupPos'].max() <= 500.
        assert gr['GroupPos'].min() >= 0.

    def test_Len_Offset_ids(self):
        gr, sub = self.rs.LoadData()
        gl = gr[-1]['GroupLen']
        go = gr[-1]['GroupOffset']
        Np = self.rs.header['TotNids']
        assert gl+go == Np
