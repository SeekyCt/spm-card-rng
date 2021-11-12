# Copyright Seeky 2021

from spmario import SpmarioGlobals
from binread import BinaryReader
from spmrng import Rand
from itemdata import getTable
from mariopouch import ITEM_ID_CARD_START, MarioPouchWork
from cardcommon import calcRngParams

def decideCard(gsw0: int, pouch: MarioPouchWork, rand: Rand, items: list[dict]) -> int:
    # Generate RNG info for available cards
    rngLimit, itemIds, chanceCache = calcRngParams(gsw0, items, pouch, "cardBagChance")
    
    # Fallback to Goomba if none can be given
    if len(itemIds) == 0:
        return ITEM_ID_CARD_START
    
    # Select card
    target = rand.irand(rngLimit - 1)
    pos = 0
    for i, itemId in enumerate(itemIds):
        pos += chanceCache[i]
        if pos > target:
            break

    return itemIds[i]

if __name__ == "__main__":
    try:
        ram = BinaryReader("ram.raw")
    except:
        ram = BinaryReader(input("Enter RAM dump path: "))

    spmarioGlobals = SpmarioGlobals(ram)
    items = getTable(ram)
    pouch = MarioPouchWork(ram)
    _seed = input("Enter seed: ")
    if _seed.startswith("0x"):
        seed = int(_seed, 16)
    else:
        seed = int(_seed)
    rand = Rand(seed)
    gsw0 = spmarioGlobals.getGSW(0)

    itemId = decideCard(gsw0, pouch, rand, items)
    print(f"Result will be item id {itemId} ({items[itemId]['itemName']})")
