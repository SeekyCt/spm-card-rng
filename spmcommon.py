# Copyright Seeky 2021

from binread import BinaryReader

def getVersion(ram: BinaryReader) -> str:
    regionChar = chr(ram.readatB(0x80000003))
    revision = ram.readatB(0x80000007)
    if regionChar == 'P':
        region = "eu"
    elif regionChar == 'E':
        region = "us"
    elif regionChar == 'J':
        region = "jp"
    else: # 'K'
        region = "kr"
    return region + str(revision)
