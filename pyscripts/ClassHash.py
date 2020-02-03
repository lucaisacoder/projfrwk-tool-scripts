#!/usr/bin/env python3
#-*- coding = utf-8 -*-
from hashlib import md5,sha1
from zlib import crc32

class ClassHash:
    def __init__(self):
        pass

    def calc_md5(self, filename):
        _ret = md5()
        with open(filename, 'rb') as f:
            _ret.update(f.read())
        return _ret.hexdigest()

    def calc_sha1(self, filename):
        _ret = sha1()
        with open(filename, 'rb') as f:
            _ret.update(f.read)
        return _ret.hexdigest()

    def calc_crc32(self, filename):
        with open(filename, 'rb') as f:
            return crc32(f.read())