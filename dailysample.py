#coding=utf-8
__author__ = 'xuwenbo'

import sys
import codecs

from pandas import DataFrame, Series
import pandas as pd

ENCODING = sys.getfilesystemencoding()

level_unknown_safe = [u'未知', u'安全']

def print_data(data):
    print(data.decode('utf-8').encode(ENCODING))

def show_top(frame):
    print(frame[u'包名'].value_counts()[:10])
    print(frame['name'].value_counts()[:10])

def do_stat(records):
    """
    同name (or 包名etc)下样本级别分布
    """
    #md5     name    包名    版本号  证书md5 证书名  级别    状态    abroadcautious  dexsize 软件大小
    frame = DataFrame(records[1:], columns=records[0])
    grouped_name = frame.groupby('name')
    for name, group in grouped_name:
        if not name:
            continue

        total = len(group)
        #unknown_safe = len([level for level in group.get(u'级别') if level in level_unknown_safe])
        unknown_safe = 0
        for level in group.get(u'级别'):
            if level in level_unknown_safe:
                unknown_safe += 1

        print('%s\t%d\t%d\t%f\t_name_'%(name.encode(ENCODING), total, unknown_safe, unknown_safe * 1.0 / total))
        #now the detailed
        for index, row in group.iterrows():
            if row[u'级别'] in level_unknown_safe:
                print('\t'.join(row.values).encode(ENCODING))

def load_records():
    """
    can also consider other ways
    """
    records = []
    with open(sys.argv[1]) as fr:
        records = [line.split('\t') for line in unicode(fr.read(), 'utf-8').splitlines()]
    return records

def main():
    records = load_records()
    do_stat(records)

if __name__ == "__main__":
    main()