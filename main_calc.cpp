#include "include/error.h"
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string.h>
#include <fstream>
#include "include/calc.h"

void print_usage()
{
  std::cerr << "Usage:\n  ./compiler input" << std::endl;
  exit(0);
}

int main(int argc, char ** argv)
{
  if (argc != 2) {
    print_usage();
  }
  std::cout<<"[main/main.cpp] Enter main\n";

  try {
    char* file = argv[1];

    Parser::parse(std::string(file));

    ErrorReport* er = ErrorReport::instance();
    if (er->errors()) {
      std::cerr << "There were errors during parsing\n";
      // TODO: cleanup?
      exit(0);
    }

    return 0;
  } catch (const Parser::ParseException & e) {
    std::cerr << "\n\nALERT!!! - Caught parser exception" << std::endl;
    std::cerr << e.getReason() << std::endl;
    exit(0);
  }
}
