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
from get_list_of_strings import get_list_of_str_from_list


def brace_expansion_vec(complex_str: str) -> List[str]:
    # Build a tree of nodes
    # Get a list of list of strings from this tree
    # From this list of lists of strings, make a list of strings
    return ([])  # TODO implement


def brace_expansion(complex_str: str) -> str:
    return " ".join(brace_expansion_vec(complex_str))
