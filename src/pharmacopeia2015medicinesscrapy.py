#coding: utf-8
import requests
import re
from bs4 import BeautifulSoup

'''
    Scrapy the medicines data of The pharmacopeia 2015 online websit.

    http://db.ouryao.com/

    Basic url: http://db.ouryao.com/yd2015/view.php?v=txt&id=index
    The range of index : 1 - 618
'''

medicine_pattern = r'[\u4e00-\u9fff]+'

pinyin_pattern = r'[A-Z][a-z ]+'

latin_pattern = r'[A-Z]+[^a-z\r\n]+[A-Z]+'

# Parse the page to get the contents we need
def parse_page(source_page):

    page_contents = source_page.content

    bs_object = BeautifulSoup(page_contents)

    cms_list = bs_object.find('pre')
    if cms_list == None:
        print('contents are None!')
        return ''
    # the text of contents
    content_text = cms_list.get_text()

    content_text = content_text.replace('\r\n', '').replace('"', '')

    content_text_list = content_text.split('【')

    # content_text_list[0] are the medicines name and abstraction
    medinces_and_abstraction_str = get_name_and_abstract(content_text_list[0])
    print(medinces_and_abstraction_str)

    # the last part are the key and value
    key_and_value_str = get_key_and_values(content_text_list)

    print(key_and_value_str)

    result = '{' + medinces_and_abstraction_str.strip() + key_and_value_str.strip() + '"数据来源":"2015中国药典"}'

    return result




# Get the medicine name and abstraction
def get_name_and_abstract(text):
    text_list = text.split('    ')
    names_str = text_list[0]
    abstraction_str = text_list[1]

    medicine_str = ''
    if re.search(medicine_pattern, names_str):
        medicine_str = re.search(medicine_pattern, names_str).group(0)

    pinyin_str = ''
    if re.search(pinyin_pattern, names_str):
        pinyin_str = re.search(pinyin_pattern, names_str).group(0)

    latin_str = ''
    if re.search(latin_pattern, names_str):

        latin_str = re.search(latin_pattern, names_str).group(0)

    result = '"中文名":"' + medicine_str + '","拼音":"' + pinyin_str + '","拉丁名":"' + latin_str + '","摘要":"' + abstraction_str + '",'

    return result

# Get the key and value parse string
def get_key_and_values(content_text_list):
    if content_text_list == None:
        return ''

    # parse the list
    result = ''

    for item in content_text_list:

        if '】' in item:
            item_split_list = item.split('】')
            key_str = item_split_list[0]
            value_str = item_split_list[1].replace('    ', '').replace('"', '')

            result += '"' + key_str + '":"' + value_str + '",'
    return result







################################
def main():
    print('Begin!')

    # page number from 1 to 618
    index = 1

    data_file = '/Users/heermaster/PycharmProjects/webscrapyofTCM/src/2015medicines.txt'

    basic_url = 'http://db.ouryao.com/yd2015/view.php?v=txt&id='

    with open(data_file, 'w') as out_file:
        # page number f
        for page_num in range(1, 619): #619

            url = basic_url + str(page_num)

            source_page = requests.get(url)

            parsed_data = parse_page(source_page)

            out_file.write(parsed_data + '\n')

            print(index)
            index += 1


    print('End!')

if __name__ == '__main__':
    main()