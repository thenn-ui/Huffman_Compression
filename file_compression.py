# usage $ fcompress <input file name> <output filename>

import sys
from huffmantree import PriorityQueue as pqueue


MAX_FILE_READ_SIZE = 1500 # so that whole file is not read into memory at once

def compress():
    None


##  priority queue implementation goes here:

# convert tups to dict
def convert(tups, d):
    for a, b in tups:
        d[a] = b

def sort_dict(d):
    tups = sorted(d.items(), key=lambda x: x[1])
    sorted_dict = {}
    convert(tups, sorted_dict)
    return sorted_dict


def write_bindata(file, write_data):
    writebuff = bytes(write_data, 'utf-8')
    file.write(writebuff)

def write_data(file, write_data):
    file.write(write_data)


if __name__ == "__main__":
    n = len(sys.argv)

    if n < 3:
        print("Error: Check arguments to fcompress")
        exit(1)

    inputfilename = sys.argv[1]
    outputfilename = sys.argv[2]


    infhandle = open(inputfilename, 'r', encoding='utf-8')
    outfhandle = open(outputfilename, 'wb')

    read_data = infhandle.read(MAX_FILE_READ_SIZE)
    symbols = {}
    totalcharacters = 0
    while read_data:
        for i in range(0,len(read_data)):
            if read_data[i] in symbols:
                symbols[read_data[i]] += 1
            else:
                symbols[read_data[i]] = 1
            totalcharacters += 1

        read_data = infhandle.read(MAX_FILE_READ_SIZE)

    
    print(symbols)
    print(totalcharacters)
    #for key, value in symbols.items():
        #symbols[key] = symbols[key]/totalcharacters * 100

    symbols = sort_dict(symbols)

    print(symbols)

    print("Starting File Compression...")
    
