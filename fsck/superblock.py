import struct


class superBlock:
    BLOCK0_SIZE = 1024  # Number in byte of the block 0
    SUPERBLOCK_SIZE = 20  # Number in byte of data in the super block
    MINIX_LITTLE_ENDIAN_VALUE = 0x137f  # Minix filesystem v.1, value of little endian architecture
    endian = '<'  # by default little endian

    def __init__(self, img):
        img.seek(self.BLOCK0_SIZE + 16)
        self.endian = '<' if struct.unpack("<H", img.read(2))[0] == self.MINIX_LITTLE_ENDIAN_VALUE else '>'
        img.seek(self.BLOCK0_SIZE)

        self.ninodes, self.nzones, self.imap_blocks, self.zmap_blocks, self.firstdatazone, \
        self.log_zone_size, self.max_size, self.magic, self.size = struct.unpack(self.endian + "HHHHHHIHH", img.read(self.SUPERBLOCK_SIZE))

    def __str__(self):
        s = "---- SUPER BLOCK -----\n"
        s += "ninodes       : " + hex(self.ninodes) + "\n"
        s += "nzones        : " + hex(self.nzones) + "\n"
        s += "imap_blocks   : " + hex(self.imap_blocks) + "\n"
        s += "zmap_blocks   : " + hex(self.zmap_blocks) + "\n"
        s += "firstdatazone : " + hex(self.firstdatazone) + "\n"
        s += "log_zone_size : " + hex(self.log_zone_size) + "\n"
        s += "max_size      : " + hex(self.max_size) + "\n"
        s += "magic         : " + hex(self.magic) + "\n"
        s += "size          : " + hex(self.size) + "\n"
        return s
