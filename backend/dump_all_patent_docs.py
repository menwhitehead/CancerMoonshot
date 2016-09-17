import os
import os.path
import sys

import dump_patent_docs

directory = sys.argv[1]

for filename in os.listdir(directory):
    filename = directory + '/' + filename
    if os.path.isfile(filename) and filename[-4:] == ".xml":
        output_filename = filename[:-3] + "txt"
        print filename, output_filename
        dump_patent_docs.dumpPatentDocs(filename, output_filename)
