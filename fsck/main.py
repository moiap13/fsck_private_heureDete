import file_system

if __name__ == '__main__':
    img_file_path = "../IMG//minixfs_lab1.img"
    fs = file_system.file_system(img_file_path)
    de = fs.get_dir_entry(1024*223+64)
    print(de)
    de = fs.get_inode(4)
    print(de)
    de = fs.browse_directory(1024*223)
    for de_2 in de:
        print(de_2)
    print "****************** \n\n\n\n\n "
    fs.browse_tree()