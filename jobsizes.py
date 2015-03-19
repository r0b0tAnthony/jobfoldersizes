import scandir,re,os
p = re.compile(ur'^\d{5}')

def convert_bytes(bytes):
        bytes = float(bytes)
        if bytes >= 1099511627776:
            terabytes = bytes / 1099511627776
            size = '%.2fT' % terabytes
        elif bytes >= 1073741824:
            gigabytes = bytes / 1073741824
            size = '%.2fG' % gigabytes
        elif bytes >= 1048576:
            megabytes = bytes / 1048576
            size = '%.2fM' % megabytes
        elif bytes >= 1024:
            kilobytes = bytes / 1024
            size = '%.2fK' % kilobytes
        else:
            size = '%.2fb' % bytes
        return size

def get_tree_size(path):
    """Return total size of all files in directory tree at path."""
    size = 0
    try:
        for entry in scandir.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                size += get_tree_size(os.path.join(path, entry.name))
            else:
                size += entry.stat(follow_symlinks=False).st_size
    except OSError:
        pass
    return size

root_dir = '/mnt/server01_jobs'

for entry in scandir.scandir(root_dir):
    if entry.is_dir(follow_symlinks=False) and re.search(p, entry.name):
        print "Calculating Job Sizes For: %s" % entry.name
        size = get_tree_size(os.path.join(root_dir, entry.name))
        print convert_bytes(size)
