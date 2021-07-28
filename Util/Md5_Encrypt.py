# -*- coding: utf-8 -*-
"""
Time:     2021/7/26 23:46
Author:   panyuangao@foxmail.com
File:     Md5_Encrypt.py
Describe: 
"""
import hashlib

def md5_encrypt(text):
    m5 = hashlib.md5()
    #TypeError: Unicode-objects must be encoded before hashing for python3
    m5.update(text.encode('utf-8'))
    value = m5.hexdigest()
    return value
