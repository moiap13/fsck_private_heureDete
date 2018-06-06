from __builtin__ import xrange

import superblock as s
import inode as i
import dir_entry as d
import bitarray


class file_system:
    DIRECTORY_TYPE = 0x4
    def __init__(self, image_path):
        self.image = open(image_path)
        self.sb = s.superBlock.from_file(self.image)
        print self.sb
        self.block_size = 1024 * 2 ** self.sb.log_zone_size
        self.inode_table_pos = (self.sb.imap_blocks + self.sb.zmap_blocks + 1) * self.block_size + self.sb.BLOCK0_SIZE
        self.inode_table = [self.get_inode(i) for i in xrange(1, self.sb.ninodes + 1)]
        self.inode_bitmap = self.get_inode_bitmap()
        self.block_bitmap = self.get_block_bitmap()


    @property
    def nb_allocated_inode(self):
        return self.inode_bitmap.count(1)

    @property
    def nb_allocated_block(self):
        return self.block_bitmap.count(1)

    def check_file_size(self):
        res = []
        for index, inode in enumerate(self.inode_table):
            if inode.size > self.sb.max_size:
                res = [(index+1, inode.size)]
        return res

    def get_inode(self, inode_number):
        address = self.inode_table_pos + (inode_number - 1) * i.inode.DATA_SIZE
        self.image.seek(address)
        return i.inode.from_file(self.image, self.sb.endian)

    def get_block(self, block_number):
        return block_number * self.block_size

    def get_dir_entry(self, address):
        self.image.seek(address)
        return d.dir_entry.from_file(self.image, self.sb.endian)

    def get_inode_bitmap(self):
        self.image.seek(self.get_block(2))
        ba = bitarray.bitarray(endian='little' if self.sb.endian == '<' else 'big')
        ba.fromfile(self.image, self.sb.ninodes / 8)
        return ba

    def get_block_bitmap(self):
        self.image.seek(self.get_block(2 + self.sb.imap_blocks))
        ba = bitarray.bitarray(endian='little' if self.sb.endian == '<' else 'big')
        ba.fromfile(self.image, self.sb.nzones / 8)
        return ba

    def browse_directory(self, address): # address must be the beginig of the block
        i = 2*2*d.dir_entry.DIR_ENTRY_SIZE # 1st 2 is for 2 * 16
        dir_entry_table = []
        dir_entry = self.get_dir_entry(address)
        current_dir_inode = self.get_inode(dir_entry.inode)
        while(i < current_dir_inode.size):
            new_address = address+i # 2 * dir_entry_size is for ignoring "." and ".."
            dir_entry = self.get_dir_entry(new_address)
            if(dir_entry.inode > 0):
                dir_entry_table.append(self.get_dir_entry(new_address))
            else:
                break
            i += 2*d.dir_entry.DIR_ENTRY_SIZE
        return dir_entry_table

    def is_directory(self, de):
        return self.get_inode(de.inode).file_type == i.inode.DIRECTORY

    t=0
    def browse_tree(self, address=1024*220):
        self.t+=1
        print("T : " + str(self.t) + "\n")

        if(self.t == 25):
            test = 1

        redirect = True
        for i in self.browse_directory(address):
            if self.is_directory(i):
                print "------ DIRECTORY ------"
                print(i)
                print "------------------------"
                inode = self.get_inode(i.inode)
                for y in inode.zone:
                    if y != 0:
                        self.browse_tree(y*1024)
                    else:
                        redirect = False
            else:
                print "------ NOT A DIRECTORY ------"
                print(i)
                print "-----------------------------"

    def statistics(self):
        print("number of allocated inodes: " + str(self.nb_allocated_inode))
        print("number of allocated blocks: " + str(self.nb_allocated_block))
        # print("number of inodes that have a name: ")
        # print("number of blocks used by inodes: ")

    def fsck(self):
        size_error = self.check_file_size()
        print("there are " + str(len(size_error)) + " files that are bigger than " + str(self.sb.max_size) + " byte")
        if len(size_error) > 0:
            for i in size_error:
                print("inode: " + str(i[0]) + " size: "+str(i[1]))

    def __str__(self):
        s = "bloc_size: " + str(self.block_size) + "\n"
        return s