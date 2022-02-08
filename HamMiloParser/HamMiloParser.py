###################################
###HamMiloParser by AugustoDoidin.############################
###It parses infos and extracts files on DC1/2/3/DLC MILO's###
##############################################################

import os
import zlib

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

def readBEInt(file):
    return int.from_bytes(file.read(4), "big")

def readBEString(file):
    stringLen = readBEInt(file)
    byteString = file.read(stringLen).decode("utf-8")
    return byteString

def writeBEFile(byte, output):
    makeDirs = os.path.split(os.path.abspath(output))
    os.makedirs(makeDirs[0], exist_ok=True)
    outFile = open(output, "wb")
    outFile.write(byte)
    outFile.close()

#def getFileFromMiloDeprecate(file):
    #terminator = [b'\xad',b'\xde',b'\xad',b'\xde']
    #bytesRead = []
    #fileInfo = b''
    #while bytesRead != terminator:
        #if(len(bytesRead) == 4):
            #bytesRead.pop(0)
        #actualByte = file.read(1)
        #bytesRead.append(actualByte)
        #fileInfo += actualByte
    #return fileInfo[:-4]

def getFileFromMilo(file):
    terminator = b'\xad\xde\xad'
    fileInfo = b''
    startOffset = file.tell()
    try:
        terminatorOffset = file.read().index(terminator)
        file.seek(startOffset)
        fileInfo = file.read(terminatorOffset)
        file.seek(3,1)
        if(file.read(1) != b'\xde'):
            file.seek(-1, 1)
        return fileInfo
    except:
        file.seek(startOffset)
        return(file.read())
        

def readObjectDir(file):
    objects = []
    objDirGameVer = readBEInt(file)#DC1=28,DC2+=32
    objDirType = readBEString(file)
    objDirName = readBEString(file)
    if(objDirGameVer == 32):
        file.seek(9, 1)
    else:
        file.seek(8, 1)
    objDirEntries = readBEInt(file)
    for x in range(objDirEntries):
        entryType = readBEString(file)
        entryName = readBEString(file)
        objects.append({'name': entryName, 'type': entryType})
    return objects

def extractUiLabel(file, count, output):
    for x in range(count):
        print('UILabelDir: uniq0\n')
        uiLabel1Files = readObjectDir(file)
        writeBEFile(getFileFromMilo(file), output + f"uniq0.milo")
        for uiLabel1File in uiLabel1Files:
            uiLabel1Name = uiLabel1File['name']
            uiLabel1Type = uiLabel1File['type']
            print(f'{uiLabel1Type}: {uiLabel1Name}')
            writeBEFile(getFileFromMilo(file), output + f"UILabelDir\\uniq0\\{uiLabel1Type}\\{uiLabel1Name}.milo")
    getFileFromMilo(file)

def extractHamMilo(file, output="extract\\", hamType="DLC"):
    if(hamType == "UPDATE"):
        dlcObjcs = readObjectDir(file)
        writeBEFile(getFileFromMilo(file), output + f"update.milo")
        if(dlcObjcs[0]['name'] == "barks"):
            writeBEFile(getFileFromMilo(file), output + f"barks.milo")
        if(dlcObjcs[1]['type'] == "ObjectDir"):
            writeBEFile(getFileFromMilo(file), output + f"move_data.milo")
            objDirFiles = readObjectDir(file)
            getFileFromMilo(file)#the same milo from the objdir that was already written
            print(f'ObjectDir: move_data\n')
            for objDirObject in objDirFiles:
                objDirName = objDirObject['name'].replace("*","").replace(">","")
                objDirType = objDirObject['type']
                print(f'{objDirType}: {objDirName}')
                writeBEFile(getFileFromMilo(file), output + f"MoveDir\\moves\\ObjectDir\\move_data\\{objDirType}\\{objDirName}")
        for objDirObject in dlcObjcs:
            objDirName = objDirObject['name'].replace("*","").replace(">","")
            objDirType = objDirObject['type']
            if(objDirType != "ObjectDir"):
                print(f'{objDirType}: {objDirName}')
                writeBEFile(getFileFromMilo(file), output + f"MoveDir\\moves\\{objDirType}\\{objDirName}")
        
    if(hamType == "DLC"):
        entireFile = file.read()
        uiLabelCount = entireFile.count(b'\x55\x49\x4C\x61\x62\x65\x6C\x44\x69\x72')
        file.seek(0)
        dlcObjcs = readObjectDir(file)
        writeBEFile(getFileFromMilo(file), output + "song.milo")
        for dcObject in dlcObjcs:
            dcName = dcObject['name']
            dcType = dcObject['type']
            if(dcType == 'ObjectDir'):
                print(f'\n{dcType}: {dcName}\n')
                writeBEFile(getFileFromMilo(file), output + f"{dcName}.milo")
                objDirFiles = readObjectDir(file)
                writeBEFile(getFileFromMilo(file), output + f"{dcName}2.milo")#the same milo from the objdir that was already written
                for objDirObject in objDirFiles:
                    objDirName = objDirObject['name'].replace("*","ASTERISCO").replace(">","SETAPROLADO")
                    objDirType = objDirObject['type']
                    print(f'{objDirType}: {objDirName}')
                    writeBEFile(getFileFromMilo(file), output + f"{dcType}\\{dcName}\\{objDirType}\\{objDirName}")
            if(dcType == 'MoveDir'):
                print(f'\n{dcType}: {dcName}\n')
                writeBEFile(getFileFromMilo(file), output + f"{dcName}.milo")
                movDirFiles = readObjectDir(file)
                if(uiLabelCount != 0):
                    file.seek(400, 1)
                    fileQnt = readBEInt(file)
                    for x in range(fileQnt):
                        font = readBEString(file)
                    if(file.read(4) != b'\x01\x01\x00\x00'):
                        file.seek(4,1)
                    extractUiLabel(file, uiLabelCount, output)
                else:
                    getFileFromMilo(file)#read moves.milo again
                if(movDirFiles[0]['name'] == "barks"):
                    writeBEFile(getFileFromMilo(file), output + f"barks.milo")
                if(movDirFiles[1]['type'] == "ObjectDir"):
                    writeBEFile(getFileFromMilo(file), output + f"move_data.milo")
                    objDirFiles = readObjectDir(file)
                    getFileFromMilo(file)#the same milo from the objdir that was already written
                    print(f'ObjectDir: move_data\n')
                    for objDirObject in objDirFiles:
                        objDirName = objDirObject['name'].replace("*","").replace(">","")
                        objDirType = objDirObject['type']
                        print(f'{objDirType}: {objDirName}')
                        writeBEFile(getFileFromMilo(file), output + f"MoveDir\\moves\\ObjectDir\\move_data\\{objDirType}\\{objDirName}")
                for objDirObject in movDirFiles:
                    objDirName = objDirObject['name'].replace("*","").replace(">","")
                    objDirType = objDirObject['type']
                    if(objDirType != "ObjectDir"):
                        print(f'{objDirType}: {objDirName}')
                        writeBEFile(getFileFromMilo(file), output + f"MoveDir\\moves\\{objDirType}\\{objDirName}")


directory = os.fsencode("input\\")
    
for file in os.listdir(directory):
     filename = os.fsdecode(file)
     if("milo_xbox" in filename): 
         dlcdir = os.path.join(directory.decode(), filename)
         file = open("uncompressed\\temp.milo_xbox", 'wb')
         file.write(inflateMilo(dlcdir))
         file.close()
         file = open("uncompressed\\temp.milo_xbox", 'rb')
         extractHamMilo(file, output=f"extract\\{filename.replace('.milo_xbox','')}\\")
         file.close()
         continue
     else:
         continue
                





