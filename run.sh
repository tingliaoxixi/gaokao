#!/usr/bin/env bash
# zhangxiaoyang.hit@gmail.com

echo "**1/6 initializing..."
mkdir -p schoolspecialindex
mkdir -p school
mkdir -p output
cat config.py | grep -v '#'

echo
read -p "**2/6 confirm[Y/n]:" confirm
if [ "$confirm" != "Y" ]; then
    exit 0
fi

echo
echo "**3/6 crawling schoolspecialindex..."
python -u crawl.py schoolspecialindex

echo
echo "**4/6 crawling school..."
python -u crawl.py school

echo
echo "**5/6 merging data..."
output_file=output/gaokao.csv
python merge.py | iconv -f utf8 -t gb18030 > $output_file

echo
echo "**6/6 finish: $output_file"
