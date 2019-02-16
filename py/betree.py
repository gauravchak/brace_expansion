from typing import List

from get_list_of_strings import get_list_of_str_from_list


class BENode(object):
    '''
    Generic Node of the parse tree we are building.
    Every node in this parse tree should be able to return a list of strings.
    '''

    def __init__(self) -> None:
        self.actively_parsing = True
        # Not sure if we will need this in this tree, but parent == SELF if and only if this is the root
        self.parent = self
        # 0 means STR, 1 means CONCAT, 2 means OR, 3 means SEQUENCE, 4 means OR | SEQ
        self.type = 'STR'
        # Return value of node in the function get_list_of_strings
        self.list_str: List[str] = []
        # TODO: Implement whatever else is remaining
        self.my_str = ''  # This is only not '' if it is of type STR
        self.concat_children: List[BENode] = []  # This is only not empty if it is of type CONCAT
        # Note: We are handling OR and SEQ the same, until we know what special type it is
        self.orseq_children: List[BENode] = []
        self.orseq_delim_list: List[str] = []  # These are characters/strings between children of OR and SEQ

    def whoami(self) -> None:
        print('About me {}'.format(self))
        if (self.parent == self):
            print('parent = self = {}'.format(self.parent))
        else:
            print('parent = {}'.format(self.parent))
        print('type = {} actively_parsing = {}'.format(self.type, self.actively_parsing))
        if (self.type == 'STR'):
            print('my_str = {}'.format(self.my_str))
        elif (self.type == 'CONCAT'):
            if self.concat_children:
                for c in self.concat_children:
                    if c:
                        c.whoami()
            else:
                print("I am a weird {} node with no children".format(self.type))
        elif (self.type == 'OR|SEQ') or (self.type == 'OR') or (self.type == 'SEQ'):
            if self.orseq_children:
                for idx, c in enumerate(self.orseq_children):
                    if (idx < len(self.orseq_delim_list)):
                        print('delim: {}'.format(self.orseq_delim_list[idx]))
                    c.whoami()
                if (len(self.orseq_children) < len(self.orseq_delim_list)):
                    for idx in range(len(self.orseq_children), len(self.orseq_delim_list)):
                        print('end delim: {}'.format(self.orseq_delim_list[idx]))
            else:
                print("I am a weird {} node with no children".format(self.type))

    def parse_next_char(self, next_char: str) -> bool:
        '''
        Handles the next char and returns false if it cannot accomodate the new character.
        Note that next_char is of type string and not char since Python doe snot have char data type
        '''
        if (self.type == 'STR'):
            # STR type. If we see a special character like "{,}.." then we have to go up and
            # say that this is not ours to handle.
            if ((next_char == '}') or (next_char == ',') or (next_char == '..')):
                # Since this is a special character, move active parsing to a higher level.
                self.actively_parsing = False
                self.set_list_of_strings()
                return (False)
            elif (next_char == '{'):
                # This was earlier of type string but now that it has seen a special character it should
                # turn into concat
                self.type = 'CONCAT'
                if (self.my_str):
                    # Only add a child string node if and only if the current string is non-empty
                    # If it is empty then we have encountered '{' at the first step
                    self.concat_children = [BENode()]
                    # We are adding a closed node since it has already been parsed. Hence actively_parsing is False
                    self.concat_children[0].actively_parsing = False
                    self.concat_children[0].parent = self
                    self.concat_children[0].type = 'STR'
                    self.concat_children[0].my_str = self.my_str
                    self.concat_children[0].concat_children.clear()
                    # We need to finalize the list of strings since actively parsing has been turned off
                    self.concat_children[0].set_list_of_strings()
                else:
                    # If it is empty then we have encountered '{' at the first step
                    # In this case we don't need to make a string child
                    # But we should initialize self.concat_children
                    self.concat_children.clear()
                # Since this is no longer of type 'STR' we should set my_str to None
                self.my_str = ''
                # Since we have seen a '{' we should start a OR|SEQ child node
                self.concat_children.append(BENode())
                # use index -1 to access last item of list
                self.concat_children[-1].actively_parsing = True
                self.concat_children[-1].parent = self
                self.concat_children[-1].type = 'OR|SEQ'
                # Send the character '{' to the OR|SEQ node.
                parsed = self.concat_children[-1].parse_next_char(next_char)
                if not parsed:
                    raise ValueError('There is no reason for an ORSEQ node to not handle the starting \'{\'')
                return (parsed)
                # TODO: revise
            else:
                # Since this is a string type node, it should append this string to the current string
                if (self.my_str):
                    self.my_str = self.my_str + next_char
                else:
                    self.my_str = next_char
                return (True)
        elif (self.type == 'OR|SEQ'):
            # If given the first { then just add it to self.orseq_delim_list and return true
            if not self.orseq_delim_list:
                # if delimiter list is empty then we are expecting curly braces
                if (next_char == '{'):
                    self.orseq_delim_list = [next_char]
                    # Initialize first child of type string
                    self.orseq_children = [BENode()]
                    self.orseq_children[-1].parent = self
                    self.orseq_children[-1].actively_parsing = True
                    self.orseq_children[-1].type = 'STR'
                else:
                    raise ValueError('First character of OR|SEQ should be { and not {}'.format(next_char))
                return True
            else:
                if not self.orseq_children:
                    # It is not expected to not have children at this stage
                    raise ValueError('Somehow children are missing at ORSEQ node {}'.format(self))
                else:
                    # if we have children who have control pass the character to them.
                    # If they return false then handle it.
                    if self.orseq_children[-1].actively_parsing:
                        parsed = self.orseq_children[-1].parse_next_char(next_char)
                        if not parsed:
                            # Like if this was an STR node and it saw a '}' or ','
                            if (next_char == ','):
                                self.orseq_children.append(BENode())
                                self.orseq_children[-1].parent = self
                                self.orseq_children[-1].actively_parsing = True
                                self.orseq_children[-1].type = 'STR'
                                # TODO: we can set self.type = 'OR'
                                # However, we are choosing to do it when self.actively_parsing = False
                                self.orseq_delim_list.append(next_char)
                                return True
                            elif (next_char == '..'):
                                self.orseq_children.append(BENode())
                                self.orseq_children[-1].parent = self
                                self.orseq_children[-1].actively_parsing = True
                                self.orseq_children[-1].type = 'STR'
                                # TODO: we can set self.type = 'SEQ'
                                # However, we are choosing to do it when self.actively_parsing = False
                                self.orseq_delim_list.append(next_char)
                                return True
                            elif (next_char == '}'):
                                self.actively_parsing = False
                                self.orseq_delim_list.append(next_char)
                                self.set_list_of_strings()
                                return True
                            else:
                                # the actively parsing child returned false and closed shop and yet it is not a special
                                # character?!?
                                raise ValueError('Non special miscreant character = {} at {}'.format(next_char, self))
                                return False
                        else:
                            # If parsed then return True
                            return parsed
            raise ValueError('Unhandled ORSEQ returning False to parsing')  # not possible only written as a fuse
            return (False)
        elif (self.type == 'CONCAT'):
            # if last child is actively parsing let it. If it fails then do something.
            if self.concat_children:
                # Check if the last child is actively parsing
                if self.concat_children[-1].actively_parsing:
                    # Usual case
                    parsed = self.concat_children[-1].parse_next_char(next_char)
                    if parsed:
                        return parsed
                    else:
                        print("Debug parse_next_char::CONCAT WHOMAI")
                        self.whoami()
                        raise ValueError(
                            'Why have we received a False to parsing in CONCAT? next_char = {}'.format(next_char))
                else:
                    # This can happen if the last child was a SEQ or OR and it sets actively_parsing = False
                    # Hence we have to add a new node. Since we don't know much about it, we are adding a STR
                    # node and calling parse on it.
                    self.concat_children.append(BENode())
                    self.concat_children[-1].actively_parsing = True
                    self.concat_children[-1].parent = self
                    self.concat_children[-1].type = 'STR'
                    parsed = self.concat_children[-1].parse_next_char(next_char)
                    if parsed:
                        return parsed
                    else:
                        # For example for input string:
                        # {a,b{1..3},c}
                        # we can get here with the comma just before c at the end
                        # self.concat_children[-1].actively_parsing was False since the SEQ node was done
                        # We added a new STR node assuming a string will follow.
                        # However, seeing a special character it returned parsed = false.
                        # The right thing to do is to close this CONCAT node and to send the comma up to the OR node to
                        # handle.
                        self.actively_parsing = False
                        self.set_list_of_strings()
                        return False
            else:
                raise ValueError('165, dont know why I would ever be here. There should always be children of concat')
            return (False)

    def handle_eof(self) -> bool:
        '''
        Tells tree that the string has ended and there isn't anything more to parse.
        Returns False if one encountered an error
        '''
        if (self.type == 'STR'):
            self.actively_parsing = False
            self.set_list_of_strings()
            return (True)
        elif (self.type == 'CONCAT'):
            if self.concat_children and self.concat_children[-1].actively_parsing:
                self.concat_children[-1].handle_eof()
            self.actively_parsing = False
            self.set_list_of_strings()
            return (True)
        return (False)

    def set_list_of_strings(self) -> None:
        '''Constructs the variable list_str, which is the return value of each node'''
        if (self.type == 'STR'):
            # If node type is just a string then we will just return a one element list
            if (self.my_str):
                self.list_str = [self.my_str]
            else:
                self.list_str = []
        elif (self.type == 'OR|SEQ'):
            if ((len(self.orseq_delim_list) == 3) and (self.orseq_delim_list[0] == '{')
                    and (self.orseq_delim_list[1] == '..') and (self.orseq_delim_list[-1] == '}')):
                # Sequence:
                self.type = 'SEQ'
                str1 = self.orseq_children[0].my_str
                str2 = self.orseq_children[1].my_str
                try:
                    int1 = int(str1)
                    int2 = int(str2)
                    if (int1 < int2):
                        # ascending
                        self.list_str = [str(x) for x in list(range(int1, 1 + int2))]
                    else:
                        # descending sequence
                        self.list_str = [str(x) for x in list(range(int1, int2 - 1, -1))]
                except ValueError:
                    # Either of them is not int
                    if (str1.isalpha() and str2.isalpha()):
                        ord1 = ord(str1)
                        ord2 = ord(str2)
                        if (ord1 < ord2):
                            self.list_str = [chr(x) for x in list(range(ord1, 1 + ord2))]
                        else:
                            self.list_str = [chr(x) for x in list(range(ord1, ord2 - 1, -1))]
                    else:
                        self.list_str = [str1 + '..' + str2]
                        # TODelete
                        # print('DEBUG SEQ str1 {} str2 {}'.format(str1, str2))
            elif ((len(self.orseq_delim_list) >= 3) and (self.orseq_delim_list[0] == '{')
                  and (self.orseq_delim_list[-1] == '}') and (set(self.orseq_delim_list[1:-1]) == set([',']))):
                # Valid OR
                self.type = 'OR'
                # Concatenating multiple lists Ref: https://stackoverflow.com/a/3021669/408936
                list_of_lists_of_strings_from_children = [c.get_list_of_strings() for c in self.orseq_children]
                self.list_str = sum(list_of_lists_of_strings_from_children, [])
                # TODelete
                # print('DEBUG set_list_of_strings::OR {} child1 {}'.format(self.list_str,
                #                                                           self.orseq_children[0].get_list_of_strings()))
                # This step guarantees that there are no empty strings. Ref: https://stackoverflow.com/a/3845453/408936
                # If str_list was ['a', '', 'df']
                # then str_list = list(filter(None, str_list))
                # would make it ['a', 'df']
                self.list_str = list(filter(None, self.list_str))
            else:
                # TODO: It could be "{{0,3,}2}"
                # In this case we should make it a CONCAT node and create strings like that.
                raise ValueError(
                    'OR|SEQ node does not look right. Delims: {} Lendelims = {} Delimset = {} Numchildren = {}'.format(
                        ' '.join(self.orseq_delim_list), len(self.orseq_delim_list), set(self.orseq_delim_list[1:-1]),
                        len(self.orseq_children)))
        elif (self.type == 'CONCAT'):
            # Get a list of lists of strings
            list_of_lists_of_strings = [c.get_list_of_strings() for c in self.concat_children]
            # TODelete
            # print('DEBUG CONCAT init1 = {} child1 = {}'.format(list_of_lists_of_strings,
            #                                                    self.concat_children[-1].get_list_of_strings()))

            # # Remove emoty strings from each list
            [list(filter(None, t_list)) for t_list in list_of_lists_of_strings]
            # Remove empty lists from the list
            list_of_lists_of_strings = list(filter(None, list_of_lists_of_strings))
            self.list_str = get_list_of_str_from_list(list_of_lists_of_strings)

    def get_list_of_strings(self) -> List[str]:
        # TODelete
        # if self.list_str == ['0', '1', '2', '3']:
        #     self.whoami()
        return (self.list_str)
