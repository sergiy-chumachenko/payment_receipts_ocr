from parser import get_results_from_text_file
from processor import processing
import os
import re

BASE_DIR = os.path.abspath(os.curdir)


def row_analyser_text(row, key):
    row_list = str(row).lower().split(' ')
    for i, j in enumerate(row_list):
        if key == j:
            result = ' '.join(filter(lambda x: x.isalpha(), row_list[i + 1:]))
            return result


def row_analyser_number(row):
    check_list, clean_lst = [elem for elem in str(row).lower().split(' ') if any(char.isdigit() for char in elem)],\
                            list()
    for elem in check_list:
        if elem is not None:
            clean_lst.append(re.sub("[^0123456789\.]", "", elem))

    if len(clean_lst) > 0:
        if len(clean_lst) == 1:
            return clean_lst[0]
        else:
            return clean_lst


def text_analyser(res_dict):
    result = {}
    for key, value in res_dict.items():
        result[key] = list(map(row_analyser_text, (row for row in res_dict.get(key)), [key]))
    if len(result) > 0:
        result['category'] = 'text'
    return result


def numeric_analyser(res_dict):
    result = {}
    for key, value in res_dict.items():
        result[key] = list(map(row_analyser_number, (row for row in res_dict.get(key))))
    if len(result) > 0:
        result['category'] = 'numeric'
    return result


def results_analyser(res_lst):
    res = []
    for dictionary in res_lst:
        if dictionary.get('category') == 'text':
            result_from_text = text_analyser({i: v for i, v in dictionary.items() if i != "category"})
            if result_from_text is not None:
                res.append(result_from_text)
        elif dictionary.get('category') == 'numeric':
            result_from_numeric = numeric_analyser({i: v for i, v in dictionary.items() if i != "category"})
            if result_from_numeric is not None:
                res.append(result_from_numeric)
    return res


def launcher(path, name, limit_value, user):
    path_to_text_file = processing(path_to_image=path, filename=name, user=user)
    results_list, res_points = get_results_from_text_file(path=path_to_text_file)
    if res_points < limit_value:
        return None
    clean_results = results_analyser(results_list)
    return clean_results
