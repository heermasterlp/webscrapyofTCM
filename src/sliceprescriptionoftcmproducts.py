#coding:utf-8
import json
import re
'''
    Get the prescriptions of tcm products from the data file.
'''

prescription_pattern = u'[\u4e00-\u9fff]+'
measure_pattern = u'[0-9]+'
unit_pattern = u'[a-zA-Z]+'
preparation_pattern = '[（.*）]+'


#  Parse the prescriptions of products
#   the data format: 产品名称：xx,处方:xx,计量:88,单位:,制法:炒
def parse(prescriptions_str):

    result_list = []

    # result = ''
    if prescriptions_str == '':
        return result_list

    # parse process
    prescription_list = prescriptions_str.split('|')
    print(len(prescription_list))

    if len(prescription_list) == 0:
        return result_list

    # parse the item of list
    for prescription_item in prescription_list:

        #params
        pres_str = ''
        measure_str = ''
        unit_str = ''
        preparation_str = ''
        #process item
        print(repr(prescription_item.encode('utf-8').decode('utf-8')))

        # prescription text.encode('latin-1').decode('unicode_escape')
        if re.search(preparation_pattern, prescription_item):
            pres_str = re.search(preparation_pattern, prescription_item).group(0).strip().encode('utf-8')
            print(type(pres_str))

        # measure
        if re.search(measure_pattern, prescription_item):
            measure_str = re.search(measure_pattern, prescription_item).group(0).strip().encode('utf-8')

        # unit
        if re.search(unit_pattern, prescription_item):
            unit_str = re.search(unit_pattern, prescription_item).group(0).strip().encode('utf-8')

        # preparation
        if re.search(preparation_pattern, prescription_item):
            preparation_str = re.search(preparation_pattern, prescription_item).group(0).strip().encode('utf-8')
        print(type(preparation_str))
        result = '"处方":"' + str(pres_str) + '","剂量":"' + str(measure_str) + '","单位":"' + str(unit_str) + '","制法":"' + str(preparation_str) + '"'

        print(type(result))
        result_list.append(result)

    return result_list


###################################
if __name__ == '__main__':

    product_data_file = '/Users/heermaster/Documents/UM/ICMSRA/2015phramsdata/2015products.txt'

    prescription_data_file = '/Users/heermaster/PycharmProjects/webscrapyofTCM/src/2015prescriptions.txt'

    # Read data from the products data file.
    with open(prescription_data_file, 'w') as out_file:
        with open(product_data_file, 'r') as in_file:
            index = 0
            for line in in_file:
                print('index:' + str(index))
                try:

                    json_data = json.loads(line)
                    # product string
                    product_str = json_data['中文名']
                    # process the prescriptions of products
                    prescriptions_str = json_data['处方']

                    # the data format: 产品名称：xx,处方:xx,计量:88,单位:,制法:炒
                    result_list = parse(prescriptions_str)

                    if result_list == None or len(result_list) == 0:
                        continue

                    # write to target file
                    for result_item in result_list:
                        result_item_str = '{"产品名称":"' + product_str + '",' + result_item + '}'
                        print(type(result_item_str))
                        out_file.write(result_item_str + '\n')
                except json.decoder.JSONDecodeError:
                    print('error index: ' + str(index))


                # exit()
                index += 1