#!/usr/bin/env python
# coding=utf-8
import numpy as np
from loadsim.read_subgroup import ReadSub


class ReadIds(ReadSub):
    def __init__(self, Base, *args, **kwargs):
        super(ReadIds, self).__init__(
            Base.replace("ids", "tab"), *args, **kwargs)
        self.dt_ids_header = np.dtype([
            ('Ngroups', np.int32, 1),
            ('TotNgroups', np.int32, 1),
            ('Nids', np.int32, 1),
            ('TotNids', np.int64, 1),
            ('NTask', np.int32, 1),
            ('Offset', np.int32, 1),
        ])
        self.LoadData()
        self.gen_sub_table()
        self.get_fnr_ids()

    def ids_getheader(self, fnr):
        self.ids_setbuf(fnr)
        with open(self.ids_buf, 'r') as f:
            self.ids_header = self.fromfile(
                f, dtype=self.dt_ids_header, count=1)[0]
            f.close()

    def ids_setbuf(self, fnr):
        self.ids_buf = self.Base.replace("tab", "ids") + "%d" % fnr

    def get_fnr_ids(self):
        self.ids_getheader(0)
        header = self.ids_header
        NTask = header['NTask']
        Nids = []
        NidOff = []
        for i in range(NTask):
            self.ids_getheader(i)
            header = self.ids_header
            Nids.append(header['Nids'])
            NidOff.append(header['Offset'])
        self.Nids = np.array(Nids)
        self.NidOff = np.array(NidOff)

    def gen_sub_table(self):
        self.subtable = dict(
            zip(self.Data_sub['SubMostBoundID'], self.Data_sub))

    def get_par_files(self, submbid=0):
        sub = self.subtable[submbid]
        sublen = sub['SubLen']
        suboff = sub['SubOffset']
        subend = suboff + sublen
        filenums = np.argwhere(
            ((self.NidOff+self.Nids) >= suboff)*(subend >= self.NidOff))
        filenums = np.squeeze(filenums)
        text = "finding mostbound ID {}... -> start id: {}; end id: {}.".format(
            submbid, suboff, subend)
        text2 = "get file number: {}, ids {}~{}".format(
            filenums, self.NidOff[filenums], self.NidOff[filenums]+self.Nids[filenums])
        print(text)
        print(text2)
        return filenums

    def get_par_ids(self, submbid=0):
        """
        FIXIT: one subhalo saved into two files? :finished
        """
        sub = self.subtable[submbid]
        sublen = sub['SubLen']
        suboff = sub['SubOffset']
        subend = suboff + sublen
        fnrs = self.get_par_files(submbid).flatten()
        ids = []
        for fnr in fnrs:
            loc_offset = max(0, suboff - self.NidOff[fnr])
            loc_len = min(subend - self.NidOff[fnr]-loc_offset,
                          self.Nids[fnr] - loc_offset)
            self.ids_setbuf(fnr)
            with open(self.ids_buf, 'r') as fp:
                self.ids_header = self.fromfile(
                    fp, dtype=self.dt_ids_header, count=1)[0]
                fp.seek(self.ids_header.nbytes+loc_offset*4, 0)
                ids.append(self.fromfile(fp, dtype=np.int32, count=loc_len))
                fp.close()
        ids = np.hstack(ids)
        print(ids, ids.shape)
        assert ids[0] == submbid, "The first id should be most bound id!"
        assert ids.size == sublen, "The length of particels should be equal to sublen!"
        return ids

    def __call__(self, submbid=7881425):
        # print("-"*10)
        # print(self.subtable[submbid])
        # print(self.subtable[submbid].dtype)
        return self.get_par_ids(submbid)


if __name__ == "__main__":
    rs = ReadIds('/home/mtx/work/tree/groups_066/subhalo_ids_066.')
    print(rs.header)
    print(rs.header.dtype)
    print("="*80)
    rs(12638380)
    rs()
