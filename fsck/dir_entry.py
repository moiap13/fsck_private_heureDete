import struct


class dir_entry:
    MINIX_NAME_LEN = 14  # size of a string that contain a directory name
    DIR_ENTRY_SIZE = 16

    def __init__(self, entry):
        self.inode, temp_name = entry
        # remove the \0 characters
        self.name = "".join(c for c in temp_name if c != '\x00')


    @classmethod
    def from_file(cls, img, endian):
        return cls(struct.unpack(endian + "H%ds" % cls.MINIX_NAME_LEN, img.read(cls.DIR_ENTRY_SIZE)))

    def __str__(self):
        s = "inode: " + hex(self.inode) + "\n"
        s += "name: " + self.name + "\n"
        return s
