#! /usr/bin/python3
# -*- coding:utf-8 -*-
import random
import os


class RandomSelector(object):
    def __init__(self, elapsed):
        if not 0 < elapsed <= 256*60:
            elapsed = random.randrange(256*60)
        self._selector = random.Random(int.from_bytes(os.urandom(32), 'big') * elapsed)

    def randselect(self, items, num):
        _items = items.copy()
        self._selector.shuffle(_items)
        return [_items.pop(self._selector.randrange(len(_items))) for _ in range(min(num, len(_items)))]


def randomselect(elapsed_ms, items, select_num):
    if len(items) == 0:
        return items
    return RandomSelector(elapsed_ms).randselect(items, select_num)
