# Copyright Seeky 2021

class Rand:
    def __init__(self, seed: int = 1):
        self.seed = seed

    def _rand(self, lim: int) -> int:
        RAND_MULT_MAGIC = 0x5d588b65

        divisor = 0xffffffff // (lim + 1)
        if divisor < 1:
            divisor = 1

        res = lim + 1 # make condition fail on first run
        while res >= lim + 1:
            # Python doesn't limit integer size, so & 0xffffffff is used to emulate a C 32-bit int
            self.seed = (((self.seed * RAND_MULT_MAGIC) & 0xffffffff) + 1) & 0xffffffff
            res = self.seed // divisor
        return res

    def irand(self, lim: int) -> int:
        # Calculate absolute value of lim
        # This isn't converted back to being negative on return
        absLim = abs(lim)

        if absLim == 0:
            # 0 will always result in zero
            return 0
        elif absLim == 1:
            # Special case for 1
            # 0-500 is 0, 501-1000 is 1
            return self._rand(1000) > 500
        elif absLim == 100:
            # Special case for 100
            # Selected from 0-1009 and divided by 10 (rounding down)
            return self._rand(1009) // 10
        else:
            # Calculate value in requested range
            return self._rand(absLim)
