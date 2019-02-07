
# if priority: k1 = 10, k2 = 5
KEYWORDS = [{'priority': 1, 'values': ['total',  'total paid', 'paid', 'total amount',
                                       'amount', 'total amount paid'],
             'k': 10, 'category': 'numeric'},
            {'priority': 2, 'values': ['patient name', 'name', 'payer name', 'invoice'], 'k': 5, 'category': 'text'},
            {'priority': 3, 'values': ['bill date', 'date'], 'k': 1, 'category': 'date'},
            {'priority': 4, 'values': ['address', 'account no.', 'receipt no', 'id no'], 'k': 1, 'category': 'text'},
            {'priority': 5, 'values': ['tax invoice', 'gst regn no', 'card',
                                       'gst', 'total charges', 'total charges before gst',
                                       'total charges after gst', 'total balance'], 'k': 1, 'category': 'text'}]


def create_line_array(filepath):
    text_lines = []
    for line in open(filepath, 'r'):
        text_line = list()
        text_line.append(line.strip())
        text_lines.append(text_line)
    text_lines = [elem for elem in text_lines if elem != ['']]
    return text_lines


def modify_keywords_list(lst):
    output = list()
    for elem in lst:
        if isinstance(elem, str):
            output.append(elem)
            output.append(elem + ':')
    return output


def if_line_is_empty(line, keyword):
    modified_line = line[0].lower().split(' ')
    modified_keyword = keyword.lower()
    cut_line = modified_line[modified_line.index(modified_keyword)+1:]
    if len(cut_line) == 0:
        return True
    return False


def text_parser(list_of_lines, keywords):
    priority = keywords.get('priority')
    list_of_keywords = modify_keywords_list(keywords.get('values'))
    res_points, results_dict = int(), dict()
    for num, line in enumerate(list_of_lines):
        if len(line) != 0:
            set_split_line = set(line[0].lower().split(' '))
            set_list_of_keywords = set(list_of_keywords)
            interception_list = list(set_split_line & set_list_of_keywords)
            if len(interception_list) > 0:
                for item in interception_list:
                    if priority <= 2:
                        if not if_line_is_empty(line=line, keyword=item):
                            if results_dict.get(item):
                                results_dict[item].extend(line)
                            else:
                                results_dict[item] = line
                        else:
                            line_index = num + 1 if len(list_of_lines) != num+1 else num
                            if results_dict.get(item):
                                results_dict[item].extend(list_of_lines[line_index])
                            else:
                                results_dict[item] = list_of_lines[line_index]
                        results_dict['category'] = keywords.get('category')
                        res_points += len(interception_list) * keywords.get('k')
                    else:
                        res_points += len(interception_list) * keywords.get('k')
    return results_dict if len(results_dict) != 0 else None, res_points


def get_results_from_text_file(path):
    lines_list = create_line_array(filepath=path)
    total_points, general_results = int(), list()
    for keyword_list in KEYWORDS:
        results, points = text_parser(list_of_lines=lines_list, keywords=keyword_list)
        total_points += points
        general_results.append(results) if results is not None else None
    return general_results, total_points

