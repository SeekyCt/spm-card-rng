# Copyright Seeky 2021

from spmario import SpmarioGlobals
from binread import BinaryReader
from spmrng import Rand
from itemdata import getTable
from mariopouch import ITEM_ID_CARD_START, ITEM_ID_CARD_MAX, MarioPouchWork
from cardcommon import calcRngParams

def decideShopCards(gsw0: int, pouch: MarioPouchWork, rand: Rand, items: list[dict]):
    # Clear cards that aren't one-time from stash
    stash = pouch.getShopCardStash()
    for i, itemId in enumerate(range(ITEM_ID_CARD_START, ITEM_ID_CARD_MAX)):
        if stash[i] != 0 and (not items[itemId]["cardShopBlockDuplicate"] \
                              or not pouch.checkCardKnown(itemId)):
            stash[i] = 0
    
    # Calculate how many items more than 10 will be for sale
    extraItemCount = rand.irand(5)
    
    # Generate RNG info for available cards
    rngLimit, itemIds, chanceCache = calcRngParams(gsw0, items, pouch, "cardShopChance")

    # The game will return nothing if this is 0, regardless of whether sold
    # one-time cards could still be bought
    if len(itemIds) == 0:
        return []

    # Select up to 100 cards to put in the stash
    # One-time cards that have been sold will already be in the stash
    for i in range(0, 100):
        target = rand.irand(rngLimit - 1)
        pos = 0
        for j, itemId in enumerate(itemIds):
            pos += chanceCache[j]
            if pos > target:
                break
        idx = itemIds[j] - ITEM_ID_CARD_START
        if stash[idx] == 0:
            stash[idx] = 1

    # Get a list of all indexes into the stash which aren't zero
    idxs = []
    for i in range(0, 256):
        if stash[i] != 0:
            idxs.append(i)
    
    # Shuffle those indexes
    for i in range(0, 1000):
        r1 = rand.irand(len(idxs) - 1)
        r2 = rand.irand(len(idxs) - 1)
        temp = idxs[r1]
        idxs[r1] = idxs[r2]
        idxs[r2] = temp
    
    # Add up to 10 + extraItemCount cards to the item table
    itemTable = []
    for i in range(0, len(idxs)):
        if i >= extraItemCount + 10:
            break
        itemTable.append(idxs[i] + ITEM_ID_CARD_START)
    
    # Sort the item table
    for i in range(0, len(itemTable)):
        for j in range(0, len(itemTable) - 1):
            itemId = itemTable[j]
            nextId = itemTable[j+1]
    
            if items[itemId]["sortValue"] > items[nextId]["sortValue"]:
                itemTable[j] = nextId
                itemTable[j+1] = itemId
    
    return itemTable

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

    cards = decideShopCards(gsw0, pouch, rand, items)
    print("Results will be item ids:")
    for i, card in enumerate(cards):
        print(f"    {card} ({items[card]['itemName']})")
