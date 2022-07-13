import re


def get_number_from_str(string):
    temp = re.findall(r'\d+', string)
    res = list(map(int, temp))
    return res[0] if res else 0