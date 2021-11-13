from binread import BinaryReader
from spmcommon import getVersion

# TODO: port
MSGW_ADDR = {
    "eu0" : 0x805adf18,
    "eu1" : 0x805adf18
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
