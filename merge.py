#!/usr/bin/env python
# coding: utf8

import os
import json
from config import *

def list_dir(path):
    stdout = os.popen('ls ' + path + ' 2>/dev/null').read().strip()
    if stdout:
        return stdout.split('\n')
    return []

def read_file_to_json(file_path):
    with open(file_path, 'r') as f:
        c = f.read().strip()
        try:
            return json.loads(c)
        except:
            return None

def stringify(s):
    if type(s) == str:
        return s.replace('\r', ' ').replace('\n', ' ')
    if type(s) == dict or type(s) == list:
        return json.dumps(s, ensure_ascii=False).encode('utf-8')
    if type(s) == unicode:
        return s.encode('utf-8')
    return str(s)

if __name__ == '__main__':
    school_path = 'school'
    index_path = 'schoolspecialindex'
    result = []

    header = set()
    for year in range(YEAR_TO, YEAR_BEGIN - 1, -1):

        for school_file_name in list_dir(school_path + '/*'):
            school_id = int(school_file_name.split('/')[-1].split('.')[0])
            school_obj = read_file_to_json(school_file_name) 

            if not school_obj:
                continue

            for index_file_path in list_dir('{index_path}/{year}_{school_id}_*.json'.format(**locals())):
                index_obj = read_file_to_json(index_file_path)
                if not index_obj:
                    continue

                for one in index_obj['data']['item']:
                    for k in school_obj:
                        one[k] = school_obj[k]
                    result.append(one)

                header |= set(one.keys())

    header = list(header)
    print '\t'.join([h for h in header])
    for one in result:
        print '\t'.join(map(str,[stringify(one.get(h, '')) for h in header]))
