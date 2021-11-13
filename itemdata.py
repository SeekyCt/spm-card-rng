# Copyright Seeky 2021

from binread import BinaryReader
from spmcommon import getVersion
from msgdrv import GlobalText

TABLE_ADDR = {
    "eu0" : 0x803f5f98,
    "eu1" : 0x803f5f98,
    "us0" : 0x803B6978,
    "us1" : 0x803B7CD8,
    "us2" : 0x803B7E78,
    "jp0" : 0x8038BBF8,
    "jp1" : 0x8038CD78,
    "kr0" : 0x80426AB8
}

def getTable(ram: BinaryReader) -> list[dict]:
    ver = getVersion(ram)
    addr = TABLE_ADDR[ver]
    globalTxt = GlobalText(ram)

    ret = []
    for _ in range(0, 538):
        entry = {}
        itemNameAddr = ram.readatW(addr + 0x0)
        entry["itemName"] = ram.readatS(itemNameAddr)
        nameMsgAddr = ram.readatW(addr + 0x10)
        nameMsg = ram.readatS(nameMsgAddr)
        entry["nameMsg"] = globalTxt.get(nameMsg)
        entry["cardBagChance"] = ram.readatB(addr + 0x20)
        entry["cardShopChance"] = ram.readatB(addr + 0x21)
        entry["cardShopBonusSeq"] = ram.readatH(addr + 0x22)
        entry["cardShopMinGsw0"] = ram.readatH(addr + 0x24)
        entry["cardShopBlockDuplicate"] = ram.readatB(addr + 0x26)
        entry["sortValue"] = ram.readatH(addr + 0x2a)

        ret.append(entry)
        addr += 0x2c

    return ret
