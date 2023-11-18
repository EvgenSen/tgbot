#!/usr/bin/python

import os
import config

def save_to_file(filename, text):
    try:
        f = open(filename, "w")
        f.write(text)
        f.close()
        return 0
    except Exception as e:
        print(str(e))
    return 1

def read_from_file(filename):
    try:
        f = open(filename, "r")
        text = f.read()
        f.close()
        return text
    except Exception as e:
        print(str(e))
    return None
