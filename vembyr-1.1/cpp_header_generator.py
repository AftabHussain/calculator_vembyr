# Generates a header file (.h) for the c++ parser generator so that
# the parser functions can be used in other files. Uses an interpreter style

def generate_guard(peg):
    guard = "peg"
    for module in peg.module:
        guard = guard + "_" + module
    return guard

def generate(peg):
    guard = generate_guard(peg)
    
    code = """
    /* filename should be a path to a file */
    extern const void * parse(const std::string & filename, bool stats = false);

    /* data contains the bytes that will be parsed. data should be null-terminated */
    extern const void * parse(const char * data, bool stats = false);

    /* parses the bytes from 'in' which has the length 'length' */
    extern const void * parse(const char * in, int length, bool stats = false);

    /* ParseException can be thrown by the parser in case of parser failure */
    class ParseException: public std::exception {
    public:
        std::string getReason() const;
        int getLine() const;
        int getColumn() const;
        virtual ~ParseException() throw();
    };
    """

    namespaces = """
%s
%s
%s
""" % (peg.cppNamespaceStart(), code, peg.cppNamespaceEnd())

    return """
#ifndef _%s_
#define _%s_

#include <string>

%s

#endif
""" % (guard, guard, namespaces)
