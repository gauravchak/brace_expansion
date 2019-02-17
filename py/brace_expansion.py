'''
A file with utility that generates a string given a string with braces.

Some examples and what they expand to:
  {aa,bb,cc,dd}  => aa bb cc dd
  {0..12}        => 0 1 2 3 4 5 6 7 8 9 10 11 12
  {3..-2}        => 3 2 1 0 -1 -2
  {a..g}         => a b c d e f g
  {g..a}         => g f e d c b a

If the brace expansion has a prefix or suffix string then those strings are included in the expansion:
  a{0..3}b       => a0b a1b a2b a3b

Brace expansions can be nested:
  {a,b{1..3},c}  => a b1 b2 b3 c

Reference: https://www.linuxjournal.com/content/bash-brace-expansion
'''

from typing import List

from betree import BENode


def brace_expansion_vec(complex_str: str) -> List[str]:
    '''Takes a complex string like {ab,cd} and returns a List of strings like ['ab','cd']'''
    # Build a tree of nodes
    root_node = BENode()
    next_char_proc_already = False
    for idx, next_char in enumerate(complex_str):
        if next_char_proc_already:
            # Ignore this iteration since it has been processed already
            next_char_proc_already = False
            continue
        if ((next_char == '.') and (idx + 1 < len(complex_str)) and (complex_str[idx + 1] == '.')):
            next_char = '..'
            parsed = root_node.parse_next_char(next_char)
            next_char_proc_already = True
        else:
            parsed = root_node.parse_next_char(next_char)
            if not parsed:
                root_node.print_entire_tree()
                raise ValueError('Parsing failed at root node next_char={}'.format(next_char))
    # The tree might need knowing that the string has ended. Hence call eof
    parsed = root_node.handle_eof()
    if not parsed:
        raise ValueError('Parsing failed at root node EOF')
    # print('\nFor debugging input {} tree-whoami:'.format(complex_str))
    # root_node.print_entire_tree()
    # Get a list of strings from this tree
    list_of_strings = root_node.get_list_of_strings()
    return (list_of_strings)


def brace_expansion(complex_str: str) -> str:
    '''
    Takes a complex string like {ab,cd} and returns a brace expanded string like "ab cd"
    '''
    expanded_list_of_strings = brace_expansion_vec(complex_str)
    ret_str = ''
    try:
        ret_str = " ".join(expanded_list_of_strings)
    except TypeError:
        if expanded_list_of_strings:
            print('type = {} el1 = {}'.format(type(expanded_list_of_strings[0]), expanded_list_of_strings))
    return (ret_str)
