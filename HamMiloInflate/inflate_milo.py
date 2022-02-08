import zlib
import struct

def readLEInt(file):
    return int.from_bytes(file.read(4), "little")

def inflateMilo(inputFile):
    file = open(inputFile, 'rb')
    miloType = file.read(4)
    if(miloType != b'\xAF\xDE\xBE\xCD'):
        print("Only HAM Milo's supported!")
        return None
    zOffset = readLEInt(file)
    zBlockCount = readLEInt(file)
    zBiggestSize = readLEInt(file)
    zBlocks = []
    for x in range(zBlockCount):
        zBlocks.append(readLEInt(file))
    file.seek(zOffset, 0)
    miloData = b''
    for x in range(len(zBlocks)):
        defaultValue = 16777216
        if zBlocks[x] >= defaultValue:
            readValue = zBlocks[x] - defaultValue
            miloBlock = file.read(readValue)
        else:
            file.seek(4, 1)
            block = file.read(zBlocks[x] - 4)
            zLib = zlib.decompressobj()
            zLib.decompress(bytes([0x78, 0x9c]))
            miloBlock = zLib.decompress(block)
        miloData = miloData + miloBlock
    file.close()
    return miloData

def compressMilo(file, compressedMilo):
    decompressedMilo = file.read()
    decompressedMiloDataSize = len(decompressedMilo)
    
    compressedMilo.write(b'\xAF\xDE\xBE\xCD')
    compressedMilo.write((2064).to_bytes(4, "little"))
    compressedMilo.write((1).to_bytes(4, "little"))
    compressedMilo.write(struct.pack('<I', decompressedMiloDataSize))
    compressedMilo.write(struct.pack('<I', decompressedMiloDataSize+16777216))
    compressedMilo.seek(2064)
    compressedMilo.write(decompressedMilo)

