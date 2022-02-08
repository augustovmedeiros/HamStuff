import os
import hashlib

def get_hash(f_path, mode='sha1'):
    h = hashlib.new(mode)
    with open(f_path, 'rb') as file:
        data = file.read()
    h.update(data)
    digest = h.digest()
    return digest
def list_files(dir):
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            r.append(os.path.join(root, name))
    return r

xexfile = open("default.xex" , "rb").read()
files = list_files(os.getcwd())
for dc3file in files:
    if not(dc3file.endswith(".py") and dc3file.endswith(".xex")):
        decimaloffset = xexfile.find(get_hash(dc3file))
        if(decimaloffset != -1):
            print(dc3file + ";" + str(decimaloffset))



