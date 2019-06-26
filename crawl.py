#!/usr/bin/env python
# coding: utf8

import sys
import json
import time
import requests

from config import *

def crawl(url, file_path):
    while True:
        try:
            res = requests.get(url, timeout=3)
            if res.status_code == 404:
                return None
            else:
                with open(file_path, 'w') as f:
                    f.write(res.text)
                return True
        except:
            pass

        print 'retry: ' + url
        time.sleep(0.1)
    return False # never be here

def crawl_schoolspecialindex():

    def crawl_helper(year, school_id, page_num):
        province_id = PROVINCE_ID
        subject_id = SUBJECT_ID
        url_template = 'https://static-data.eol.cn/www/2.0/schoolspecialindex/{year}/{school_id}/{province_id}/{subject_id}/{page_num}.json'
        url = url_template.format(**locals())

        file_path = 'schoolspecialindex/' + '_'.join(map(str, [year, school_id, subject_id, page_num])) + '.json'
        return crawl(url, file_path)

    for year in range(YEAR_TO, YEAR_BEGIN - 1, -1):
        for school_id in range(0, 1000):
            crawled = False

            # Test school_id
            page_num = 1
            if crawl_helper(year, school_id, page_num) is None:
                print '[SKIP] crawl: {year}/{school_id}/{page_num}'.format(**locals())
                continue

            # Crawl data of school_id
            for page_num in range(0, 100):
                succ = crawl_helper(year, school_id, page_num)
                if succ is None:
                    succ_flag = 'SKIP'
                elif succ:
                    crawled = True
                    succ_flag = 'SUCC'
                else:
                    succ_flag = 'FAIL'

                print '[{succ_flag}] crawl: {year}/{school_id}/{page_num}'.format(**locals())
                if succ is None and crawled:
                    break

def crawl_school():

    def crawl_helper(school_id):
        url_template = 'https://static-data.eol.cn/www/school/{school_id}/info.json'
        url = url_template.format(**locals())

        file_path = 'school/' + str(school_id) + '.json'
        return crawl(url, file_path)

    for school_id in range(0, 1000):
        crawled = False

        succ = crawl_helper(school_id)
        if succ is None:
            succ_flag = 'SKIP'
        elif succ:
            crawled = True
            succ_flag = 'SUCC'
        else:
            succ_flag = 'FAIL'

        print '[{succ_flag}] crawl: {school_id}'.format(**locals())
        if succ is None and crawled:
            break

if __name__ == '__main__':
    if len(sys.argv) > 1:
        selector = sys.argv[1]
        if selector in ['schoolspecialindex', 'school']:
            exec 'crawl_%s()' % selector
            exit(0)

    print 'Invalid arguments, need selector'
    exit(1)
