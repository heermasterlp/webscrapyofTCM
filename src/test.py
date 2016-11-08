#coding:utf-8
import re

text = '胜马刺 50g 三七 三七 10.5g 油0.87ml'

patterns = r'[\u4e00-\u9fff]+[ 0-9a-z\.]*[^\u4e00-\u9fff]'
text = u'\u6ce2\u68f1\u74dc\u5b5030g'

prescri_items = re.findall(patterns, text)

print(len(prescri_items))

for item in prescri_items:
    print(item)







