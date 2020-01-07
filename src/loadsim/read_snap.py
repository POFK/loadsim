#!/usr/bin/env python
# coding=utf-8
import numpy as np


class ReadSnapshot(object):
    """
    A script for reading L-Gadget format data. More details see 
    https://wwwmpa.mpa-garching.mpg.de/gadget/users-guide.pdf
    """

    def __init__(self, snap_base='/home/mtx/work/tree/snapdir_066/snap_066.'):
        self.Base = snap_base
        self.dt_header = np.dtype([('head', np.int32, 1),
                                   ('npar', np.int32, 6),
                                   ('massarr', np.float64, 6),
                                   ('time', np.float64),
                                   ('redshift', np.float64),
                                   ('flag_sfr', np.int32),
                                   ('flag_feedback', np.int32),
                                   ('npartall', np.int32, 6),
                                   ('flag_cooling', np.int32),
                                   ('Nsubfiles', np.int32),
                                   ('BoxSize', np.float64),
                                   ('Omega0', np.float64),
                                   ('OmegaL', np.float64),
                                   ('H', np.float64),
                                   ])
        self.getheader(0)
        print("reading header: {} ...\n{}\n{}\n".format(
            self.buf, self.header, self.header.dtype))

    def setbuf(self, fnr):
        self.buf = self.Base + "%d" % fnr

    def getheader(self, fnr):
        self.setbuf(fnr)
        with open(self.buf, 'r') as fp:
            self.header = np.fromfile(fp, dtype=self.dt_header, count=1)[0]
            fp.close()
        self.npar = self.header['npar']
        self.massarr = self.header['massarr']
        self.Nsubfiles = self.header['Nsubfiles']

    def skipblock(self, fp):
        buf = np.fromfile(fp, dtype=np.int32, count=1)[0]
        skip = buf+4
        fp.seek(fp.tell()+skip)

    def readpos(self, fnr):
        dt = np.dtype([
            ('x', np.float32, 1),
            ('y', np.float32, 1),
            ('z', np.float32, 1),
        ])
        with open(self.buf, 'r') as fp:
            self.skipblock(fp)  # skip header
            length = self.npar.sum()
            buf1 = np.fromfile(fp, dtype=np.int32, count=1)[0]
            pos = np.fromfile(fp, dtype=dt, count=self.npar.sum())
            buf2 = np.fromfile(fp, dtype=np.int32, count=1)[0]
            assert buf1 == buf2
            assert buf1 == length*3*4
            fp.close()
        return pos

    def readvel(self, fnr):
        dt = np.dtype([
            ('vx', np.float32, 1),
            ('vy', np.float32, 1),
            ('vz', np.float32, 1),
        ])
        with open(self.buf, 'r') as fp:
            self.skipblock(fp)  # skip header
            self.skipblock(fp)  # skip position
            length = self.npar.sum()
            buf1 = np.fromfile(fp, dtype=np.int32, count=1)[0]
            vel = np.fromfile(fp, dtype=dt, count=self.npar.sum())
            buf2 = np.fromfile(fp, dtype=np.int32, count=1)[0]
            assert buf1 == buf2
            assert buf1 == length*3*4
            fp.close()
        return vel

    def readids(self, fnr):
        with open(self.buf, 'r') as fp:
            self.skipblock(fp)  # skip header
            self.skipblock(fp)  # skip position
            self.skipblock(fp)  # skip velocity
            length = self.npar.sum()
            buf1 = np.fromfile(fp, dtype=np.int32, count=1)[0]
            ids = np.fromfile(fp, dtype=np.int32, count=self.npar.sum())
            buf2 = np.fromfile(fp, dtype=np.int32, count=1)[0]
            assert buf1 == buf2
            assert buf1 == length*4
            fp.close()
        return ids

    def readmass(self, fnr):
        a = self.npar
        b = self.massarr
        bool_var = (a > 0) ^ (b > 0)
        bool_not_var = np.logical_not(bool_var)
        offset = self.npar[bool_not_var].sum()
        length = self.npar[bool_var].sum()
        massarr = np.zeros(shape=[self.npar.sum()], dtype=np.float32)
        with open(self.buf, 'r') as fp:
            self.skipblock(fp)  # skip header
            self.skipblock(fp)  # skip position
            self.skipblock(fp)  # skip velocity
            self.skipblock(fp)  # skip id
            buf1 = np.fromfile(fp, dtype=np.int32, count=1)[0]
            mass = np.fromfile(fp, dtype=np.float32, count=length)
            buf2 = np.fromfile(fp, dtype=np.int32, count=1)[0]
            assert buf1 == buf2
            assert buf1 == length*4
            fp.close()
        start = 0
        start_var = 0
        for i in range(len(self.npar)):
            if self.npar[i] == 0:
                continue
            if bool_not_var[i]:
                massarr[start:start+self.npar[i]] = self.massarr[i]
            else:
                massarr[start:start+self.npar[i]
                        ] = mass[start_var:start_var+self.npar[i]]
                start_var += self.npar[i]
            start += self.npar[i]
        """
        for i in self.npar:
            s = marr[start:start+i]
            print(s.shape, s)
            start+=i
        """
        return massarr

    def __call__(self):
        pos = []
        vel = []
        ids = []
        marr = []
        for fnr in range(self.header['Nsubfiles']):
            self.getheader(fnr)
            pos.append(self.readpos(fnr))
            vel.append(self.readvel(fnr))
            ids.append(self.readids(fnr))
            marr.append(self.readmass(fnr))
        pos = np.hstack(pos)
        vel = np.hstack(vel)
        ids = np.hstack(ids)
        marr = np.hstack(marr)
        return ids, pos, vel, marr


if __name__ == '__main__':
    rs = ReadSnapshot()
    rs()
