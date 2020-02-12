#!/usr/bin/env python
# coding=utf-8

import numpy as np


class ReadSub(object):
    def __init__(self, Base, *args, **kwargs):
        self.Base = Base
        self.IsByteswap = False
        if "IsByteswap" in kwargs:
            self.IsByteswap = True
        self.offset_gr = 0
        self.offset_sub = 0
        self.SetDtype(1, 1)
        self.getheader(0)
        self.Data_gr = np.empty(
            shape=self.header['TotNgroups'], dtype=self.dt_group)
        self.Data_sub = np.empty(
            shape=self.header['TotNsubgroups'], dtype=self.dt_sub)

    def fromfile(self, fp, dtype, count=-1):
        """TODO: Docstring for fromfile.
        :fp: TODO
        :dtype: TODO
        :count: TODO
        :returns: TODO
        """
        if self.IsByteswap:
            return np.fromfile(fp, dtype=dtype, count=count).byteswap()
        else:
            return np.fromfile(fp, dtype=dtype, count=count)

    def getheader(self, fnr):
        self.setbuf(fnr)
        with open(self.buf, 'r') as f:
            self.header = self.fromfile(f, dtype=self.dt_header, count=1)[0]
            f.close()

    def setbuf(self, fnr):
        self.buf = self.Base + "%d" % fnr

    def SetDtype(self, Ngroups, Nsubgroups):
        vector_gr = [Ngroups, 3]
        vector_sub = [Nsubgroups, 3]
        if Ngroups == 1:
            vector_gr.pop(0)
        if Nsubgroups == 1:
            vector_sub.pop(0)

        self.dt_header = np.dtype([
            ('Ngroups', np.int32, 1),
            ('TotNgroups', np.int32, 1),
            ('Nids', np.int32, 1),
            ('TotNids', np.int64, 1),
            ('NTask', np.int32, 1),
            ('Nsubgroups', np.int32, 1),
            ('TotNsubgroups', np.int32, 1),
        ])

        self.dt_group = np.dtype([
            ('GroupLen', np.int32, Ngroups),
            ('GroupOffset', np.int32, Ngroups),
            ('GroupMass', np.float32, Ngroups),
            ('GroupPos', np.float32, vector_gr),
            ('Group_M_Mean200', np.float32, Ngroups),
            ('Group_R_Mean200', np.float32, Ngroups),
            ('Group_M_Crit200', np.float32, Ngroups),
            ('Group_R_Crit200', np.float32, Ngroups),
            ('Group_M_TopHat200', np.float32, Ngroups),
            ('Group_R_TopHat200', np.float32, Ngroups),
            #           ('Group_VelDisp_Mean200', np.float32, Ngroups),
            #           ('Group_VelDisp_Crit200', np.float32, Ngroups),
            #           ('Group_VelDisp_TopHat200', np.float32, Ngroups),
            ('GroupContaminationCount', np.int32, Ngroups),
            ('GroupContaminationMass', np.float32, Ngroups),
            ('GroupNsubs', np.int32, Ngroups),
            ('GroupFirstSub', np.int32, Ngroups),
        ])

        self.dt_sub = np.dtype([
            ('SubLen', np.int32, Nsubgroups),
            ('SubOffset', np.int32, Nsubgroups),
            ('SubParentHalo', np.int32, Nsubgroups),
            ('SubhaloMass', np.float32, Nsubgroups),
            ('SubPos', np.float32, vector_sub),
            ('SubVel', np.float32, vector_sub),
            ('SubCM', np.float32, vector_sub),
            ('SubSpin', np.float32, vector_sub),
            ('SubVelDisp', np.float32, Nsubgroups),
            ('SubVmax', np.float32, Nsubgroups),
            ('SubVmaxRad', np.float32, Nsubgroups),
            ('Subhalfmass', np.float32, Nsubgroups),
            ('SubMostBoundID', np.int32, Nsubgroups),
            ('SubGrNr', np.int32, Nsubgroups),
        ])

    def LoadGr(self, fp):
        if self.header['Ngroups'] > 0:
            Data_gr = self.fromfile(fp, dtype=self.dt_group, count=1)[0]
            for name in self.dt_group.names:
                self.Data_gr[name][self.offset_gr:self.offset_gr +
                                   self.header['Ngroups']] = Data_gr[name][:]
            return self.Data_gr[self.offset_gr:self.offset_gr+self.header['Ngroups']]
        else:
            return 0

    def LoadSub(self, fp):
        if self.header['Nsubgroups'] > 0:
            Data_sub = self.fromfile(fp, dtype=self.dt_sub, count=1)
            for name in self.dt_sub.names:
                #   print(name, self.offset_sub, self.header['Nsubgroups'], Data_sub[name].shape)
                self.Data_sub[name][self.offset_sub:self.offset_sub + self.header['Nsubgroups']] = Data_sub[name]
            return self.Data_sub[self.offset_sub:self.offset_sub+self.header['Nsubgroups']]
        else:
            return 0

    def LoadOneFile(self, fnr):
        self.getheader(fnr)
        Ngroups = self.header['Ngroups']
        Nsubgroups = self.header['Nsubgroups']
        #print('reading file {}: group, {}; subgroup, {}'.format(self.buf, Ngroups, Nsubgroups))
        with open(self.buf, 'r') as fp:
            _ = self.fromfile(fp, dtype=self.dt_header, count=1)[0]
            self.SetDtype(Ngroups, Nsubgroups)
            gr = self.LoadGr(fp)
            sub = self.LoadSub(fp)
            fp.close()
        self.offset_gr += Ngroups
        self.offset_sub += Nsubgroups
        return gr, sub

    def LoadData(self, num=None):
        """TODO: Docstring for fromfile.
        FIXIT: reconstruct it later.
        :num: int or None.
        """
        print('reading file {}, {}'.format(self.Base, num))
        if num is None:
            num = range(self.header['NTask'])
            for fnr in num:
                self.LoadOneFile(fnr)
            return self.Data_gr, self.Data_sub
        else:
            return self.LoadOneFile(num)


if __name__ == "__main__":
    rs = ReadSub('/home/mtx/work/tree/groups_066/subhalo_tab_066.')
    fnr = 0
    rs.getheader(fnr)
    print(rs.header)
    print(rs.header.dtype)
    print("="*80)
    gr, sub = rs.LoadData()
    #gr, sub = rs.LoadData(0)
    print(gr.dtype, gr.shape)
    print(sub.dtype, sub.shape)
    print(sub['SubhaloMass'][:10],sub['SubMostBoundID'][:10])
    print("="*80)
