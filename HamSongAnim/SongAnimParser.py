import struct

def readBEInt(file):
    return int.from_bytes(file.read(4), "big")

def readBEFloat(file):
    return struct.unpack('>f',file.read(4))[0]

def readBEString(file):
    stringLen = readBEInt(file)
    byteString = file.read(stringLen).decode("utf-8")
    return byteString

def parseSongAnim(file):
    file.seek(38)
    songAnimEntries = readBEInt(file)
    for x in range(songAnimEntries):
        file.seek(8,1)
        entryType = readBEString(file)
        if(entryType == "HamDirector"):
            file.seek(11,1)
            hamType = readBEString(file)
            print(hamType)
            if(hamType == "clip" or hamType == "shot" or hamType == "practice"):
                file.seek(13,1)
                hamEntries = readBEInt(file)
                for x in range(hamEntries):
                    entryName = readBEString(file)
                    entryValue = readBEFloat(file)
                    print(f"{entryName}: {entryValue}")
            if(hamType == "postproc" or hamType == "move"):
                file.seek(4,1)
                entrySubType = readBEString(file)
                print(entrySubType)
                file.seek(5,1)
                hamEntries = readBEInt(file)
                if(hamType == "postproc"):
                    file.seek(4,1)
                for x in range(hamEntries):
                    entryName = readBEString(file)
                    entryValue = readBEFloat(file)
                    print(f"{entryName}: {entryValue}")
                
            
hamDir = open("song.anim", 'rb')
parseSongAnim(hamDir)
hamDir.close()
