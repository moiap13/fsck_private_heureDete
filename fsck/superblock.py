import struct


class superBlock:
    BLOCK0_SIZE = 1024  # Number in byte of the block 0
    SUPERBLOCK_SIZE = 20  # Number in byte of data in the super block
    MINIX_LITTLE_ENDIAN_VALUE = 0x137f  # Minix filesystem v.1, value of little endian architecture
    endian = '<'  # by default little endian

    def __init__(self, block_info):
        """
        ninodes: Total Number of i-nodes
        nzones:  Nombre de blocs total, tout compris, y compris bloc 0
        imap_blocks: Taille de la bitmap des inodes en blocs (I bitmap)
        zmap_blocks: Taille de la bitmap des zones libres/occupee en blocs (D bitmap)
        firstdatazone: Index du premier bloc avec des donnees (D)
        log_zone_size: taille d'un bloc donnees en octets = 1024*2s_log_zone_size
        max_size: Taille maximum d'un fichier en octets
        magic: 0x137f if big endian, else little endian
        size: a-t-il ete proprement demonte ?

        :param block_info: a tuple that contain all the values for the
        """
        self.ninodes, self.nzones, self.imap_blocks, self.zmap_blocks, self.firstdatazone, \
        self.log_zone_size, self.max_size, self.magic, self.size = block_info

    @classmethod
    def from_file(cls, img):
        """
        :param img: the file descriptor of the image
        :return: call the constructor with the created tuple
        """
        # read magic
        img.seek(cls.BLOCK0_SIZE + 16)

        magic = struct.unpack(cls.endian + "H", img.read(2))

        img.seek(cls.BLOCK0_SIZE)
        if magic[0] != cls.MINIX_LITTLE_ENDIAN_VALUE:
            cls.endian = '>'

        return cls(struct.unpack(cls.endian + "HHHHHHIHH", img.read(cls.SUPERBLOCK_SIZE)))


    def __str__(self):
        s = "==== SUPER BLOCK ====\n"
        s += "ninodes: " + hex(self.ninodes) + "\n"
        s += "nzones: " + hex(self.nzones) + "\n"
        s += "imap_blocks: " + hex(self.imap_blocks) + "\n"
        s += "zmap_blocks: " + hex(self.zmap_blocks) + "\n"
        s += "firstdatazone: " + hex(self.firstdatazone) + "\n"
        s += "log_zone_size: " + hex(self.log_zone_size) + "\n"
        s += "max_size: " + hex(self.max_size) + "\n"
        s += "magic: " + hex(self.magic) + "\n"
        s += "size: " + hex(self.size) + "\n"
        return s
