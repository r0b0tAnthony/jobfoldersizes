import scandir,re,os,sys,getopt,operator

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

def usage():
    print "-h\t\t\t\tPrint this help message"
    print "--root=\t\t\tSet the root directory which to traverse. Be sure to quote paths with spaces."
    print "--sort=\t\t\tHow the final results short be sorted"
    print "--filter=\t\tA Python regex needle to filter top directories in root directory. Be sure to quote filter."

if __name__ == "__main__":
    sort_opts = {
        'name': 'name',
        'size': 'size',
        'date': 'date',
        'none': 'none'
    }

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hrsf:d", ["help", "root=", "sort=", "filter="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    else:
        needle = ''
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage()
                sys.exit()
            elif opt == '-d':
                global _debug
                _debug = 1
            elif opt in ("-r", "--root"):
                root_dir = arg
            elif opt in ("-s", "--sort"):
                sort = sort_opts.get(arg, 'size')
            elif opt in ("-f", "--filter"):
                needle = arg
    jobs = {}
    p = re.compile(needle)

    if _debug:
        if scandir.scandir == getattr(scandir, 'scandir_c', None):
            print('Using fast C version of scandir')
        elif scandir.scandir == getattr(scandir, 'scandir_python', None):
            print('Using slower ctypes version of scandir')
        elif scandir.scandir == scandir.scandir_generic:
            print('Using very slow generic version of scandir')

    for top_dir in scandir.scandir(root_dir):
        if (top_dir.is_dir(follow_symlinks=False) and re.search(p, top_dir.name)) or (needle is None and top_dir.is_dir(follow_symlinks=False)):
            if _debug:
                print "Calculating Job Sizes For: %s" % top_dir.name
            size = get_tree_size(os.path.join(root_dir, top_dir.name))
            jobs[top_dir.name] = size
    if len(jobs) > 0:
        max_name = max(len(s) for s in  jobs.keys())
        row_format_tabbing = "{:<%d}" % (max_name + 10)
        row_format =row_format_tabbing * 2
        print row_format.format(*{'Job', 'Size'})

        if sort == 'name':
            for job in sorted(jobs.items(), key=lambda (k,v): (k.lower(), v)):
                print row_format.format(job[0], convert_bytes(job[1]))
        elif sort == 'size':
            for job in sorted(jobs.items(), key=operator.itemgetter(1), reverse=True):
                print row_format.format(job[0], convert_bytes(job[1]))
        else:
            for job in jobs:
                print row_format.format(job, convert_bytes(jobs[job]))
    else:
        print "No Jobs Found or No Jobs matching the filter '%s'" % needle
