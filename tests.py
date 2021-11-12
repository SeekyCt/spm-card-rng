from binread import BinaryReader
from mariopouch import MarioPouchWork
from itemdata import getTable
from spmario import SpmarioGlobals
from spmrng import Rand
from cardbag import decideCard
from caughtcards import decideShopCards

def test_cardbag(ramPath, seed):
    ram = BinaryReader(ramPath)

    spmarioGlobals = SpmarioGlobals(ram)
    items = getTable(ram)
    pouch = MarioPouchWork(ram)
    rand = Rand(seed)
    gsw0 = spmarioGlobals.getGSW(0)

    itemId = decideCard(gsw0, pouch, rand, items)
    return itemId

def test_caughtcards(ramPath, seed):
    ram = BinaryReader(ramPath)

    spmarioGlobals = SpmarioGlobals(ram)
    items = getTable(ram)
    pouch = MarioPouchWork(ram)
    rand = Rand(seed)
    gsw0 = spmarioGlobals.getGSW(0)

    cards = decideShopCards(gsw0, pouch, rand, items)
    return cards

assert test_cardbag("test1.raw", 0xefdc4016) == 327
assert test_caughtcards("test1.raw", 0x6c7d4b11) == [
    0x11F, 0x130, 0x147, 0x148, 0x153, 0x154, 0x184, 0x15B, 0x16D, 0x1A7, 0x1B6, 0x1C0, 0x1FD, 0x1DF
]

assert test_cardbag("test2.raw", 0x60a13c04) == 422
assert test_caughtcards("test2.raw", 0x1a783d97) == [
    0x129, 0x12C, 0x13A, 0x141, 0x14D, 0x153, 0x15A, 0x15C, 0x15D, 0x161, 0x18E, 0x191, 0x196, 0x1FC
]
