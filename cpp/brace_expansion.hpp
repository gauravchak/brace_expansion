/**
Bash brace expansion is used to generate stings at the command line or in a
shell script. The syntax for brace expansion consists of either a sequence
specification or a comma separated list of items inside curly braces "{}". A
sequence consists of a starting and ending item separated by two periods "..".

Some examples and what they expand to:

  {aa,bb,cc,dd}  => aa bb cc dd
  {0..12}        => 0 1 2 3 4 5 6 7 8 9 10 11 12
  {3..-2}        => 3 2 1 0 -1 -2
  {a..g}         => a b c d e f g
  {g..a}         => g f e d c b a

If the brace expansion has a prefix or suffix string then those strings are
included in the expansion:
 a{0..3}b       => a0b a1b a2b a3b

Brace expansions can be nested:
 {a,b{1..3},c}  => a b1 b2 b3 c

Ref: https://www.linuxjournal.com/content/bash-brace-expansion
 */

#include <string>
#include <vector>

#include "betree.hpp"

using namespace std;

#define MAX_STR_LEN 10000

// Returns a vector of expanded strings
vector<string> get_vec_string_after_brace_expansion(const string &input_str)
{
  // initialize to empty vector
  vector<string> ret_vec;

  // if string is very large then just return empty vector
  // if string is empty then return emoty vector
  if ((input_str.length() >= MAX_STR_LEN) || (input_str.empty()))
  {
    return ret_vec;
  }

  // Build a tree of nodes
  BENode ctop(input_str);

  // Compute vector of strings
  ret_vec = ctop.get_vec_strings();

  return (ret_vec);
}

// Returns a string after space-delimited-concatenation
// Given ["abc", "def"] it will return "abc def"
string sp_concat_vec_strings(const vector<string> &vec_str)
{
  // TODO:
  return "";
}

// Returns a string after space-delimited-concatenating all the expanded strings
string get_string_after_brace_expansion(const string &input_str)
{
  auto vec_str = get_vec_string_after_brace_expansion(input_str);
  string concat_str = sp_concat_vec_strings(vec_str);
  return (concat_str);
}
