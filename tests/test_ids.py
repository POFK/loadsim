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

    def test_sub_in_two_files(self, submbid=12638380):
        pass
