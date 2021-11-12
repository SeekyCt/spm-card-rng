# Copyright Seeky 2021

from mariopouch import MarioPouchWork

def gsw0ToSeqIndicator(n: int) -> int:
    if n in range(0, 11):
        return 0
    elif n in range(11, 18):
        return 11
    elif n in range(18, 29):
        return 12
    elif n in range(29, 38):
        return 13
    elif n in range(38, 66):
        return 14
    elif n in range(66, 77):
        return 21
    elif n in range(77, 83):
        return 22
    elif n in range(83, 89):
        return 23
    elif n in range(89, 101):
        return 24
    elif n in range(101, 106):
        return 31
    elif n in range(106, 112):
        return 32
    elif n in range(112, 118):
        return 33
    elif n in range(118, 129):
        return 34
    elif n in range(129, 139):
        return 41
    elif n in range(139, 161):
        return 42
    elif n in range(161, 179):
        return 44
    elif n in range(179, 187):
        return 51
    elif n in range(187, 195):
        return 52
    elif n in range(195, 203):
        return 53
    elif n in range(203, 225):
        return 54
    elif n in range(225, 272):
        return 61
    elif n in range(272, 290):
        return 62
    elif n in range(290, 291):
        return 63
    elif n in range(291, 292):
        return 64
    elif n in range(292, 307):
        return 71
    elif n in range(307, 328):
        return 72
    elif n in range(328, 359):
        return 74
    elif n in range(359, 371):
        return 81
    elif n in range(371, 387):
        return 82
    elif n in range(387, 405):
        return 83
    elif n in range(405, 421):
        return 84
    else:
        return 90

def calcRngParams(gsw0: int, items: list[dict], pouch: MarioPouchWork, chanceName: str) -> (int, list[int], list[int]):
    seq = gsw0ToSeqIndicator(gsw0)
    rngLimit = 0
    itemIds = []
    chanceCache = []
    for itemId, item in enumerate(items):
        # Chance must be non-zero, GSW(0) must be high enough, and if this is a one-time
        # card then it can't be added unless it's unknown
        if item[chanceName] != 0 and item["cardShopMinGsw0"] <= gsw0 and \
           (not item["cardShopBlockDuplicate"] or not pouch.checkCardKnown(itemId)):
            chance = item[chanceName]
            if seq >= item["cardShopBonusSeq"]:
                # 10x chance if above certain GSW(0)
                chance *= 10
            if pouch.getCardCount(itemId) == 0:
                # 3x chance if none are in inventory
                chance *= 3
            rngLimit += chance
            chanceCache.append(chance)
            itemIds.append(itemId)

    return rngLimit, itemIds, chanceCache
