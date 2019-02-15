from typing import List


class BENode(object):
    '''
    Generic Node of the parse tree we are building.
    Every node in this parse tree should be able to return a list of strings.
    '''

    def __init__(self) -> None:
        self.actively_parsing = True
        # Not sure if we will need this in a tree
        self.parent = None
        # 0 means STR, 1 means CONCAT, 2 means OR, 3 means SEQUENCE, 4 means OR | SEQ
        self.type = 'STR'
        # Return value of node in the function get_list_of_strings
        self.list_str: List[str] = []
        # TODO: Implement whatever else is remaining
        self.my_str = None  # This is only not None if it is of type STR
        self.concat_children = None  # This is only not None if it is of type CONCAT
        self.orseq_children = None  # We are handling OR and SEQ the same, until we know what special type it is
        self.orseq_delim_list = None  # These are characters/strings between children of or and seq

    def parse_next_char(self, nextchar: str) -> bool:
        '''
        Handles the next char and returns false if it cannot accomodate the new character.
        Note that nextchar is of type string and not char since Python doe snot have char data type
        '''
        if (self.type == 'STR'):
            # STR type. If we see a special character like "{,}.." then we have to go up and
            # say that this is not ours to handle.
            if ((nextchar == '}') or (nextchar == ',') or (nextchar == '..')):
                # Since this is a special character, move active parsing to a higher level.
                self.actively_parsing = False
                self.set_list_of_strings()
                return (False)
            elif (nextchar == '{'):
                # This was earlier of type string but now that it has seen a special character it should
                # turn into concat
                self.type = 'CONCAT'
                if (self.my_str):
                    # Only add a child string node if and only if the current string is non-empty
                    # If it is empty then we have encountered '{' at the first step
                    self.concat_children = [BENode()]
                    self.concat_children[0].actively_parsing = False
                    self.concat_children[0].parent = self
                    self.concat_children[0].type = 'STR'
                    self.concat_children[0].my_str = self.my_str
                    self.concat_children[0].concat_children = None
                # Since this is no longer of type 'STR' we should set my_str to None
                self.my_str = None
                # Since we have seen a '{' we should start a OR|SEQ child node
                self.concat_children.append(BENode())
                # use index -1 to access last item of list
                self.concat_children[-1].actively_parsing = True
                self.concat_children[-1].parent = self
                self.concat_children[-1].type = 'OR|SEQ'
                self.concat_children[-1].parse_next_char(nextchar)

            else:
                # Since this is a string type node, it should append this string to the current string
                if (self.my_str):
                    self.my_str = self.my_str + nextchar
                else:
                    self.my_str = nextchar
                return (True)

    def handle_eof(self) -> bool:
        '''
        Tells tree that the string has ended and there isn't anything more to parse.
        '''
        if (self.type == 0):
            self.actively_parsing = False
            self.set_list_of_strings()
            return (False)

    def set_list_of_strings(self) -> None:
        '''Constructs the variable list_str, which is the return value of each node'''
        if (self.type == 0):
            # If node type is just a string then we will just return a one element list
            if (self.my_str):
                self.list_str = [self.my_str]
            else:
                self.list_str = []

    def get_list_of_strings(self) -> List[str]:
        # TODO: Implement
        return (self.list_str)