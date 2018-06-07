import struct

class dir_entry:
    MINIX_NAME_LEN = 14 # size name constant
    DIR_ENTRY_SIZE = 16 # size dir_entry minix 1.0 32 bytes for minix 

    def __init__(self, img, endian):
        self.inode, self.name = struct.unpack(endian + "H%ds" % self.MINIX_NAME_LEN, img.read(self.DIR_ENTRY_SIZE))
        self.name = "".join(c for c in self.name if c != '\x00')

    def __str__(self):
        return "inode   : " + hex(self.inode) + "\nname    : " + self.name + "\n"
