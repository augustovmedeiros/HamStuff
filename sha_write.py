import os
import hashlib

def get_hash(f_path, mode='sha1'):
    h = hashlib.new(mode)
    with open(f_path, 'rb') as file:
        data = file.read()
    h.update(data)
    digest = h.digest()
    return digest

gamexex = open("default.xex", 'r+b')
with open("offsets.txt") as file:
    for line in file:
        filestuff = line.rstrip().split(";")
        fileadress = filestuff[0]
        fileoffset = int(filestuff[1])
        print(fileadress)
        gamexex.seek(fileoffset)
        gamexex.write(get_hash(fileadress))
gamexex.close()




