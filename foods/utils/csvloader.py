"""
load csv file
"""

import csv
import os

def loadcsv(filename, field):
    firstRow = True
    index = 0
    result = []
    old = csv.field_size_limit(831072)
    if not os.path.isfile(filename):
        return result
    with open(filename , 'rb') as f:
        for line in csv.reader(f):
            if firstRow:
                firstRow = False
                index = line.index(field)
                print 'Find index %d' % index
                continue
            if (len(line)) < index:
                print 'error ' + " ".join(line)
                continue
            result.append(line[index])

    print 'All downloaded pages counts is %d'% len(result)
    return result
def filtercsv(filein,fileout,fields):
    firstRow = True
    index = []
    csv.field_size_limit(831072)
    if not os.path.isfile(filein):
        return
    with open(filein, 'rb') as fin:
        with open(fileout, 'wb') as fout:
            writer = csv.writer(fout)
            for line in csv.reader(fin):
                if firstRow:
                    firstRow = False
                    for field in fields:
                        index.append(line.index(field))
                    continue
                if (len(line) < max(index)):
                    print 'error ' + " ".join(line)
                    continue
                row = []
                for i in index:
                    row.append(line[i])
                # row = line[index]
                writer.writerow(row)






