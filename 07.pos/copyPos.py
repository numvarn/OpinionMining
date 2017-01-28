import sys
import shutil
from os import listdir, path, makedirs
from os.path import isfile, join

def main():
    if len(sys.argv) > 1:
        rootDir = sys.argv[1]
        sourcePath = rootDir+"/rawData"
        # destPath = rootDir+"/filtered-pos"
        
        destPath = '/Volumes/PHISAN_HD/filtered-pos'

        if not path.exists(destPath):
            makedirs(destPath)

        onlyDir = [ name for name in listdir(sourcePath) \
                            if path.isdir(path.join(sourcePath, name)) ]

        file_count = 0
        dir_count = 0
        for dirname in onlyDir:
            pos_filetered_dir = sourcePath+"/"+dirname+"/filtered-pos"
            if path.exists(pos_filetered_dir):
                onlyfiles = [f for f in listdir(pos_filetered_dir) \
                            if isfile(join(pos_filetered_dir, f))]

                dir_count += 1
                for filename in onlyfiles:
                    file_count += 1
                    srcfile = pos_filetered_dir+"/"+filename
                    print "#%d copying file %s :: %s" %(file_count, dirname, filename)
                    shutil.copy(srcfile, destPath)

if __name__ == '__main__':
    main()
