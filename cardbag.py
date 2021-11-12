# Copyright Seeky 2021

from spmario import SpmarioGlobals
from binread import BinaryReader
from spmrng import Rand
from itemdata import getTable
from mariopouch import ITEM_ID_CARD_START, MarioPouchWork
from cardcommon import gsw0ToSeqIndicator

def decideCard(gsw0: int, pouch: MarioPouchWork, rand: Rand, items: list[dict]) -> int:
    # Generate RNG info for available cards
    seq = gsw0ToSeqIndicator(gsw0)
    rngLimit = 0
    chanceCache = []
    itemIds = []
    for itemId, item in enumerate(items):
        # Chance must be non-zero, GSW(0) must be high enough, and if this is a one-time
        # card then it can't be added unless it's unknown
        if item["cardBagChance"] != 0 and item["cardShopMinGsw0"] <= gsw0 and \
        (not item["cardShopBlockDuplicate"] or not pouch.checkCardKnown(itemId)):
            chance = item["cardBagChance"]
            if seq >= item["cardShopBonusSeq"]:
                # 10x chance if above certain GSW(0)
                chance *= 10
            if pouch.getCardCount(itemId) == 0:
                # 3x chance if none are in inventory
                chance *= 3
            rngLimit += chance
            chanceCache.append(chance)
            itemIds.append(itemId)
    
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
