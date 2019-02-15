'''Tests for brace_expansion'''

from brace_expansion import brace_expansion

if __name__ == "__main__":
    test_cases = {
        'abc': 'abc',
        '{aa,bb,cc,dd}': 'aa bb cc dd',
        '{0..12}': '0 1 2 3 4 5 6 7 8 9 10 11 12',
        '{3..-2}': '3 2 1 0 -1 -2',
        '{a..g}': 'a b c d e f g',
        '{g..a}': 'g f e d c b a'
    }
    for input_str, exp_output in test_cases.items():
        # I have tested the following line works
        # print('{} => {}'.format(input_str, exp_output))
        output_str = brace_expansion(input_str)
        if (output_str != exp_output):
            raise ValueError('Error in brace_expansion. For {} expected {} got {}'.format(
                input_str, exp_output, output_str))
