class BENode:
    '''
    Generic Node of the parse tree we are building
    '''

    def __init__(self) -> None:
        self.parent = None
        # TODO:

    def parse_next_char(self, nextchar: str) -> bool:
        '''
        Handles the next char and returns false if it cannot accomodate the new character. 
        Note that nextchar is of type string and not char since Python doe snot have char data type
        '''