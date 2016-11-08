#coding:utf-8
import requests
import re
from bs4 import BeautifulSoup
'''
    Scrpay the tcm products from 2015 pharmacopeias

    Website : http://db.ouryao.com/

    basic url: http://db.ouryao.com/yd2015/view.php?v=txt&id=index

    The range of index : 666 - 2158
'''

medicines_name_pattern = u'[\u4e00-\u9fff]+'
pinyin_pattern = r'[A-Za-z ]+'
# prescription_pattern = r'[\u4e00-\u9fff]+[0-9]+[a-z]+'
# prescription_pattern = u'[\u4e00-\u9fff]+[\u0020\u0030-\u0039\u0061-\u007a\u002e]*[^\u4e00-\u9fff]'
# prescription_pattern = u'[\u4e00-\u9fff]+\u0020*(\uff08[\u4e00-\u9fff]*\u3001*\uff09)*[0-9]*[a-z]*[A-Z]*[^\u4e00-\u9fff]'
prescription_pattern = u'[\u4e00-\u9fff]+[\uff08\uff09\u3001\u4e00-\u9fff]*[ 0-9a-z\.]*[^\u4e00-\u9fff]'


chinese_pattern = r'[\u4e00-\u9fff]+'

number_pattern = r'[0-9]+'

unit_pattern = r'[a-z]+'


# parse source page
def parse_page(source_page):
    page_contents = source_page.content

    bs_object = BeautifulSoup(page_contents)

    cms_list = bs_object.find('pre')
    if cms_list == None:
        print('contents are None!')
        return ''

    # the text of contents
    content_text = cms_list.get_text().encode('utf-8')

    content_text = content_text.replace('\r\n', ' ').replace('"', ' ').replace('\t', '')
    # 【
    content_list = content_text.split('【')
    # [0] is the medicines name and pinyin
    name_and_pinyin = content_list[0].strip().decode('utf-8')
    print(repr(name_and_pinyin))

    name_str = ''
    if re.search(medicines_name_pattern, name_and_pinyin):
        name_str = re.search(medicines_name_pattern, name_and_pinyin).group(0).encode('utf-8').strip()
        # print(name_str)

    pinyin_str = ''
    if re.search(pinyin_pattern, name_and_pinyin):
        pinyin_str = re.search(pinyin_pattern, name_and_pinyin).group(0).encode('utf-8').strip()

    result = '{"中文名":"' + name_str + '","拼音名":"' + pinyin_str + '",'

    # [1] is the prescription
    if '处方' in content_list[1]:
        prescription_list = content_list[1].split('】')

        prescription_item_str = ''
        print(repr(prescription_list[1].decode('utf-8')))
        prescri_items = re.findall(prescription_pattern, prescription_list[1].decode('utf-8'))

        for pre_i in prescri_items:

            prescription_item_str += pre_i.encode('utf-8').strip() + '|'
        prescription_item_str = prescription_item_str.rstrip('|')
        # print(len(prescri_items))
        print(prescription_item_str)
        result += '"' + prescription_list[0] + '":"' + prescription_item_str + '",'

    # [2]...are the key and value contents
    length = len(content_list)
    for index in range(2, length - 1):
        if '】' in content_list[index]:

            prescription_item = content_list[index].split('】')
            if index == length - 1:
                result += '"' + prescription_item[0] + '":"' + prescription_item[1].replace('     ','') + '"'
            else:
                result += '"' + prescription_item[0] + '":"' + prescription_item[1].replace('     ','') + '",'

    result += '}'
    return result

# get the prescription list of this products with format: key:p1|p2|p3|....
def get_prescriptions(text):
    result = ''
    return result


######################################33
def main():

    index = 0

    basic_url = 'http://db.ouryao.com/yd2015/view.php?v=txt&id='

    data_file = '/Users/heermaster/PycharmProjects/webscrapyofTCM/src/2015products.txt'

    page_num = 666

    with open(data_file, 'w') as out_file:

        for page_num in range(666, 2159): # 2159

            url = basic_url + str(page_num)

            source_page = requests.get(url=url)

            parsed_data = parse_page(source_page)

            out_file.write(parsed_data + '\n')

            print(page_num - 665)
            page_num += 1


if __name__ == '__main__':
    main()