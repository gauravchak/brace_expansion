/**
Bash brace expansion is used to generate stings at the command line or in a shell script. The syntax for brace expansion consists of either a sequence specification or a comma separated list of items inside curly braces "{}". A sequence consists of a starting and ending item separated by two periods "..".

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

Ref: https://www.linuxjournal.com/content/bash-brace-expansion
 */
