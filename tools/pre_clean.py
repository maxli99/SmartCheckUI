# -*- coding: utf-8 -*-
#!/user/bin/python
# -*- coding: utf-8 -*-
# Filename: cleanpyc.py
# Date:2011-03-26

import os
import fnmatch
import sys

def clearpyc(root, patterns='*.pyc',single_level=False, yield_folders=False):
    """
    root: 需要遍历的目录
    patterns： 需要查找的文件，以；为分割的字符串
    single_level: 是否只遍历单层目录，默认为否
    yield_folders: 是否包含目录本身，默认为否
    """
    patterns = patterns.split(';')
    for path, subdirs, files in os.walk(root):
        if yield_folders:
            files.extend(subdirs)
            files.sort()
        for name in files:
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern.strip()):# 去除pattern两端的空格
                    yield os.path.join(path, name)
        if single_level:
            break


if __name__ == '__main__':
    if 2 == len(sys.argv):
        pass
    else:
        sys.exit(0)

    directory = sys.argv[1]

    for path in clearpyc(directory,'*.pyc;*.pyo'):
        print path
        os.remove(path)
