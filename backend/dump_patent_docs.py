import unicodedata
from bs4 import BeautifulSoup
import dataset_preprocessor
import sys

def tidyHTML(txt):
    soup = BeautifulSoup(txt)
    result = soup.text.encode('utf-8')
    result = dataset_preprocessor.process(result)
    return result


def dumpPatentDocs(filename, output_filename):
    start_tag = '''<?DETDESC description="Detailed Description" end="lead"?>'''
    end_tag = '''<?DETDESC description="Detailed Description" end="tail"?>'''

    inside = False
    curr_text = ''

    f = open(filename, 'r')
    o = open(output_filename, 'w')
    count = 1
    for line in f:
        if line.strip() == start_tag:
            inside = True
        elif line.strip() == end_tag:
            inside = False
            r = tidyHTML(curr_text)
            if len(r.strip()) > 0:
                o.write(r + "\n")
            curr_text = ''
            if count % 100 == 0: print "COUNT: ", count
            count += 1
        else:
            if inside:
                curr_text += line.strip() + " "

    o.close()
    f.close()


if __name__ == "__main__":
    filename = sys.argv[1]
    output_filename = sys.argv[2]
    dumpPatentDocs(filename, output_filename)
