# Copyright Seeky 2021

from binread import BinaryReader
from spmcommon import getVersion

class SpmarioGlobals:
    GP_ADDR = {
        "eu0" : 0x805ae178,
        "eu1" : 0x805ae178,
        "us0" : 0x8056D198,
        "us1" : 0x8056C9F8,
        "us2" : 0x8056CB78,
        "jp0" : 0x80542498,
        "jp1" : 0x80541A78,
        "kr0" : 0x805D7978
    }

    def __init__(self, ram: BinaryReader):
        self._ram = ram
        ver = getVersion(ram)
        self._addr = ram.readatW(SpmarioGlobals.GP_ADDR[ver])
    
    def getGSW(self, id: int) -> int:
        if id == 0:
            return self._ram.readatW(self._addr + 0x140)
        else:
            return self._ram.readatB(self._addr + 0x544 + id)
