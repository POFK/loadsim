#!/usr/bin/env python
# coding=utf-8
import numpy as np
import pytest
from loadsim.read_subgroup import ReadSub


class TestsubGroup():
    def setup_method(self, method):
        self.rs = ReadSub('/home/mtx/work/tree/groups_066/subhalo_tab_066.')

    def teardown_method(self):
        del self.rs

    def test_pos_all(self):
         """for phoenix"""
         gr, sub = self.rs.LoadData()
         assert sub['SubPos'].max() <= 500.
         assert sub['SubPos'].min() >= 0.

