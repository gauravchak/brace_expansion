'''Tests for brace_expansion'''

from brace_expansion import brace_expansion

if __name__ == "__main__":
    test_cases = {
        'abc': 'abc',
        '{aa,bb,cc,dd}': 'aa bb cc dd',
        '{0..12}': '0 1 2 3 4 5 6 7 8 9 10 11 12',
        '{3..-2}': '3 2 1 0 -1 -2',
        '{a..g}': 'a b c d e f g',
        '{g..a}': 'g f e d c b a',
        'a{0..3}b': 'a0b a1b a2b a3b',
        'a{b,c}d': 'abd acd',
        '{a,b{1..3},c}': 'a b1 b2 b3 c',
        'a{{0,3},2}b{h,w}': 'a0bh a0bw a3bh a3bw a2bh a2bw',
        # 'a{{0,3}2}b{h,w}': 'a{02}bh a{02}bw a{32}bh a{32}bw' # not working yet
    }
    for input_str, exp_output in test_cases.items():
        print('Testing input string: {}'.format(input_str))
        output_str = brace_expansion(input_str)
        if (output_str != exp_output):
            raise ValueError('Error in brace_expansion. For {} expected {} got {}'.format(
                input_str, exp_output, output_str))
    print('Passed tests')
