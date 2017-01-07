from os import listdir
from os import path
from os import makedirs
from os.path import isfile, join
import os
import sys
import shutil

def main():
    if len(sys.argv) != 1:
        rootDir = sys.argv[1]
        dir_count = 1
        onlyDir = [ name for name in listdir(rootDir) if path.isdir(path.join(rootDir, name)) ]
        for dirname in onlyDir:
            src = rootDir+"/"+dirname+"/processed/lexto"
            dest = rootDir+"/"+dirname

            if os.path.exists(src):
                shutil.move(src, dest)
            print "Processed %s\n" %(dirname)
            dir_count += 1

if __name__ == '__main__':
    main()
