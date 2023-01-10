from binread import BinaryReader
from spmcommon import getVersion

MSGW_ADDR = {
    "eu0" : 0x805adf18,
    "eu1" : 0x805adf18,
    "us0" : 0x8056cf38,
    "us1" : 0x8056c798,
    "us2" : 0x8056c918,
    "jp0" : 0x80542238,
    "jp1" : 0x80541818,
    "kr0" : 0x805d79d0
}

class GlobalText:
    def __init__(self, ram: BinaryReader):
        ver = getVersion(ram)
        msgw = ram.readatW(MSGW_ADDR[ver])
        gtxt = ram.readatW(msgw + 0x4)
        count = ram.readatW(msgw + 0x8)

        self.msgDict = {}
        p = gtxt
        haveName = False
        workingName = ""
        workingMsg = ""
        for _ in range(count):
            name = ram.readatS(p)
            p += len(name) + 1
            msg = ram.readatS(p)
            p += len(msg) + 1

            if not name in self.msgDict:
                self.msgDict[name] = msg
        
    def get(self, name):
        return self.msgDict[name]
