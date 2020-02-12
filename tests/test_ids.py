#!/usr/bin/env python
# coding=utf-8
import numpy as np
import pytest
from loadsim.read_ids import ReadIds


class TestsubGroup():
    def setup_method(self, method):
        self.rs = ReadIds('/home/mtx/work/tree/groups_066/subhalo_ids_066.')

    def teardown_method(self):
        del self.rs

    def test_fnr(self, submbid=12638380):
        self.rs.gen_sub_table()
        self.rs.get_fnr_ids()
        fnr = self.rs.get_par_files(submbid)
        sub = self.rs.subtable[submbid]
        sublen = sub['SubLen']
        suboff = sub['SubOffset']
        subend = suboff + sublen
        assert self.rs.NidOff[fnr] < suboff
        assert self.rs.NidOff[fnr] + self.rs.Nids[fnr] > subend

    def test_first_id_is_mostboundid(self, submbid=12638380):
        ids = self.rs.get_par_ids(submbid=submbid)
        assert ids[0] == submbid

    def test_ids_sublen(self, submbid=12638380):
        ids = self.rs.get_par_ids(submbid=submbid)
        assert ids.size == self.rs.subtable[submbid]['SubLen']

    def test_ids_shape(self, submbid=12638380):
        ids = self.rs.get_par_ids(submbid=submbid)
        assert ids.shape == (self.rs.subtable[submbid]['SubLen'])

    def test_ids_unique(self, submbid=12638380):
        ids = self.rs.get_par_ids(submbid=submbid)
        assert np.unique(ids).size == ids.size

    def test_sub_in_multiple_files_filenum(self):
        # submbid=8495089
        submbid = self.rs.Data_sub['SubMostBoundID'][0]
        fnrs = self.rs.get_par_files(submbid)
        assert fnrs.size > 1

    def test_sub_in_multiple_files_sublen(self):
        # submbid=8495089
        submbid = self.rs.Data_sub['SubMostBoundID'][0]
        sub = self.rs.subtable[submbid]
        print(sub.dtype)
        print(sub)
        ids = self.rs.get_par_ids(submbid=submbid)
        assert ids.size == sub['SubLen']

    def test_sub_in_multiple_files_mbid(self):
        # submbid=8495089
        submbid = self.rs.Data_sub['SubMostBoundID'][0]
        sub = self.rs.subtable[submbid]
        ids = self.rs.get_par_ids(submbid=submbid)
        assert ids[0] == submbid

    def test_sub_in_multiple_files_unique(self):
        # submbid=8495089
        submbid = self.rs.Data_sub['SubMostBoundID'][0]
        sub = self.rs.subtable[submbid]
        ids = self.rs.get_par_ids(submbid=submbid)
        assert np.unique(ids).size == ids.size
