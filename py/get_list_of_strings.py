from typing import List


def get_list_of_str_from_list(l_of_l_of_s: List[List[str]]) -> List[str]:
    '''
    Given a list of list of strings this returns a list of strings of all possible permutations.
    Given [['a'],['b','c'],['d']] returns ['abd', 'acd']
    '''
    # TODelete
    # print('DEBUG get_list_of_str_from_list called with {}'.format(l_of_l_of_s))
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
