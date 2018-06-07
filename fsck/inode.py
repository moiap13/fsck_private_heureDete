import datetime
import struct
import superblock


class inode:
    DIRECTORY = 0x4 # Id for directory
    DATA_SIZE = 32  # Inode size
    ZONE_ARRAY_SIZE = 7 # constant of the array zone

    def __init__(self, img, endian, nb_inode = 0):
        self.nb_inode = nb_inode
        self.zone = [None] * self.ZONE_ARRAY_SIZE

        self.mode, self.uid, self.size, self.time, self.gid, self.nlinks, \
        self.zone[0], self.zone[1], self.zone[2], self.zone[3], self.zone[4], self.zone[5], self.zone[6], \
        self.indr_zone, self.dbl_indr_zone = struct.unpack(endian + "HHIIBB%dHHH" % (self.ZONE_ARRAY_SIZE), img.read(self.DATA_SIZE)) # initialize the classe variables
        self.file_type = self.mode >> 12 # decale and read the first 4 firsts bits (16-12=4)

    def __str__(self):
        print(self.nb_inode)

        if (self.nb_inode>0):
            s = "----- INODE N0 " + str(self.nb_inode) + " -----\n"

        s += "mode          : " + hex(self.mode) + "\n"
        s += "file type     : " + hex(self.file_type) + "\n"
        s += "uid           : " + hex(self.uid) + "\n"
        s += "size          : " + hex(self.size) + "\n"
        s += "time          : " + str(datetime.datetime.fromtimestamp(self.time)) + "\n"
        s += "gid           : " + hex(self.gid) + "\n"
        s += "nlinks        : " + hex(self.nlinks) + "\n"
        s += "zones         : " + str(self.zone) + "\n"
        s += "indr_zone     : " + hex(self.indr_zone) + "\n"
        s += "dbl_indr_zone : " + hex(self.dbl_indr_zone) + "\n"
        return s
