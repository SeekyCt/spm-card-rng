# Copyright Seeky 2021

from binread import BinaryReader
from cardcommon import calcRngParams, gsw0ToSeqIndicator
from itemdata import getTable
from os import makedirs

from mariopouch import ITEM_ID_CARD_MAX, ITEM_ID_CARD_START

class DummyPouch:
    def checkCardKnown(self, _):
        return False
    
    def getCardCount(self, _):
        return 1

def getChancesAt(gsw0, items: dict):
    rngLimit1, itemIds1, chanceCache1 = calcRngParams(gsw0, items, DummyPouch(), "cardBagChance")
    rngLimit2, itemIds2, chanceCache2 = calcRngParams(gsw0, items, DummyPouch(), "cardShopChance")
    return (rngLimit1, tuple(itemIds1), tuple(chanceCache1)), (rngLimit2, tuple(itemIds2), tuple(chanceCache2))

def pad_right(s, l):
    s = str(s)
    return "".join((s, ' ' * (l - len(s))))

ram = BinaryReader("ram.raw")
items = getTable(ram)
makedirs("out", exist_ok=True)

def dump_data(gsw0, bag, shop, items):
    lines = ["".join([
        pad_right(f"Item Id", 12),
        pad_right(f"Bag", 12),
        pad_right(f"Shop", 12),
        "Item Name"
    ])]

    for i in range(ITEM_ID_CARD_START, ITEM_ID_CARD_MAX):
        if i in bag[1]:
            bag_chance = bag[2][bag[1].index(i)]
        else:
            bag_chance = 0
        if i in shop[1]:
            shop_chance = shop[2][shop[1].index(i)]
        else:
            shop_chance = 0

        if bag_chance == shop_chance == 0:
            continue

        lines.append("".join([
            pad_right(i, 12),
            pad_right(f"{100*bag_chance/bag[0]:.2f}%", 12),
            pad_right(f"{100*shop_chance/shop[0]:.2f}%", 12),
            items[i]["nameMsg"]
        ]))

    with open(f"out/Sequence {gsw0} ({gsw0ToSeqIndicator(gsw0):02d}).txt", 'w') as f:
        f.write('\n'.join(lines) + '\n')

last_bag, last_shop = None, None
for i in range(424):
    bag, shop = getChancesAt(i, items)
    bag_hash, shop_hash = hash(bag), hash(shop)
    if bag_hash == last_bag and shop_hash == last_shop:
        continue
    last_bag , last_shop = bag_hash, shop_hash

    dump_data(i, bag, shop, items)

