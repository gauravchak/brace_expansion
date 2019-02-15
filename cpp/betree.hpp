// Data structures to build the parse tree
#include <string>
#include <vector>
using namespace std;

/// Type of BENode
typedef enum {
  SIMPLE_STR,  // Like {sdfdf} This is a leaf node
  PERMUTE,     // Like {a,b}
  RANGE,       // Like {a..e}
  CONCAT       // Like abc{d,e}hw
} nodetype_t;

class ReadingContext {
 public:
  bool braces_read_;
  string string_read_so_far_;
  ReadingContext(bool br, string srsf) : braces_read_(br), string_read_so_far_(srsf) {}
};

class BENode;
class BELeaf : public BENode {
 public:
  BELeaf(const string &i_str) : BENode(ReadingContext(false, ""), "") {
    BENode::str_ = i_str;
    BENode::type_ = SIMPLE_STR;
    BENode::vec_strings_.push_back(i_str);
  }
};

/// Node
class BENode {
 public:
  size_t string_length_read_by_node_;
  nodetype_t type_;
  string str_;  // This variable is used in case this node is of type SIMPLE_STR
  vector<BENode *> child_nodes_;
  vector<string> vec_strings_;  // This is returned in get_vec_strings

  size_t get_string_length_read_by_node() const { return string_length_read_by_node_; }

  // TODO: Add an empty constructor
  BENode() : string_length_read_by_node_(0) {}

  BENode(const ReadingContext &t_given_context_, const string &input_str) : string_length_read_by_node_(0) {
    // If we are the end of the string then this node is just a leaf.
    // If this were anything fancier then we would have seen characters like '}'
    if (input_str.empty()) {
      str_ = t_given_context_.string_read_so_far_;
      string_length_read_by_node_ = input_str.length();  // which is 0
      type_ = SIMPLE_STR;
      // child_nodes_ are empty
      // output vector is just one string
      vec_strings_.push_back(str_);
      return;
    }

    size_t next_idx_of_input_str = 0;
    if (!t_given_context_.braces_read_) {  // If we have not read a brace so far then the only fancy character is '{'
      size_t found = input_str.find('{');  // Only one special character
      // If the returned index == end; then this is a simple string
      if (found == string::npos) {
        str_ = t_given_context_.string_read_so_far_ + input_str;
        string_length_read_by_node_ = input_str.length();
        type_ = SIMPLE_STR;
        // child_nodes_ are empty.
        // output vector is just one string
        vec_strings_.push_back(str_);
        return;
      }
      // If the returned index is neither 0 nor end: the part that we read becomes a simple child node and then set
      // input_str to index ptr and start while loop again
      else if (found > 0) {
        child_nodes_.push_back(new BELeaf(t_given_context_.string_read_so_far_ + input_str.substr(0, found)));
        // TODO: Change this to creating a BELeaf node
        type_ = CONCAT;  // our type is CONCAT since the text has not finished yet
        // Note that after this point t_given_context_.string_seen_already_ is not useful any more.
        next_idx_of_input_str += found;
        // Now we have to read a complex node since we have seen a '{'
      }
      // If the returned index == 0; then try to read a complex node
      else {
        // The very first character is a '{'
      }

      // If we are here then the next chacracter must be '{'
      ReadingContext current_context_(true, "{");
      next_idx_of_input_str++;  // Move ahead one character since we already know this one

      // if t_given_context_.braces_read_ is false then we have to keep reading till the end
      while (next_idx_of_input_str < input_str.length()) {
      }

      // After the loop, if current_context_.string_read_so_far_ is not empty then add a child leaf simple string node
      if (!current_context_.string_read_so_far_.empty()) {
        child_nodes_.push_back(new BELeaf(current_context_.string_read_so_far_));
      }
    } else {
      // Since we have read a '{' already, try to read '}' or ','
      // Either of these special characters means we have to do something for a BraceNode
      // TODO: Handle nesting
      size_t found = input_str.find_first_of("},");
      if (found == string::npos) {  // No special character found till the end
        // Hence this is just string
        str_ = t_given_context_.string_read_so_far_ + input_str;
        type_ = SIMPLE_STR;
        string_length_read_by_node_ = input_str.length();
        // child_nodes_ are empty
        // output vector is just one string
        vec_strings_.push_back(str_);
        return;
      } else if (found == 0) {
        // special characters found at the very beginning. That is also an error
        // I mean it is just a string.
        str_ = t_given_context_.string_read_so_far_ + input_str.at(0);
        type_ = SIMPLE_STR;
        string_length_read_by_node_ = 1;
        // child_nodes_ are empty
        // output vector is just one string
        vec_strings_.push_back(str_);
        // This is interesting. This is the first time we have returned without reaching the end of the string.
        // This is because we start with a '{' and then right after that we find a '}' or ','
        // Both "{}" and "{," probably expand into nothing but themselves.
        // Since this was a fancy node, we should return and tell the calling BENode that this node's job is done
        // and the parent should handle the rest of the input string.
        return;
      } else {
        // special characters found in the middle. Like {a,b} or {a}
        if (input_str.at(found) == '}') {
          // This is also a simple string.
          str_ = t_given_context_.string_read_so_far_ + input_str.substr(0, found + 1);
          type_ = SIMPLE_STR;
          string_length_read_by_node_ = found + 1;
          // next index is not needed since we are calling return but still we are setting it.
          next_idx_of_input_str += found + 1;
          // child_nodes_ are empty
          // output vector is just one string
          vec_strings_.push_back(str_);
          return;
        } else {
          // read character was ','
          // Hence create a node of just the part before the ','
          BENode *this_child_node_ = new BENode(ReadingContext(false, ""), input_str.substr(0, found))
        }
      }
    }

    // Build vec_strings
    // return
  }

  // Returning a copy of the vector of strings that this node expanded into.
  // This assumes that the vector is already built when the node is initialized.
  vector<string> get_vec_strings() { return vec_strings_; }
};
