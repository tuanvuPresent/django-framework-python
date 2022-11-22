import datetime
from time import time

INSTANCE_GEN_ID = 1
EPOCH_TIME = int(datetime.datetime(year=2022, month=9, day=1).timestamp()) * 1000


class UuidGenerator:
    """
        time (ms)
        instance(int): 13 bit
        seq(int): 10 bit
    """
    MAX_SEQ = 2 ** 10 - 1

    def __init__(self, epoch: int = 0, instance: int = 1):
        current = int(time() * 1000)
        self._epo = epoch
        self._ts = current - self._epo
        self._inf = instance
        self._seq = 0

    def __next__(self):
        current = int(time() * 1000) - self._epo
        if self._ts == current:
            if self._seq == self.MAX_SEQ:
                return None
            self._seq += 1
        else:
            self._seq = 0

        self._ts = current
        return self._ts << 23 | self._inf << 10 | self._seq


class UuidGenSingletonGroup:
    _instances = {}
    uuid = None

    def __new__(cls, name):
        if not cls._instances.get((cls.__name__, name)):
            cls._instances[(cls.__name__, name)] = super(UuidGenSingletonGroup, cls).__new__(cls)
            cls.uuid = UuidGenerator(epoch=EPOCH_TIME, instance=INSTANCE_GEN_ID)
        return cls._instances.get((cls.__name__, name))

    def __init__(self, name):
        self.name = name

    def gen(self):
        return next(self.uuid)


uuid = UuidGenerator(epoch=EPOCH_TIME, instance=INSTANCE_GEN_ID)