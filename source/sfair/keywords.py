import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def keys():
    keys = open(os.path.join(os.path.dirname(BASE_DIR), ".keywords.src"), 'r').read()
    keywords = keys.split("\n")
    keywords.pop()
    return keywords
