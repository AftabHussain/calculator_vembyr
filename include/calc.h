
#ifndef _peg_Parser_
#define _peg_Parser_

#include <string>



namespace Parser{



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
    


} /* Parser */



#endif
