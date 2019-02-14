#include <iostream>
#include <map>
#include <string>
#include <tuple>

#include "../brace_expansion.hpp"

using namespace std;

int main(int argc, char **argv)
{
    map<string, string> list_of_cases;
    /**
Some examples and what they expand to:

{aa,bb,cc,dd}  => aa bb cc dd
{0..12}        => 0 1 2 3 4 5 6 7 8 9 10 11 12
{3..-2}        => 3 2 1 0 -1 -2
{a..g}         => a b c d e f g
{g..a}         => g f e d c b a
*/
    list_of_cases.insert(pair<string, string>("abc", "abc"));
    list_of_cases.insert(pair<string, string>("{aa,bb,cc,dd}", "aa bb cc dd"));
    /**
If the brace expansion has a prefix or suffix string then those strings
are included in the expansion: 

a{0,3}b       => a0b a3b
a{0..3}b       => a0b a1b a2b a3b
*/
    list_of_cases.insert(pair<string, string>("a{0,3}b", "a0b a3b"));
    /**
Brace expansions can be nested:
{a,b{1..3},c}  => a b1 b2 b3 c
*/
    list_of_cases.insert(pair<string, string>("{a,b{1..3},c}", "a b1 b2 b3 c"));

    for (const auto &t_case : list_of_cases)
    {
        const string &input = t_case.first;
        const string &exp_output = t_case.second;
        string output = get_string_after_brace_expansion(input);
        if (exp_output != output)
        {
            cerr << "Failed to expand " << input << endl;
            exit(1);
        }
    }
    return 0;
}
