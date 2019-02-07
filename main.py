import analyser
import itertools
from difflib import SequenceMatcher
from celery import shared_task

MARKERS = [
    'receipt', 'policy', 'invoice'
]


def cut_line(line):
    splitted_line = line.split(' ')
    for word in splitted_line:
        if word in MARKERS:
            return ' '.join(splitted_line[:splitted_line.index(word)])
    return line


def single_list(lst, output=None):
    output = []
    for elem in lst:
        if elem is not None:
            if type(elem) == list:
                output = single_list(elem, output)
            else:
                output.append(elem)
    return output


def cmp_data(data, res, category, ratio):
    res_list = list()
    if category == 'text':
        text = data.get('value').lower()
        for key, value in res.items():
            if key != 'category':
                if any(list(map(lambda x: SequenceMatcher(None, text, cut_line(x)).ratio() >= ratio,
                                single_list(list(value))))):
                    res_dict = dict(
                        key=key,
                        value=True
                    )
                    res_list.append(res_dict)
        return res_list
    elif category == 'numeric':
        try:
            amount = float(data.get('value'))
        except ValueError:
            return None
        for key, value in res.items():
            if key != 'category':
                if any(list(map(lambda elem: float(elem) == float(amount), single_list(list(value))))):
                    res_dict = dict(
                        key=key,
                        value=True
                    )
                    res_list.append(res_dict)
        return res_list


def launcher(data, path, name, limit, user, ratio):
    auto_approve = False
    results = analyser.launcher(path=path, name=name, limit_value=limit, user=user)
    if results is not None:
        res_lst = list()
        for v1, v2 in itertools.product(data.values(), results):
            if v1.get('category') == v2.get('category'):
                res = [{'key': v1.get('category'), 'value': cmp_data(data=v1,
                                                                     res=v2,
                                                                     category=v1.get('category'),
                                                                     ratio=ratio)}]
                res_lst.extend(res)
        if all(any(value for value in elem.get('value')) for elem in res_lst):
            auto_approve = True
            return auto_approve, res_lst
        return auto_approve, None
    else:
        return auto_approve, None


if __name__ == "__main__":
    @shared_task
    def ocr_processing(data, claim):
        user_data = {'name': {'value': claim.user.first_name + ' ' + claim.user.last_name, 'category': 'text'},
                     'total': {'value': float(claim.incurred_amount), 'category': 'numeric'}
                     }
        filename = data.get('name')
        path_to_file = data.get('file')
        lv = 20
        ratio = 0.75
        return launcher(data=user_data, path=path_to_file, name=filename, limit=lv, user=claim.user.username,
                        ratio=ratio)

