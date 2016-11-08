#coding:utf-8
import json
import re
'''
    Get the prescription from data

'''
# prescription_patterns = r'[\u4e00-\u9fff]+(（[\u4e00-\u9fff]+）)*'
prescription_patterns = r'([\u4e00-\u9fff]+(（[\u4e00-\u9fff]*[^0-9a-zA-Z]）)*)+'
# remove_patterns = r'[0-9a-zA-Z.]*(（[\u4e00-\u9fff]+）)*'



def parse_text(line):
    '''
    Parse the text to get the prescriptions.

    :param line:
    :return:

    Text file format:

    product_name: prescription, methods: method_name
    '''
    try:
        jsondata = json.loads(line.replace(r'\r\n|\t\t', ' '), strict=False)
        # print(len(jsondata))
        # print(jsondata.keys())

        if jsondata == None:
            print('error json data')
            return ''
        contents = ''

        if '处方' in jsondata:

            prescriptions = jsondata['处方']
            tcmname = jsondata['中文名']

            # find all the prescriptions of tcm
            # print(type(prescriptions))
            descri_items = re.findall(prescription_patterns,prescriptions)
            # descri_fix = prescriptions.replace(remove_patterns, ' ')
            # print(descri_fix)
            # print(len(descri_items))
            items_str = ''
            index = 0
            for item in descri_items:
                if index == len(descri_items) - 1:
                    items_str += item[0]
                else:
                    items_str += item[0] + '|'
                index += 1
                # print(item[0])

            return tcmname + '#' + items_str

        else:
            print('no prescriptions')
            return ''
    except json.JSONDecodeError:
        print('Error!')
        return ''

    return ''


#############################

path = '/Users/heermaster/Documents/python/TCMProducts.txt'
prescriptionpath = '/Users/heermaster/Documents/python/TCMPrescription.txt'

with open(prescriptionpath, 'w') as outfile:

    contents = ''
    with open(path, 'r') as file:
        for line in file:
            contents = parse_text(line)
            # print(contents)
            # xx#xx|xx|xx|xx
            if contents != '':
                content_str = ''
                content_items = contents.split('#')
                medicine_items = content_items[1].split('|')
                for med_item in medicine_items:
                    # split the medicines and methods
                    med_item = med_item.strip()
                    content_str = ''
                    if '（' in med_item:
                        med_items = med_item.split('（')
                        content_str = '{"' + content_items[0] + '":"' + med_items[0] + '","制法":"' + '' + med_items[1].replace('）','') +'"}\n'

                    else:
                        content_str = '{"' + content_items[0] + '":"' + med_item + '"}\n'
                    outfile.write(content_str)


