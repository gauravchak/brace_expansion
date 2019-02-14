import re
from typing import List


def get_list_of_str_from_list(l_of_l_of_s: list) -> list:
    '''
    Given a list of list of strings this returns a list of strings of all possible permutations'''
    if not l_of_l_of_s:
        # if the given list was empty then return an empty list
        return []
    el1 = l_of_l_of_s[0]  # since the list was not empty first element exists
    l_of_rest = get_list_of_str_from_list(l_of_l_of_s=l_of_l_of_s[1:])
    if not l_of_rest:
        # if returned list was empty
        return el1
    fin_list = []
    for t_str in el1:
        for suf_str in l_of_rest:
            fin_list.append(t_str + suf_str)
    return fin_list


class TopLvlObj:
    '''A top level Object of the complex str. Complex strings can only be top level objects separated by comma'''

    def __init__(self, g_str: str) -> None:
        '''the given string g_str can either a simple string or a complex_string starting and ending with {}'''
        # Check if the given string is simple or complex
        if re.match(r'{[a-zA-Z0-9.{}]+}', g_str):
            self.is_complex = True
            self.complex_str = g_str
            self.simple_str = ''
        else:
            self.is_complex = False
            self.simple_str = g_str
            self.complex_str = ''


def get_list_of_tlo(cmplx_str: str) -> List[TopLvlObj]:
    '''
    Given a list of complex strings this returns a list of TopLvlObj
    '''
    # I tried the following but that will not work since it might match a closing brace with the wrong opening brace
    # c_dict = re.match(r"(?P<simple_prefix_str>[\S]+){(?P<cmplx_intstr>.+)}(?P<simple_suffix_str>[\S]+)", cmplx_str)