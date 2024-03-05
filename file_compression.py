# usage $ fcompress <input file name> <output filename>
import sys
import math
import os
from queue import PriorityQueue as pqueue


MAX_FILE_READ_SIZE = 1500 # so that whole file is not read into memory at once
READMODE = 'r'
WRITEMODE = 'w'
BWRITEMODE = 'wb'

#Global variables
symbols={}
totalcharacters = 0

class Symbol:
    sid = None
    sfreq = None
    lchild = None
    rchild = None
    scode = None
    parent = None
    insymbolset = None

    def get_mappings(self):
        node = self
        mappings = {}
        q = []
        q.append(node)

        while(q != []):
            node = q.pop(0)
            if node.insymbolset:
                mappings[node.sid] = node.scode

            if node.lchild is not None:
                q.append(node.lchild)

            if node.rchild is not None:
                q.append(node.rchild)

        return mappings
   
    def get_encoded_tree(self):

        node = self
        encodedstring = ''
        
        q = []
        q.append(node)

        while(q != []):
            node = q.pop(0)
            if node.insymbolset:
                encodedstring = encodedstring + repr(node.sid) + ':' + node.scode + '|'

            if node.lchild is not None:
                q.append(node.lchild)

            if node.rchild is not None:
                q.append(node.rchild)

        return encodedstring
        
    def update_codes(self, node): #PLR traversal
        if node is None:
            return

        if node.parent is not None:
            node.scode = node.parent.scode + node.scode

        self.update_codes(node.lchild)
        self.update_codes(node.rchild)

    def __init__(self, name, freq, isinset):
        self.sid = name
        self.sfreq = freq
        self.lchild = None
        self.rchild = None
        self.scode = ''
        self.insymbolset = isinset

    def set_lchild(self, lch):
        self.lchild = lch
        lch.scode = "0"

    def set_rchild(self, rch):
        self.rchild = rch
        rch.scode = "1"

    def set_parent(self, par):
        self.parent = par

    def __lt__(self, other):
        return self.sfreq < other.sfreq

    def print_tree(self, node):

        if node.lchild is not None:
            self.print_tree(node.lchild)

        if node.insymbolset:
            print(repr(node.sid), node.sfreq, node.scode)

        if node.rchild is not None:
            self.print_tree(node.rchild)

def compress(infile, outfile):
    
    huffmantree = construct_huffman_tree(infile)

    print("Starting File Compression...")

    while(huffmantree.qsize() > 1):
        s1 = huffmantree.get()
        s2 = huffmantree.get()

        s3 = Symbol('sym', s1.sfreq + s2.sfreq, False)
        s3.set_lchild(s1)
        s3.set_rchild(s2)
        s1.set_parent(s3)
        s2.set_parent(s3)

        huffmantree.put(s3)

    tree = huffmantree.get()
    tree.update_codes(tree)
    #tree.print_tree(tree)

    enctree = tree.get_encoded_tree()
    treesize = len(enctree)

    size = treesize + get_compressed_file_expected_length(tree) + 2 + len(str(abs(treesize)))
    print("Expected Compressed bytes = ", size) 

    realsize = len(str(abs(treesize))) + 1
    realsize += treesize

    outfhandle.write((str(treesize) + '|').encode('latin-1'))
    outfhandle.write(enctree.encode('latin-1'))

    mappings = tree.get_mappings()

    #print(mappings)

    encstr = ''

    infhandle.seek(0)
    read_data = infhandle.read(MAX_FILE_READ_SIZE)

    while read_data:
        for i in range(0,len(read_data)):
            encstr = encstr + mappings[read_data[i]]

        read_data = infhandle.read(MAX_FILE_READ_SIZE)

    bytestr = get_byte_encoded_str(encstr)
    realsize += len(bytestr)
    print("Final calculated size = ", realsize)
    outfhandle.write(bytestr.encode('latin-1')) 

def get_compressed_file_expected_length(tree):
    global symbols, totalcharacters
    mappings = tree.get_mappings()
    totalbits = 0
    for key, value in mappings.items():
        symbol_count = symbols[key]/100 * totalcharacters
        numbits = len(value)
        totalbits += numbits*symbol_count
        #print("symbol - ", key, "bits used - ", numbits, "freq - ", symbol_count, "total chars - ", totalcharacters)

    return totalbits/8

def convert_str_to_byte(bitstr):
    bits = 0x0
    for i in range(0, len(bitstr)):
        if bitstr[i] == '1':
            bits = (bits << 1) | 1
        else:
            bits = bits << 1
    return bits

def get_byte_encoded_str(bitstring):

    size = len(bitstring)
    #print("============================")
    #print(bitstring)
    #print("============================")

    bytearr = []

    for i in range(0, size, 8):
        bytestr = bitstring[i:i+8]
        byte = convert_str_to_byte(bytestr)
        bytearr.append(byte)

    chrlist = [chr(item) for item in bytearr]
    
    finalres = ''
    
    for i in chrlist:
        finalres += i

    #print(finalres)
    
    return finalres


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

def parseArgs(minlimit=3):
    n = len(sys.argv)

    if n < minlimit:
        print("Error: Check arguments to fcompress")
        exit(1)

    return sys.argv[1], sys.argv[2]

def construct_huffman_tree(infhandle):
    global symbols, totalcharacters
    read_data = infhandle.read(MAX_FILE_READ_SIZE)
    symbols = {}
    totalcharacters = 0
    
    huffmantree = pqueue()

    while read_data:
        for i in range(0,len(read_data)):
            if read_data[i] in symbols:
                symbols[read_data[i]] += 1
            else:
                symbols[read_data[i]] = 1
            totalcharacters += 1

        read_data = infhandle.read(MAX_FILE_READ_SIZE)

    #print(symbols)
    #print(totalcharacters)
        
    for key, value in symbols.items():
        symbols[key] = symbols[key]/totalcharacters * 100
        s = Symbol(key, symbols[key], True)
        huffmantree.put(s)

    return huffmantree

if __name__ == "__main__":
    
    inputfilename, outputfilename = parseArgs(minlimit=3)

    infhandle = open(inputfilename, READMODE, encoding='utf-8')
    outfhandle = open(outputfilename, BWRITEMODE)

    compress(infhandle, outfhandle)
   
    outfhandle.close()
    infhandle.close()
    
    #Final results
    
    infilesize = os.path.getsize(inputfilename)
    outfilesize = os.path.getsize(outputfilename)

    print("Input size = ", infilesize, ", outfile size = ", outfilesize, ", ratio = ", infilesize/outfilesize)

    #print("Testsizez = ", sys.getsizeof(bytestr.encode('latin-1') + (str(abs(treesize)) + '|').encode('latin-1') + enctree.encode('latin-1')))
