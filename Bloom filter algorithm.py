import math
import array
import sys
import csv

'''Proffessor Wilson's Bit Array implementation'''
def makeBitArray(bitSize, fill = 0):
    intSize = bitSize >> 5                   # number of 32 bit integers
    if (bitSize & 31):                      # if bitSize != (32 * n) add
        intSize += 1                        #    a record for stragglers
    if fill == 1:
        fill = 4294967295                                 # all bits set
    else:
        fill = 0                                      # all bits cleared

    bitArray = array.array('I')          # 'I' = unsigned 32-bit integer
    bitArray.extend((fill,) * intSize)
    return(bitArray)

  # testBit() returns a nonzero result, 2**offset, if the bit at 'bit_num' is set to 1.
def testBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    return(array_name[record] & mask)

# setBit() returns an integer with the bit at 'bit_num' set to 1.
def setBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    array_name[record] |= mask
    return(array_name[record])

# clearBit() returns an integer with the bit at 'bit_num' cleared.
def clearBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = ~(1 << offset)
    array_name[record] &= mask
    return(array_name[record])

# toggleBit() returns an integer with the bit at 'bit_num' inverted, 0 -> 1 and 1 -> 0.
def toggleBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    array_name[record] ^= mask
    return(array_name[record])


'''bloom filter implementation'''

class BloomFilter:
    def __init__(self, n):
        #size of arr
        self.n = n 
        #false positive rate
        p = 0.0000001 
        #size of bit array
        self.m = math.ceil((self.n * math.log(p)) / math.log(1 / pow(2, math.log(2)))) 
        # number of hash functions
        self.k = round((self.m / self.n) * math.log(2)) 
        #casting to int after the initial math in order to not lose accuracy
        self.m = int(self.m)
        self.k = int(self.k)
        
        self.bit_array = makeBitArray(self.m)

    def insert(self, element):
        # add item to bloom filter
        for i in range(self.k):
             # calculate hash function
            h = hash(element + str(i)) % self.m
            # set bit to 1
            setBit(self.bit_array,h)
            
    def check(self, element):
        # check if item is in bloom filter
            for i in range(self.k):
                # calculate hash function
                h = hash(element + str(i)) % self.m
                # check if bit is 0 meaning it's not in the database
                if  testBit(self.bit_array,h) == 0: return False
            return True
def load_data():
    #returns a list with the first element being the emails and the second element  being the emails to validate the bloom filter 
    if len(sys.argv) > 1:
        output = [None,None]
        with open(sys.argv[1], 'r') as file:
            csvreader = list(csv.reader(file))[1:]
            output[0] = csvreader
        with open(sys.argv[2], 'r') as file:
            csvreader = list(csv.reader(file))[1:]
            output[1] = csvreader
        return output

d = load_data()
if d:
    bf = BloomFilter(len(d[0]))
    #insert emails
    for x in d[0]:
        email = x[0]
        bf.insert(email)
    #validate
    for x in d[1]:
        email = x[0]
        if bf.check(email):
            print(email+',Probably in the DB')
        else:
            print(email+ ',Not in the DB')

            

            
    



