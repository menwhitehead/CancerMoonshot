import sys
import string

def onlyAlpha(txt):
    result = ''
    tokens = txt.split()
    for token in tokens:
        for c in token:
            if c.isalpha():
                result += c
            elif len(result) > 0 and result[-1] != ' ':
                result += ' '

        if len(result) > 0 and result[-1] != ' ':
            result += " "
    return result

def process(txt):
    txt = txt.lower()
    txt = onlyAlpha(txt)
    return txt
