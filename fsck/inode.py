import datetime
import struct


class inode:
    DIRECTORY = 0x4
    DATA_SIZE = 32  # size of 1 element of the inode table
    ZONE_ARRAY_SIZE = 7  # size of the zone array

    def __init__(self, inode_info):
        """
        :param inode_info: tuple that contain all the informations
        """
        self.zone = [None] * self.ZONE_ARRAY_SIZE

        self.mode, self.uid, self.size, self.time, self.gid, self.nlinks, \
        self.zone[0], self.zone[1], self.zone[2], self.zone[3], self.zone[4], self.zone[5], self.zone[6], \
        self.indr_zone, self.dbl_indr_zone = inode_info
        self.file_type = self.mode >> 12

    @classmethod
    def from_file(cls, img, endian):
        """
        :param img: the file descriptor of the image
        :param endian: the endianness
        :return: a tuple to the constructor
        """
        return cls(struct.unpack(endian + "HHIIBB%dHHH" % (cls.ZONE_ARRAY_SIZE), img.read(cls.DATA_SIZE)))

    def __str__(self):
        s = "mode: " + hex(self.mode) + "\n"
        s += "file type: " + hex(self.file_type) + "\n"
        s += "uid: " + hex(self.uid) + "\n"
        s += "size: " + hex(self.size) + "\n"
        s += "time: " + str(datetime.datetime.fromtimestamp(self.time)) + "\n"
        s += "gid: " + hex(self.gid) + "\n"
        s += "nlinks: " + hex(self.nlinks) + "\n"
        s += "zones: " + str(self.zone) + "\n"
        s += "indr_zone: " + hex(self.indr_zone) + "\n"
        s += "dbl_indr_zone: " + hex(self.dbl_indr_zone) + "\n"
        return s
