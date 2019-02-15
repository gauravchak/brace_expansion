from typing import List


class BENode(object):
    '''
    Generic Node of the parse tree we are building.
    Every node in this parse tree should be able to return a list of strings.
    '''

    def __init__(self) -> None:
        self.parent = None
        self.type = 0
        # 0 means STR, 1 means CONCAT, 2 means OR, 3 means SEQUENCE, 4 means OR | SEQ
        self.list_str: List[str] = []
        # Return value of node.
        # TODO:

    def parse_next_char(self, nextchar: str) -> bool:
        '''
        Handles the next char and returns false if it cannot accomodate the new character.
        Note that nextchar is of type string and not char since Python doe snot have char data type
        '''
        pass

    def handle_eof(self) -> bool:
        pass