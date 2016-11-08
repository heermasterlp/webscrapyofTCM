#coding: utf-8
import requests
from bs4 import BeautifulSoup
import json
'''
    This is the scrapy function of TCM products to get data.
    page number; 677 - 1741

    basic url: http://drugs.yaojia.org/index.php?m=drugs&c=index&a=show&catid=7&id=

'''

# get text from website
def get_text_from_web(url, page_num):

    url += str(page_num)

    page_source = requests.get(url)

    return page_source.text

# parse the content to return JSON
def parse_page(text):
    soup = BeautifulSoup(text)

    dts = soup.find_all('span', {'class':'fl'})

    dds = soup.find_all('dd')

    # length of contents
    if len(dts) != len(dds):
        return None

    length = len(dts)

    # create json data
    jsonStr = '{"'

    # process the
    tcmnames_str = dds[0].get_text().encode('utf-8').replace('\r\n', ' ').replace('"', '').strip()
    tcmnames_items = tcmnames_str.split('     ')
    # print(len(tcmnames_items))
    for tcmnames_item in tcmnames_items:
        tcm_items = tcmnames_item.split('：')
        jsonStr += tcm_items[0] + '":"' + tcm_items[1] + '","'

    # print(jsonStr)

    for index in range(1, length):
        dtStr = dts[index].get_text().encode('utf-8').replace('\r\n', ' ').replace('"', '').strip()
        ddStr = dds[index].get_text().encode('utf-8').replace('\r\n', ' ').replace('"', '').strip()
        # print('----')
        # print(repr(ddStr))

        if index == length - 1:
            #end
            jsonStr += dtStr + '":"' + ddStr + '"}'
        else:
            jsonStr += dtStr + '":"' + ddStr + '","'

    if jsonStr != '{"':
        return jsonStr
    else:
        return ''

# save to file
def save_to_file(path, jsonlist):
    if jsonlist == None:
        return

    # open file
    with open(path, mode='w') as file:

        for json_str in jsonlist:

            file.write(json_str + '\n')




#############################
if __name__ == '__main__':
    url = 'http://drugs.yaojia.org/index.php?m=drugs&c=index&a=show&catid=7&id='
    path = '/Users/heermaster/PycharmProjects/webscrapyofTCM/src/tcmproducts.txt'
    tcmprescription_path = '/Users/heermaster/PycharmProjects/webscrapyofTCM/src/tcmproducts.txt'
    page_num = 677

    max_page_num = 1740

    jsonlist = []
    prescription_list = []

    # parse
    while page_num <= max_page_num:
        print(page_num)
        text = get_text_from_web(url, page_num)

        json_str = parse_page(text)

        if json_str:
            jsonlist.append(json_str)

        page_num += 1
    print('len: ' + str(len(jsonlist)))

    # save to file
    print('begin to write')
    save_to_file(path, jsonlist)
    print('write successed!')


