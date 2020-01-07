#!/usr/bin/env python
# coding=utf-8
import numpy as np
import pytest
from loadsim.read_snap import ReadSnapshot


class TestsubGroup():
    def setup_method(self, method):
        self.rs = ReadSnapshot()

    def teardown_method(self):
        del self.rs

    def test_header(self):
        time = self.rs.header['time']
        redshift = self.rs.header['redshift']
        assert np.allclose(time, 1./(1.+redshift))

    def test_pos(self):
        self.rs.getheader(0)
        pos = self.rs.readpos(0)
        assert pos['x'].max() <= self.rs.header['BoxSize']
        assert pos['y'].max() <= self.rs.header['BoxSize']
        assert pos['z'].max() <= self.rs.header['BoxSize']
        assert pos['x'].min() >= 0.
        assert pos['y'].min() >= 0.
        assert pos['z'].min() >= 0.

    def test_vel(self):
        self.rs.getheader(0)
        vel = self.rs.readvel(0)
        assert vel['vx'].min() < 0.

    def test_mass(self):
        """check massvar particles number"""
        pass
