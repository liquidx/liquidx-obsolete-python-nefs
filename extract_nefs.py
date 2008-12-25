#!/usr/bin/python
"""
  Scours a data blob (FAT16) for Nikon RAW files (NEF)
"""
import sys
import os
import struct
import stat

NEF_HEADER = struct.unpack('<IIH', '\x4d\x4d\x00\x2a\x00\x00\x00\x08\x00\x18')
NEF_HEADER_LEN = 10

def main(args):
  
  size = os.stat(args[0])[stat.ST_SIZE]
  f = open(args[0], 'rb')
  # offsets = []
  # while True:
  #   try:
  #     block = struct.unpack('<IIH', f.read(NEF_HEADER_LEN))
  #   except (IOError, struct.error):
  #     break
  #   if block == NEF_HEADER:
  #     offsets.append(f.tell())
  #     print 'Found:', hex(f.tell())
  #   else:
  #     f.seek(-1 * (NEF_HEADER_LEN - 1), 1)
  #     if f.tell() % 0x80000 == 0:
  #       print hex(f.tell()), block
  #     continue
    
  offsets = [int(line.strip(), 16) for line in open('offsets.txt', 'r').readlines()]
  pos = 0
  f.seek(0)
  for i in range(len(offsets)):
    start = offsets[i]
    if i == len(offsets) - 1:
      end = size
    else:
      end = offsets[i+1]
    
    f.seek(start)
    d = open('%d.NEF' % i, 'w')
    d.write(f.read(end - start))
    print 'wrote: %d.NEF 0x%x to 0x%x' % (i, start, end)
    d.close()

if __name__ == '__main__':
  main(sys.argv[1:])