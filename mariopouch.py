# Copyright Seeky 2021

from binread import BinaryReader
from spmcommon import getVersion

ITEM_ID_CARD_START = 0x11a
ITEM_ID_CARD_MAX = 0x21a

class MarioPouchWork:
    POUCH_ADDRS = {
        "eu0" : 0x80511a28,
        "eu1" : 0x80511a28,
        "us0" : 0x804CEA28,
        "us1" : 0x804D02A8,
        "us2" : 0x804D0428,
        "jp0" : 0x804A3D28,
        "jp1" : 0x804A5328,
        "kr0" : 0x80549310
    }

    def __init__(self, ram: BinaryReader):
        self._ram = ram
        self._addr = MarioPouchWork.POUCH_ADDRS[getVersion(ram)]

    def checkCardKnown(self, itemId: int) -> bool:
        card = itemId - ITEM_ID_CARD_START
        idx = card // 32
        word = self._ram.readatW(self._addr + 0x328 + (idx * 4))
        mask = 1 << (idx % 32)
        return word & mask != 0

    def getCardCount(self, itemId: int) -> bool:
        card = itemId - ITEM_ID_CARD_START
        return self._ram.readatB(self._addr + 0x10c + card)

    def getShopCardStash(self):
        return list(self._ram.readat(self._addr + 0x20c, 256))
