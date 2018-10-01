
import peg





def special_escape(s):
    return s.replace("\\n", "\\\\n").replace("\\t", "\\\\t").replace("\"", '\\\"').replace("\\r", "\\\\r")

class PegError(Exception):
    def __init__(self):
        Exception.__init__(self)

class NotError(Exception):
    def __init__(self):
        Exception.__init__(self)

class Result:
    def __init__(self, position):
        self.position = position
        self.values = []

    def getPosition(self):
        return self.position

    def nextPosition(self, amount = 1):
        self.position += amount

    def setValue(self, value):
        self.values = value

    def getLastValue(self):
        if type(self.values) is list:
            if len(self.values) > 0:
                return self.values[-1]
            else:
                return None
        return self.values
    
    def matches(self):
        return len(self.values)

    def getValues(self):
        return self.values

    def addResult(self, him):
        self.values.append(him.values)
        self.position = him.position
    
    #def extendResult(self, him):
    #    self.values.extend(him.values)
    #    self.position = him.position

class Stream:
    def __init__(self, filename = None, input = None):
        def read():
            file = open(filename, 'r')
            out = file.read()
            file.close()
            return out
        self.position = 0
        self.limit = 100
        self.furthest = 0
        self.memo = {}
        if filename != None:
            self.all = read()
        elif input != None:
            self.all = input
        else:
            raise PegError("Pass a filename or input")
        # print "Read " + str(len(self.all))

    def get(self, position, number = 1):
        if position + number > self.limit:
            # print (position + number)
            self.limit += 5000
        if position + number > len(self.all):
            return chr(0)
        # print "stream: %s" % self.all[position:position+number]
        return self.all[position:position+number]

    def get2(self, position):
        if position != self.position:
            self.file.seek(position)
        self.position = position + 1
        if position > self.limit:
            print position
            self.limit += 5000
        return self.file.read(1)

    def reportError(self):
        line = 1
        column = 1
        for i in xrange(0, self.furthest):
            if self.all[i] == '\n':
                line += 1
                column = 1
            else:
                column += 1
        context = 10
        left = self.furthest - context
        right = self.furthest + context
        if left < 0:
            left = 0
        if right > len(self.all):
            right = len(self.all)
        out = "Read up till line %d, column %d" % (line, column)
        out += "\n"
        out += "'%s'" % special_escape(self.all[left:right])
        out += "\n"
        out += "%s^" % (' ' * (self.furthest - left))
        return out

    def update(self, rule, position, result):
        if result != None and result.getPosition() > self.furthest:
            self.furthest = result.getPosition()

        for_rule = None
        try:
            for_rule = self.memo[rule]
        except KeyError:
            self.memo[rule] = {}
            for_rule = self.memo[rule]
        
        for_position = None
        try:
            for_position = for_rule[position]
        except KeyError:
            for_rule[position] = None

        for_rule[position] = result

    def hasResult(self, rule, position):
        try:
            x = self.memo[rule][position]
            return True
        except KeyError:
            return False

    def result(self, rule, position):
        return self.memo[rule][position]



RULE_start = 0
RULE_module = 1
RULE_include = 2
RULE_more_code = 3
RULE_options = 4
RULE_option = 5
RULE_chunks = 6
RULE_error_option = 7
RULE_word = 8
RULE_rules = 9
RULE_rule = 10
RULE_pattern_line = 11
RULE_pattern = 12
RULE_raw_code = 13
RULE_code = 14
RULE_item = 15
RULE_failure = 16
RULE_line = 17
RULE_predicate = 18
RULE_utf8 = 19
RULE_ascii = 20
RULE_call_rule = 21
RULE_eof = 22
RULE_void = 23
RULE_range = 24
RULE_sub_pattern = 25
RULE_bind = 26
RULE_string = 27
RULE_modifier = 28
RULE_x_word = 29
RULE_rule_parameters = 30
RULE_value_parameters = 31
RULE_parameters_rules = 32
RULE_parameters_values = 33
RULE_word_or_dollar = 34
RULE_word_or_at = 35
RULE_word_at = 36
RULE_dollar = 37
RULE_number = 38
RULE_digit = 39
RULE_hex_number = 40
RULE_hex_digit = 41
RULE_start_symbol = 42
RULE_spaces = 43
RULE_space = 44
RULE_any_char = 45
RULE_any = 46
RULE_whitespace = 47
RULE_comment = 48
RULE_newlines_one = 49
RULE_newlines = 50




def rule_start(stream, position):
    if stream.hasResult(RULE_start, position):
        return stream.result(RULE_start, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'newlines'
        result_peg_2 = rule_newlines(stream, result_peg_2.getPosition())
        if result_peg_2 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'whitespace'
        result_peg_3 = rule_whitespace(stream, result_peg_3.getPosition())
        if result_peg_3 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_3);
        
        result_peg_4 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'start_symbol'
        result_peg_4 = rule_start_symbol(stream, result_peg_4.getPosition())
        if result_peg_4 == None:
            raise PegError
        start_symbol = result_peg_4.getValues()
        
        result_peg_1.addResult(result_peg_4);
        
        result_peg_5 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'newlines'
        result_peg_5 = rule_newlines(stream, result_peg_5.getPosition())
        if result_peg_5 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_5);
        
        result_peg_6 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'whitespace'
        result_peg_6 = rule_whitespace(stream, result_peg_6.getPosition())
        if result_peg_6 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_6);
        
        result_peg_7 = Result(result_peg_1.getPosition())
        
        try:
            save_peg_8 = result_peg_7.getPosition()
            
            # print "Trying rule " + 'options'
            result_peg_7 = rule_options(stream, result_peg_7.getPosition())
            if result_peg_7 == None:
                raise PegError
            
        except PegError:
            result_peg_7 = Result(save_peg_8)
            result_peg_7.setValue(None)
        options = result_peg_7.getValues()
        
        result_peg_1.addResult(result_peg_7);
        
        result_peg_9 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'newlines'
        result_peg_9 = rule_newlines(stream, result_peg_9.getPosition())
        if result_peg_9 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_9);
        
        result_peg_10 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'whitespace'
        result_peg_10 = rule_whitespace(stream, result_peg_10.getPosition())
        if result_peg_10 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_10);
        
        result_peg_11 = Result(result_peg_1.getPosition())
        
        try:
            save_peg_12 = result_peg_11.getPosition()
            
            # print "Trying rule " + 'module'
            result_peg_11 = rule_module(stream, result_peg_11.getPosition())
            if result_peg_11 == None:
                raise PegError
            
        except PegError:
            result_peg_11 = Result(save_peg_12)
            result_peg_11.setValue(None)
        module = result_peg_11.getValues()
        
        result_peg_1.addResult(result_peg_11);
        
        result_peg_13 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'newlines'
        result_peg_13 = rule_newlines(stream, result_peg_13.getPosition())
        if result_peg_13 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_13);
        
        result_peg_14 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'whitespace'
        result_peg_14 = rule_whitespace(stream, result_peg_14.getPosition())
        if result_peg_14 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_14);
        
        result_peg_15 = Result(result_peg_1.getPosition())
        
        try:
            save_peg_16 = result_peg_15.getPosition()
            
            # print "Trying rule " + 'include'
            result_peg_15 = rule_include(stream, result_peg_15.getPosition())
            if result_peg_15 == None:
                raise PegError
            
        except PegError:
            result_peg_15 = Result(save_peg_16)
            result_peg_15.setValue(None)
        include = result_peg_15.getValues()
        
        result_peg_1.addResult(result_peg_15);
        
        result_peg_17 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'newlines'
        result_peg_17 = rule_newlines(stream, result_peg_17.getPosition())
        if result_peg_17 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_17);
        
        result_peg_18 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'whitespace'
        result_peg_18 = rule_whitespace(stream, result_peg_18.getPosition())
        if result_peg_18 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_18);
        
        result_peg_19 = Result(result_peg_1.getPosition())
        
        try:
            save_peg_20 = result_peg_19.getPosition()
            
            # print "Trying rule " + 'more_code'
            result_peg_19 = rule_more_code(stream, result_peg_19.getPosition())
            if result_peg_19 == None:
                raise PegError
            
        except PegError:
            result_peg_19 = Result(save_peg_20)
            result_peg_19.setValue(None)
        code = result_peg_19.getValues()
        
        result_peg_1.addResult(result_peg_19);
        
        result_peg_21 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'newlines'
        result_peg_21 = rule_newlines(stream, result_peg_21.getPosition())
        if result_peg_21 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_21);
        
        result_peg_22 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'whitespace'
        result_peg_22 = rule_whitespace(stream, result_peg_22.getPosition())
        if result_peg_22 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_22);
        
        result_peg_23 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'rules'
        result_peg_23 = rule_rules(stream, result_peg_23.getPosition())
        if result_peg_23 == None:
            raise PegError
        rules = result_peg_23.getValues()
        
        result_peg_1.addResult(result_peg_23);
        
        result_peg_24 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'newlines'
        result_peg_24 = rule_newlines(stream, result_peg_24.getPosition())
        if result_peg_24 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_24);
        
        result_peg_25 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'whitespace'
        result_peg_25 = rule_whitespace(stream, result_peg_25.getPosition())
        if result_peg_25 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_25);
        
        result_peg_26 = Result(result_peg_1.getPosition())
        
        if chr(0) == stream.get(result_peg_26.getPosition()):
            result_peg_26.nextPosition()
            result_peg_26.setValue(chr(0))
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_26);
        
        result_peg_27 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = peg.Peg(start_symbol, include, code, module, rules, options)
        result_peg_27.setValue(value)
        
        result_peg_1.addResult(result_peg_27);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_start, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_start, position, None)
    return None


def rule_module(stream, position):
    if stream.hasResult(RULE_module, position):
        return stream.result(RULE_module, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        if 'module:' == stream.get(result_peg_2.getPosition(), 7):
            result_peg_2.nextPosition(7)
            result_peg_2.setValue('module:')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'spaces'
        result_peg_3 = rule_spaces(stream, result_peg_3.getPosition())
        if result_peg_3 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_3);
        
        result_peg_4 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'word'
        result_peg_4 = rule_word(stream, result_peg_4.getPosition())
        if result_peg_4 == None:
            raise PegError
        name = result_peg_4.getValues()
        
        result_peg_1.addResult(result_peg_4);
        
        result_peg_5 = Result(result_peg_1.getPosition())
        
        try:
            while True:
                result_peg_6 = Result(result_peg_5.getPosition());
                result_peg_7 = Result(result_peg_6.getPosition())
                
                if '.' == stream.get(result_peg_7.getPosition(), 1):
                    result_peg_7.nextPosition(1)
                    result_peg_7.setValue('.')
                else:
                    raise PegError
                
                result_peg_6.addResult(result_peg_7);
                
                result_peg_8 = Result(result_peg_6.getPosition())
                
                # print "Trying rule " + 'word'
                result_peg_8 = rule_word(stream, result_peg_8.getPosition())
                if result_peg_8 == None:
                    raise PegError
                
                result_peg_6.addResult(result_peg_8);
                
                result_peg_9 = Result(result_peg_6.getPosition())
                
                value = None
                values = result_peg_6.getValues()
                value = values[1]
                result_peg_9.setValue(value)
                
                result_peg_6.addResult(result_peg_9);
                
                result_peg_6.setValue(result_peg_6.getLastValue())
                result_peg_5.addResult(result_peg_6);
        except PegError:
            pass
        rest = result_peg_5.getValues()
        
        result_peg_1.addResult(result_peg_5);
        
        result_peg_10 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = [name] + rest
        result_peg_10.setValue(value)
        
        result_peg_1.addResult(result_peg_10);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_module, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_module, position, None)
    return None


def rule_include(stream, position):
    if stream.hasResult(RULE_include, position):
        return stream.result(RULE_include, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        if 'include:' == stream.get(result_peg_2.getPosition(), 8):
            result_peg_2.nextPosition(8)
            result_peg_2.setValue('include:')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'spaces'
        result_peg_3 = rule_spaces(stream, result_peg_3.getPosition())
        if result_peg_3 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_3);
        
        result_peg_4 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'code'
        result_peg_4 = rule_code(stream, result_peg_4.getPosition())
        if result_peg_4 == None:
            raise PegError
        code = result_peg_4.getValues()
        
        result_peg_1.addResult(result_peg_4);
        
        result_peg_5 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = code.code
        result_peg_5.setValue(value)
        
        result_peg_1.addResult(result_peg_5);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_include, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_include, position, None)
    return None


def rule_more_code(stream, position):
    if stream.hasResult(RULE_more_code, position):
        return stream.result(RULE_more_code, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        if 'code:' == stream.get(result_peg_2.getPosition(), 5):
            result_peg_2.nextPosition(5)
            result_peg_2.setValue('code:')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'spaces'
        result_peg_3 = rule_spaces(stream, result_peg_3.getPosition())
        if result_peg_3 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_3);
        
        result_peg_4 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'code'
        result_peg_4 = rule_code(stream, result_peg_4.getPosition())
        if result_peg_4 == None:
            raise PegError
        code = result_peg_4.getValues()
        
        result_peg_1.addResult(result_peg_4);
        
        result_peg_5 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = code.code
        result_peg_5.setValue(value)
        
        result_peg_1.addResult(result_peg_5);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_more_code, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_more_code, position, None)
    return None


def rule_options(stream, position):
    if stream.hasResult(RULE_options, position):
        return stream.result(RULE_options, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        if 'options:' == stream.get(result_peg_2.getPosition(), 8):
            result_peg_2.nextPosition(8)
            result_peg_2.setValue('options:')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'spaces'
        result_peg_3 = rule_spaces(stream, result_peg_3.getPosition())
        if result_peg_3 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_3);
        
        result_peg_4 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'option'
        result_peg_4 = rule_option(stream, result_peg_4.getPosition())
        if result_peg_4 == None:
            raise PegError
        option1 = result_peg_4.getValues()
        
        result_peg_1.addResult(result_peg_4);
        
        result_peg_5 = Result(result_peg_1.getPosition())
        
        try:
            while True:
                result_peg_6 = Result(result_peg_5.getPosition());
                result_peg_7 = Result(result_peg_6.getPosition())
                
                # print "Trying rule " + 'spaces'
                result_peg_7 = rule_spaces(stream, result_peg_7.getPosition())
                if result_peg_7 == None:
                    raise PegError
                
                result_peg_6.addResult(result_peg_7);
                
                result_peg_8 = Result(result_peg_6.getPosition())
                
                if ',' == stream.get(result_peg_8.getPosition(), 1):
                    result_peg_8.nextPosition(1)
                    result_peg_8.setValue(',')
                else:
                    raise PegError
                
                result_peg_6.addResult(result_peg_8);
                
                result_peg_9 = Result(result_peg_6.getPosition())
                
                # print "Trying rule " + 'spaces'
                result_peg_9 = rule_spaces(stream, result_peg_9.getPosition())
                if result_peg_9 == None:
                    raise PegError
                
                result_peg_6.addResult(result_peg_9);
                
                result_peg_10 = Result(result_peg_6.getPosition())
                
                # print "Trying rule " + 'option'
                result_peg_10 = rule_option(stream, result_peg_10.getPosition())
                if result_peg_10 == None:
                    raise PegError
                
                result_peg_6.addResult(result_peg_10);
                
                result_peg_6.setValue(result_peg_6.getLastValue())
                result_peg_5.addResult(result_peg_6);
        except PegError:
            pass
        option_rest = result_peg_5.getValues()
        
        result_peg_1.addResult(result_peg_5);
        
        result_peg_11 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = []
        for option in ([option1] + option_rest):
            import re
            debug = re.compile("debug(\d+)")
            out = debug.match(option)
            if out != None:
                num = int(out.group(1))
                for x in xrange(1,num+1):
                    value.append('debug%d' % x)
            elif option == 'no-memo':
                value.append(option)
            else:
                value.append(option)
        result_peg_11.setValue(value)
        
        result_peg_1.addResult(result_peg_11);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_options, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_options, position, None)
    return None


def rule_option(stream, position):
    if stream.hasResult(RULE_option, position):
        return stream.result(RULE_option, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        if 'debug' == stream.get(result_peg_2.getPosition(), 5):
            result_peg_2.nextPosition(5)
            result_peg_2.setValue('debug')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'number'
        result_peg_3 = rule_number(stream, result_peg_3.getPosition())
        if result_peg_3 == None:
            raise PegError
        number = result_peg_3.getValues()
        
        result_peg_1.addResult(result_peg_3);
        
        result_peg_4 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = 'debug%s' % number
        result_peg_4.setValue(value)
        
        result_peg_1.addResult(result_peg_4);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_option, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    try:
        result_peg_5 = Result(position)
        if 'state' == stream.get(result_peg_5.getPosition(), 5):
            result_peg_5.nextPosition(5)
            result_peg_5.setValue('state')
        else:
            raise PegError
        stream.update(RULE_option, position, result_peg_5)
        return result_peg_5
    except PegError:
        pass
    try:
        result_peg_6 = Result(position)
        if 'no-memo' == stream.get(result_peg_6.getPosition(), 7):
            result_peg_6.nextPosition(7)
            result_peg_6.setValue('no-memo')
        else:
            raise PegError
        stream.update(RULE_option, position, result_peg_6)
        return result_peg_6
    except PegError:
        pass
    try:
        result_peg_7 = Result(position)
        # print "Trying rule " + 'error_option'
        result_peg_7 = rule_error_option(stream, result_peg_7.getPosition())
        if result_peg_7 == None:
            raise PegError
        stream.update(RULE_option, position, result_peg_7)
        return result_peg_7
    except PegError:
        pass
    try:
        result_peg_8 = Result(position)
        # print "Trying rule " + 'chunks'
        result_peg_8 = rule_chunks(stream, result_peg_8.getPosition())
        if result_peg_8 == None:
            raise PegError
        stream.update(RULE_option, position, result_peg_8)
        return result_peg_8
    except PegError:
        pass
    stream.update(RULE_option, position, None)
    return None


def rule_chunks(stream, position):
    if stream.hasResult(RULE_chunks, position):
        return stream.result(RULE_chunks, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        if 'chunks' == stream.get(result_peg_2.getPosition(), 6):
            result_peg_2.nextPosition(6)
            result_peg_2.setValue('chunks')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'whitespace'
        result_peg_3 = rule_whitespace(stream, result_peg_3.getPosition())
        if result_peg_3 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_3);
        
        result_peg_4 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'number'
        result_peg_4 = rule_number(stream, result_peg_4.getPosition())
        if result_peg_4 == None:
            raise PegError
        number = result_peg_4.getValues()
        
        result_peg_1.addResult(result_peg_4);
        
        result_peg_5 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = 'chunks %s' % number
        result_peg_5.setValue(value)
        
        result_peg_1.addResult(result_peg_5);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_chunks, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_chunks, position, None)
    return None


def rule_error_option(stream, position):
    if stream.hasResult(RULE_error_option, position):
        return stream.result(RULE_error_option, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        if 'error-length' == stream.get(result_peg_2.getPosition(), 12):
            result_peg_2.nextPosition(12)
            result_peg_2.setValue('error-length')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'whitespace'
        result_peg_3 = rule_whitespace(stream, result_peg_3.getPosition())
        if result_peg_3 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_3);
        
        result_peg_4 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'number'
        result_peg_4 = rule_number(stream, result_peg_4.getPosition())
        if result_peg_4 == None:
            raise PegError
        number = result_peg_4.getValues()
        
        result_peg_1.addResult(result_peg_4);
        
        result_peg_5 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = 'error-length %s' % number
        result_peg_5.setValue(value)
        
        result_peg_1.addResult(result_peg_5);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_error_option, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_error_option, position, None)
    return None


def rule_word(stream, position):
    if stream.hasResult(RULE_word, position):
        return stream.result(RULE_word, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        try:
            while True:
                result_peg_3 = Result(result_peg_2.getPosition());
                # print "Trying rule " + 'any_char'
                result_peg_3 = rule_any_char(stream, result_peg_3.getPosition())
                if result_peg_3 == None:
                    raise PegError
                result_peg_2.addResult(result_peg_3);
        except PegError:
            if result_peg_2.matches() == 0:
                raise PegError
                
        result_peg_1.addResult(result_peg_2);
        
        result_peg_4 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        # print "all start symbol values " + str(values)
        # print "values[0] " + str(values[0])
        value = ''.join(values[0]).replace('-', '__')
        # print "got word " + value
        result_peg_4.setValue(value)
        
        result_peg_1.addResult(result_peg_4);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_word, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_word, position, None)
    return None


def rule_rules(stream, position):
    if stream.hasResult(RULE_rules, position):
        return stream.result(RULE_rules, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        if 'rules:' == stream.get(result_peg_2.getPosition(), 6):
            result_peg_2.nextPosition(6)
            result_peg_2.setValue('rules:')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'whitespace'
        result_peg_3 = rule_whitespace(stream, result_peg_3.getPosition())
        if result_peg_3 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_3);
        
        result_peg_4 = Result(result_peg_1.getPosition())
        
        try:
            while True:
                result_peg_5 = Result(result_peg_4.getPosition());
                result_peg_6 = Result(result_peg_5.getPosition())
                
                # print "Trying rule " + 'rule'
                result_peg_6 = rule_rule(stream, result_peg_6.getPosition())
                if result_peg_6 == None:
                    raise PegError
                
                result_peg_5.addResult(result_peg_6);
                
                result_peg_7 = Result(result_peg_5.getPosition())
                
                # print "Trying rule " + 'whitespace'
                result_peg_7 = rule_whitespace(stream, result_peg_7.getPosition())
                if result_peg_7 == None:
                    raise PegError
                
                result_peg_5.addResult(result_peg_7);
                
                result_peg_8 = Result(result_peg_5.getPosition())
                
                value = None
                values = result_peg_5.getValues()
                value = values[0]
                result_peg_8.setValue(value)
                
                result_peg_5.addResult(result_peg_8);
                
                result_peg_5.setValue(result_peg_5.getLastValue())
                result_peg_4.addResult(result_peg_5);
        except PegError:
            pass
        rules = result_peg_4.getValues()
        
        result_peg_1.addResult(result_peg_4);
        
        result_peg_9 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = rules
        result_peg_9.setValue(value)
        
        result_peg_1.addResult(result_peg_9);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_rules, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_rules, position, None)
    return None


def rule_rule(stream, position):
    if stream.hasResult(RULE_rule, position):
        return stream.result(RULE_rule, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'spaces'
        result_peg_2 = rule_spaces(stream, result_peg_2.getPosition())
        if result_peg_2 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        try:
            save_peg_4 = result_peg_3.getPosition()
            
            if 'inline' == stream.get(result_peg_3.getPosition(), 6):
                result_peg_3.nextPosition(6)
                result_peg_3.setValue('inline')
            else:
                raise PegError
            
        except PegError:
            result_peg_3 = Result(save_peg_4)
            result_peg_3.setValue(None)
        inline = result_peg_3.getValues()
        
        result_peg_1.addResult(result_peg_3);
        
        result_peg_5 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'spaces'
        result_peg_5 = rule_spaces(stream, result_peg_5.getPosition())
        if result_peg_5 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_5);
        
        result_peg_6 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'word'
        result_peg_6 = rule_word(stream, result_peg_6.getPosition())
        if result_peg_6 == None:
            raise PegError
        name = result_peg_6.getValues()
        
        result_peg_1.addResult(result_peg_6);
        
        result_peg_7 = Result(result_peg_1.getPosition())
        
        try:
            save_peg_8 = result_peg_7.getPosition()
            
            # print "Trying rule " + 'rule_parameters'
            result_peg_7 = rule_rule_parameters(stream, result_peg_7.getPosition())
            if result_peg_7 == None:
                raise PegError
            
        except PegError:
            result_peg_7 = Result(save_peg_8)
            result_peg_7.setValue(None)
        rule_parameters = result_peg_7.getValues()
        
        result_peg_1.addResult(result_peg_7);
        
        result_peg_9 = Result(result_peg_1.getPosition())
        
        try:
            save_peg_10 = result_peg_9.getPosition()
            
            # print "Trying rule " + 'value_parameters'
            result_peg_9 = rule_value_parameters(stream, result_peg_9.getPosition())
            if result_peg_9 == None:
                raise PegError
            
        except PegError:
            result_peg_9 = Result(save_peg_10)
            result_peg_9.setValue(None)
        parameters = result_peg_9.getValues()
        
        result_peg_1.addResult(result_peg_9);
        
        result_peg_11 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'spaces'
        result_peg_11 = rule_spaces(stream, result_peg_11.getPosition())
        if result_peg_11 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_11);
        
        result_peg_12 = Result(result_peg_1.getPosition())
        
        if '=' == stream.get(result_peg_12.getPosition(), 1):
            result_peg_12.nextPosition(1)
            result_peg_12.setValue('=')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_12);
        
        result_peg_13 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'spaces'
        result_peg_13 = rule_spaces(stream, result_peg_13.getPosition())
        if result_peg_13 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_13);
        
        result_peg_14 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'pattern_line'
        result_peg_14 = rule_pattern_line(stream, result_peg_14.getPosition())
        if result_peg_14 == None:
            raise PegError
        pattern1 = result_peg_14.getValues()
        
        result_peg_1.addResult(result_peg_14);
        
        result_peg_15 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'whitespace'
        result_peg_15 = rule_whitespace(stream, result_peg_15.getPosition())
        if result_peg_15 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_15);
        
        result_peg_16 = Result(result_peg_1.getPosition())
        
        try:
            while True:
                result_peg_17 = Result(result_peg_16.getPosition());
                result_peg_18 = Result(result_peg_17.getPosition())
                
                # print "Trying rule " + 'spaces'
                result_peg_18 = rule_spaces(stream, result_peg_18.getPosition())
                if result_peg_18 == None:
                    raise PegError
                
                result_peg_17.addResult(result_peg_18);
                
                result_peg_19 = Result(result_peg_17.getPosition())
                
                if '|' == stream.get(result_peg_19.getPosition(), 1):
                    result_peg_19.nextPosition(1)
                    result_peg_19.setValue('|')
                else:
                    raise PegError
                
                result_peg_17.addResult(result_peg_19);
                
                result_peg_20 = Result(result_peg_17.getPosition())
                
                # print "Trying rule " + 'spaces'
                result_peg_20 = rule_spaces(stream, result_peg_20.getPosition())
                if result_peg_20 == None:
                    raise PegError
                
                result_peg_17.addResult(result_peg_20);
                
                result_peg_21 = Result(result_peg_17.getPosition())
                
                # print "Trying rule " + 'pattern_line'
                result_peg_21 = rule_pattern_line(stream, result_peg_21.getPosition())
                if result_peg_21 == None:
                    raise PegError
                pattern = result_peg_21.getValues()
                
                result_peg_17.addResult(result_peg_21);
                
                result_peg_22 = Result(result_peg_17.getPosition())
                
                # print "Trying rule " + 'whitespace'
                result_peg_22 = rule_whitespace(stream, result_peg_22.getPosition())
                if result_peg_22 == None:
                    raise PegError
                
                result_peg_17.addResult(result_peg_22);
                
                result_peg_23 = Result(result_peg_17.getPosition())
                
                value = None
                values = result_peg_17.getValues()
                value = pattern
                result_peg_23.setValue(value)
                
                result_peg_17.addResult(result_peg_23);
                
                result_peg_17.setValue(result_peg_17.getLastValue())
                result_peg_16.addResult(result_peg_17);
        except PegError:
            pass
        patterns = result_peg_16.getValues()
        
        result_peg_1.addResult(result_peg_16);
        
        result_peg_24 = Result(result_peg_1.getPosition())
        
        try:
            save_peg_25 = result_peg_24.getPosition()
            
            # print "Trying rule " + 'failure'
            result_peg_24 = rule_failure(stream, result_peg_24.getPosition())
            if result_peg_24 == None:
                raise PegError
            
        except PegError:
            result_peg_24 = Result(save_peg_25)
            result_peg_24.setValue(None)
        fail = result_peg_24.getValues()
        
        result_peg_1.addResult(result_peg_24);
        
        result_peg_26 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = peg.Rule(name, [pattern1] + patterns, inline = (inline != None), rules = rule_parameters, parameters = parameters, fail = fail)
        result_peg_26.setValue(value)
        
        result_peg_1.addResult(result_peg_26);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_rule, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_rule, position, None)
    return None


def rule_pattern_line(stream, position):
    if stream.hasResult(RULE_pattern_line, position):
        return stream.result(RULE_pattern_line, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        try:
            while True:
                result_peg_3 = Result(result_peg_2.getPosition());
                # print "Trying rule " + 'pattern'
                result_peg_3 = rule_pattern(stream, result_peg_3.getPosition())
                if result_peg_3 == None:
                    raise PegError
                result_peg_2.addResult(result_peg_3);
        except PegError:
            pass
        patterns = result_peg_2.getValues()
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_4 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = peg.PatternSequence(patterns)
        #if code != None:
        #    value = code(peg.PatternSequence(patterns))
        #else:
        #    value = peg.PatternAction(peg.PatternSequence(patterns), "value = values;")
        result_peg_4.setValue(value)
        
        result_peg_1.addResult(result_peg_4);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_pattern_line, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_pattern_line, position, None)
    return None


def rule_pattern(stream, position):
    if stream.hasResult(RULE_pattern, position):
        return stream.result(RULE_pattern, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        try:
            save_peg_3 = result_peg_2.getPosition()
            
            # print "Trying rule " + 'bind'
            result_peg_2 = rule_bind(stream, result_peg_2.getPosition())
            if result_peg_2 == None:
                raise PegError
            
        except PegError:
            result_peg_2 = Result(save_peg_3)
            result_peg_2.setValue(None)
        bind = result_peg_2.getValues()
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_4 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'item'
        result_peg_4 = rule_item(stream, result_peg_4.getPosition())
        if result_peg_4 == None:
            raise PegError
        item = result_peg_4.getValues()
        
        result_peg_1.addResult(result_peg_4);
        
        result_peg_5 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'spaces'
        result_peg_5 = rule_spaces(stream, result_peg_5.getPosition())
        if result_peg_5 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_5);
        
        result_peg_6 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        # value = peg.PatternRule(values[0])
        if bind != None:
            item = bind(item)
        value = item
        # print "Pattern is " + str(value)
        result_peg_6.setValue(value)
        
        result_peg_1.addResult(result_peg_6);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_pattern, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_pattern, position, None)
    return None


def rule_raw_code(stream, position):
    if stream.hasResult(RULE_raw_code, position):
        return stream.result(RULE_raw_code, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        if '(' == stream.get(result_peg_2.getPosition(), 1):
            result_peg_2.nextPosition(1)
            result_peg_2.setValue('(')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'spaces'
        result_peg_3 = rule_spaces(stream, result_peg_3.getPosition())
        if result_peg_3 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_3);
        
        result_peg_4 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'code'
        result_peg_4 = rule_code(stream, result_peg_4.getPosition())
        if result_peg_4 == None:
            raise PegError
        code = result_peg_4.getValues()
        
        result_peg_1.addResult(result_peg_4);
        
        result_peg_5 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'spaces'
        result_peg_5 = rule_spaces(stream, result_peg_5.getPosition())
        if result_peg_5 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_5);
        
        result_peg_6 = Result(result_peg_1.getPosition())
        
        if ')' == stream.get(result_peg_6.getPosition(), 1):
            result_peg_6.nextPosition(1)
            result_peg_6.setValue(')')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_6);
        
        result_peg_7 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = code.code
        result_peg_7.setValue(value)
        
        result_peg_1.addResult(result_peg_7);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_raw_code, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_raw_code, position, None)
    return None


def rule_code(stream, position):
    if stream.hasResult(RULE_code, position):
        return stream.result(RULE_code, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        if '{{' == stream.get(result_peg_2.getPosition(), 2):
            result_peg_2.nextPosition(2)
            result_peg_2.setValue('{{')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        try:
            while True:
                result_peg_4 = Result(result_peg_3.getPosition());
                result_peg_5 = Result(result_peg_4.getPosition())
                
                result_peg_6 = Result(result_peg_5.getPosition());
                try:
                    if '}}' == stream.get(result_peg_6.getPosition(), 2):
                        result_peg_6.nextPosition(2)
                        result_peg_6.setValue('}}')
                    else:
                        raise NotError
                    raise PegError
                except NotError:
                    result_peg_5.setValue(None)
                        
                result_peg_4.addResult(result_peg_5);
                
                result_peg_7 = Result(result_peg_4.getPosition())
                
                temp_peg_8 = stream.get(result_peg_7.getPosition())
                if temp_peg_8 != chr(0):
                    result_peg_7.setValue(temp_peg_8)
                    result_peg_7.nextPosition()
                else:
                    raise PegError
                
                result_peg_4.addResult(result_peg_7);
                
                result_peg_9 = Result(result_peg_4.getPosition())
                
                value = None
                values = result_peg_4.getValues()
                value = values[1]
                result_peg_9.setValue(value)
                
                result_peg_4.addResult(result_peg_9);
                
                result_peg_4.setValue(result_peg_4.getLastValue())
                result_peg_3.addResult(result_peg_4);
        except PegError:
            if result_peg_3.matches() == 0:
                raise PegError
                
        result_peg_1.addResult(result_peg_3);
        
        result_peg_10 = Result(result_peg_1.getPosition())
        
        if '}}' == stream.get(result_peg_10.getPosition(), 2):
            result_peg_10.nextPosition(2)
            result_peg_10.setValue('}}')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_10);
        
        result_peg_11 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = peg.PatternCode(''.join(values[1]))
        result_peg_11.setValue(value)
        
        result_peg_1.addResult(result_peg_11);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_code, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_code, position, None)
    return None


def rule_item(stream, position):
    if stream.hasResult(RULE_item, position):
        return stream.result(RULE_item, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        try:
            save_peg_3 = result_peg_2.getPosition()
            
            if '&' == stream.get(result_peg_2.getPosition(), 1):
                result_peg_2.nextPosition(1)
                result_peg_2.setValue('&')
            else:
                raise PegError
            
        except PegError:
            result_peg_2 = Result(save_peg_3)
            result_peg_2.setValue(None)
        ensure = result_peg_2.getValues()
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_4 = Result(result_peg_1.getPosition())
        
        try:
            save_peg_5 = result_peg_4.getPosition()
            
            if '!' == stream.get(result_peg_4.getPosition(), 1):
                result_peg_4.nextPosition(1)
                result_peg_4.setValue('!')
            else:
                raise PegError
            
        except PegError:
            result_peg_4 = Result(save_peg_5)
            result_peg_4.setValue(None)
        pnot = result_peg_4.getValues()
        
        result_peg_1.addResult(result_peg_4);
        
        result_peg_6 = Result(result_peg_1.getPosition())
        
        save_peg_7 = result_peg_6.getPosition()
        
        result_peg_6 = Result(save_peg_7)
        # print "Trying rule " + 'x_word'
        result_peg_6 = rule_x_word(stream, result_peg_6.getPosition())
        if result_peg_6 == None:
            
            result_peg_6 = Result(save_peg_7)
            # print "Trying rule " + 'any'
            result_peg_6 = rule_any(stream, result_peg_6.getPosition())
            if result_peg_6 == None:
                
                result_peg_6 = Result(save_peg_7)
                # print "Trying rule " + 'eof'
                result_peg_6 = rule_eof(stream, result_peg_6.getPosition())
                if result_peg_6 == None:
                    
                    result_peg_6 = Result(save_peg_7)
                    # print "Trying rule " + 'void'
                    result_peg_6 = rule_void(stream, result_peg_6.getPosition())
                    if result_peg_6 == None:
                        
                        result_peg_6 = Result(save_peg_7)
                        # print "Trying rule " + 'range'
                        result_peg_6 = rule_range(stream, result_peg_6.getPosition())
                        if result_peg_6 == None:
                            
                            result_peg_6 = Result(save_peg_7)
                            # print "Trying rule " + 'string'
                            result_peg_6 = rule_string(stream, result_peg_6.getPosition())
                            if result_peg_6 == None:
                                
                                result_peg_6 = Result(save_peg_7)
                                # print "Trying rule " + 'line'
                                result_peg_6 = rule_line(stream, result_peg_6.getPosition())
                                if result_peg_6 == None:
                                    
                                    result_peg_6 = Result(save_peg_7)
                                    # print "Trying rule " + 'ascii'
                                    result_peg_6 = rule_ascii(stream, result_peg_6.getPosition())
                                    if result_peg_6 == None:
                                        
                                        result_peg_6 = Result(save_peg_7)
                                        # print "Trying rule " + 'utf8'
                                        result_peg_6 = rule_utf8(stream, result_peg_6.getPosition())
                                        if result_peg_6 == None:
                                            
                                            result_peg_6 = Result(save_peg_7)
                                            # print "Trying rule " + 'predicate'
                                            result_peg_6 = rule_predicate(stream, result_peg_6.getPosition())
                                            if result_peg_6 == None:
                                                
                                                result_peg_6 = Result(save_peg_7)
                                                # print "Trying rule " + 'call_rule'
                                                result_peg_6 = rule_call_rule(stream, result_peg_6.getPosition())
                                                if result_peg_6 == None:
                                                    
                                                    result_peg_6 = Result(save_peg_7)
                                                    # print "Trying rule " + 'sub_pattern'
                                                    result_peg_6 = rule_sub_pattern(stream, result_peg_6.getPosition())
                                                    if result_peg_6 == None:
                                                        
                                                        result_peg_6 = Result(save_peg_7)
                                                        # print "Trying rule " + 'code'
                                                        result_peg_6 = rule_code(stream, result_peg_6.getPosition())
                                                        if result_peg_6 == None:
                                                            raise PegError
        pattern = result_peg_6.getValues()
        
        result_peg_1.addResult(result_peg_6);
        
        result_peg_8 = Result(result_peg_1.getPosition())
        
        try:
            save_peg_9 = result_peg_8.getPosition()
            
            # print "Trying rule " + 'modifier'
            result_peg_8 = rule_modifier(stream, result_peg_8.getPosition())
            if result_peg_8 == None:
                raise PegError
            
        except PegError:
            result_peg_8 = Result(save_peg_9)
            result_peg_8.setValue(None)
        modifier = result_peg_8.getValues()
        
        result_peg_1.addResult(result_peg_8);
        
        result_peg_10 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        if modifier != None:
            pattern = modifier(pattern)
        if pnot != None:
            pattern = peg.PatternNot(pattern)
        if ensure != None:
            pattern = peg.PatternEnsure(pattern)
        value = pattern
        result_peg_10.setValue(value)
        
        result_peg_1.addResult(result_peg_10);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_item, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_item, position, None)
    return None


def rule_failure(stream, position):
    if stream.hasResult(RULE_failure, position):
        return stream.result(RULE_failure, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'whitespace'
        result_peg_2 = rule_whitespace(stream, result_peg_2.getPosition())
        if result_peg_2 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        if '<fail>' == stream.get(result_peg_3.getPosition(), 6):
            result_peg_3.nextPosition(6)
            result_peg_3.setValue('<fail>')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_3);
        
        result_peg_4 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'spaces'
        result_peg_4 = rule_spaces(stream, result_peg_4.getPosition())
        if result_peg_4 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_4);
        
        result_peg_5 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'code'
        result_peg_5 = rule_code(stream, result_peg_5.getPosition())
        if result_peg_5 == None:
            raise PegError
        code = result_peg_5.getValues()
        
        result_peg_1.addResult(result_peg_5);
        
        result_peg_6 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = code.code
        result_peg_6.setValue(value)
        
        result_peg_1.addResult(result_peg_6);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_failure, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_failure, position, None)
    return None


def rule_line(stream, position):
    if stream.hasResult(RULE_line, position):
        return stream.result(RULE_line, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        if '<line>' == stream.get(result_peg_2.getPosition(), 6):
            result_peg_2.nextPosition(6)
            result_peg_2.setValue('<line>')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = peg.PatternLine()
        result_peg_3.setValue(value)
        
        result_peg_1.addResult(result_peg_3);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_line, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_line, position, None)
    return None


def rule_predicate(stream, position):
    if stream.hasResult(RULE_predicate, position):
        return stream.result(RULE_predicate, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        if '<predicate' == stream.get(result_peg_2.getPosition(), 10):
            result_peg_2.nextPosition(10)
            result_peg_2.setValue('<predicate')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'whitespace'
        result_peg_3 = rule_whitespace(stream, result_peg_3.getPosition())
        if result_peg_3 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_3);
        
        result_peg_4 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'word'
        result_peg_4 = rule_word(stream, result_peg_4.getPosition())
        if result_peg_4 == None:
            raise PegError
        variable = result_peg_4.getValues()
        
        result_peg_1.addResult(result_peg_4);
        
        result_peg_5 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'whitespace'
        result_peg_5 = rule_whitespace(stream, result_peg_5.getPosition())
        if result_peg_5 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_5);
        
        result_peg_6 = Result(result_peg_1.getPosition())
        
        if '>' == stream.get(result_peg_6.getPosition(), 1):
            result_peg_6.nextPosition(1)
            result_peg_6.setValue('>')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_6);
        
        result_peg_7 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'whitespace'
        result_peg_7 = rule_whitespace(stream, result_peg_7.getPosition())
        if result_peg_7 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_7);
        
        result_peg_8 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'code'
        result_peg_8 = rule_code(stream, result_peg_8.getPosition())
        if result_peg_8 == None:
            raise PegError
        code = result_peg_8.getValues()
        
        result_peg_1.addResult(result_peg_8);
        
        result_peg_9 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = peg.PatternPredicate(variable, code.code)
        result_peg_9.setValue(value)
        
        result_peg_1.addResult(result_peg_9);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_predicate, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_predicate, position, None)
    return None


def rule_utf8(stream, position):
    if stream.hasResult(RULE_utf8, position):
        return stream.result(RULE_utf8, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        if '<utf8' == stream.get(result_peg_2.getPosition(), 5):
            result_peg_2.nextPosition(5)
            result_peg_2.setValue('<utf8')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'spaces'
        result_peg_3 = rule_spaces(stream, result_peg_3.getPosition())
        if result_peg_3 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_3);
        
        result_peg_4 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'hex_number'
        result_peg_4 = rule_hex_number(stream, result_peg_4.getPosition())
        if result_peg_4 == None:
            raise PegError
        num = result_peg_4.getValues()
        
        result_peg_1.addResult(result_peg_4);
        
        result_peg_5 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'spaces'
        result_peg_5 = rule_spaces(stream, result_peg_5.getPosition())
        if result_peg_5 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_5);
        
        result_peg_6 = Result(result_peg_1.getPosition())
        
        if '>' == stream.get(result_peg_6.getPosition(), 1):
            result_peg_6.nextPosition(1)
            result_peg_6.setValue('>')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_6);
        
        result_peg_7 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = peg.createUtf8Pattern(num)
        result_peg_7.setValue(value)
        
        result_peg_1.addResult(result_peg_7);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_utf8, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_utf8, position, None)
    return None


def rule_ascii(stream, position):
    if stream.hasResult(RULE_ascii, position):
        return stream.result(RULE_ascii, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        if '<ascii' == stream.get(result_peg_2.getPosition(), 6):
            result_peg_2.nextPosition(6)
            result_peg_2.setValue('<ascii')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'spaces'
        result_peg_3 = rule_spaces(stream, result_peg_3.getPosition())
        if result_peg_3 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_3);
        
        result_peg_4 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'number'
        result_peg_4 = rule_number(stream, result_peg_4.getPosition())
        if result_peg_4 == None:
            raise PegError
        num = result_peg_4.getValues()
        
        result_peg_1.addResult(result_peg_4);
        
        result_peg_5 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'spaces'
        result_peg_5 = rule_spaces(stream, result_peg_5.getPosition())
        if result_peg_5 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_5);
        
        result_peg_6 = Result(result_peg_1.getPosition())
        
        if '>' == stream.get(result_peg_6.getPosition(), 1):
            result_peg_6.nextPosition(1)
            result_peg_6.setValue('>')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_6);
        
        result_peg_7 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = peg.PatternVerbatim(int(num))
        result_peg_7.setValue(value)
        
        result_peg_1.addResult(result_peg_7);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_ascii, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_ascii, position, None)
    return None


def rule_call_rule(stream, position):
    if stream.hasResult(RULE_call_rule, position):
        return stream.result(RULE_call_rule, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        if '@' == stream.get(result_peg_2.getPosition(), 1):
            result_peg_2.nextPosition(1)
            result_peg_2.setValue('@')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'word'
        result_peg_3 = rule_word(stream, result_peg_3.getPosition())
        if result_peg_3 == None:
            raise PegError
        name = result_peg_3.getValues()
        
        result_peg_1.addResult(result_peg_3);
        
        result_peg_4 = Result(result_peg_1.getPosition())
        
        try:
            save_peg_5 = result_peg_4.getPosition()
            
            # print "Trying rule " + 'parameters_rules'
            result_peg_4 = rule_parameters_rules(stream, result_peg_4.getPosition())
            if result_peg_4 == None:
                raise PegError
            
        except PegError:
            result_peg_4 = Result(save_peg_5)
            result_peg_4.setValue(None)
        rule_parameters = result_peg_4.getValues()
        
        result_peg_1.addResult(result_peg_4);
        
        result_peg_6 = Result(result_peg_1.getPosition())
        
        try:
            save_peg_7 = result_peg_6.getPosition()
            
            # print "Trying rule " + 'parameters_values'
            result_peg_6 = rule_parameters_values(stream, result_peg_6.getPosition())
            if result_peg_6 == None:
                raise PegError
            
        except PegError:
            result_peg_6 = Result(save_peg_7)
            result_peg_6.setValue(None)
        parameters = result_peg_6.getValues()
        
        result_peg_1.addResult(result_peg_6);
        
        result_peg_8 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = peg.PatternCallRule(name, rule_parameters, parameters)
        result_peg_8.setValue(value)
        
        result_peg_1.addResult(result_peg_8);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_call_rule, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_call_rule, position, None)
    return None


def rule_eof(stream, position):
    if stream.hasResult(RULE_eof, position):
        return stream.result(RULE_eof, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        if '<eof>' == stream.get(result_peg_2.getPosition(), 5):
            result_peg_2.nextPosition(5)
            result_peg_2.setValue('<eof>')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = peg.PatternEof()
        result_peg_3.setValue(value)
        
        result_peg_1.addResult(result_peg_3);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_eof, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_eof, position, None)
    return None


def rule_void(stream, position):
    if stream.hasResult(RULE_void, position):
        return stream.result(RULE_void, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        if '<void>' == stream.get(result_peg_2.getPosition(), 6):
            result_peg_2.nextPosition(6)
            result_peg_2.setValue('<void>')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = peg.PatternVoid()
        result_peg_3.setValue(value)
        
        result_peg_1.addResult(result_peg_3);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_void, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_void, position, None)
    return None


def rule_range(stream, position):
    if stream.hasResult(RULE_range, position):
        return stream.result(RULE_range, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        if '[' == stream.get(result_peg_2.getPosition(), 1):
            result_peg_2.nextPosition(1)
            result_peg_2.setValue('[')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        try:
            while True:
                result_peg_4 = Result(result_peg_3.getPosition());
                result_peg_5 = Result(result_peg_4.getPosition())
                
                result_peg_6 = Result(result_peg_5.getPosition());
                try:
                    if ']' == stream.get(result_peg_6.getPosition(), 1):
                        result_peg_6.nextPosition(1)
                        result_peg_6.setValue(']')
                    else:
                        raise NotError
                    raise PegError
                except NotError:
                    result_peg_5.setValue(None)
                        
                result_peg_4.addResult(result_peg_5);
                
                result_peg_7 = Result(result_peg_4.getPosition())
                
                temp_peg_8 = stream.get(result_peg_7.getPosition())
                if temp_peg_8 != chr(0):
                    result_peg_7.setValue(temp_peg_8)
                    result_peg_7.nextPosition()
                else:
                    raise PegError
                
                result_peg_4.addResult(result_peg_7);
                
                result_peg_9 = Result(result_peg_4.getPosition())
                
                value = None
                values = result_peg_4.getValues()
                value = values[1]
                result_peg_9.setValue(value)
                
                result_peg_4.addResult(result_peg_9);
                
                result_peg_4.setValue(result_peg_4.getLastValue())
                result_peg_3.addResult(result_peg_4);
        except PegError:
            pass
                
        result_peg_1.addResult(result_peg_3);
        
        result_peg_10 = Result(result_peg_1.getPosition())
        
        if ']' == stream.get(result_peg_10.getPosition(), 1):
            result_peg_10.nextPosition(1)
            result_peg_10.setValue(']')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_10);
        
        result_peg_11 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = peg.PatternRange(''.join(values[1]))
        result_peg_11.setValue(value)
        
        result_peg_1.addResult(result_peg_11);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_range, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_range, position, None)
    return None


def rule_sub_pattern(stream, position):
    if stream.hasResult(RULE_sub_pattern, position):
        return stream.result(RULE_sub_pattern, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        if '(' == stream.get(result_peg_2.getPosition(), 1):
            result_peg_2.nextPosition(1)
            result_peg_2.setValue('(')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        try:
            while True:
                result_peg_4 = Result(result_peg_3.getPosition());
                # print "Trying rule " + 'pattern'
                result_peg_4 = rule_pattern(stream, result_peg_4.getPosition())
                if result_peg_4 == None:
                    raise PegError
                result_peg_3.addResult(result_peg_4);
        except PegError:
            if result_peg_3.matches() == 0:
                raise PegError
                
        result_peg_1.addResult(result_peg_3);
        
        result_peg_5 = Result(result_peg_1.getPosition())
        
        if ')' == stream.get(result_peg_5.getPosition(), 1):
            result_peg_5.nextPosition(1)
            result_peg_5.setValue(')')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_5);
        
        result_peg_6 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = peg.PatternSequence(values[1])
        result_peg_6.setValue(value)
        
        result_peg_1.addResult(result_peg_6);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_sub_pattern, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_sub_pattern, position, None)
    return None


def rule_bind(stream, position):
    if stream.hasResult(RULE_bind, position):
        return stream.result(RULE_bind, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'word'
        result_peg_2 = rule_word(stream, result_peg_2.getPosition())
        if result_peg_2 == None:
            raise PegError
        name = result_peg_2.getValues()
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        if ':' == stream.get(result_peg_3.getPosition(), 1):
            result_peg_3.nextPosition(1)
            result_peg_3.setValue(':')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_3);
        
        result_peg_4 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = lambda p: peg.PatternBind(name, p)
        result_peg_4.setValue(value)
        
        result_peg_1.addResult(result_peg_4);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_bind, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_bind, position, None)
    return None


def rule_string(stream, position):
    if stream.hasResult(RULE_string, position):
        return stream.result(RULE_string, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        if '"' == stream.get(result_peg_2.getPosition(), 1):
            result_peg_2.nextPosition(1)
            result_peg_2.setValue('"')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        try:
            while True:
                result_peg_4 = Result(result_peg_3.getPosition());
                result_peg_5 = Result(result_peg_4.getPosition())
                
                result_peg_6 = Result(result_peg_5.getPosition());
                try:
                    if '"' == stream.get(result_peg_6.getPosition(), 1):
                        result_peg_6.nextPosition(1)
                        result_peg_6.setValue('"')
                    else:
                        raise NotError
                    raise PegError
                except NotError:
                    result_peg_5.setValue(None)
                        
                result_peg_4.addResult(result_peg_5);
                
                result_peg_7 = Result(result_peg_4.getPosition())
                
                temp_peg_8 = stream.get(result_peg_7.getPosition())
                if temp_peg_8 != chr(0):
                    result_peg_7.setValue(temp_peg_8)
                    result_peg_7.nextPosition()
                else:
                    raise PegError
                
                result_peg_4.addResult(result_peg_7);
                
                result_peg_9 = Result(result_peg_4.getPosition())
                
                value = None
                values = result_peg_4.getValues()
                value = values[1]
                result_peg_9.setValue(value)
                
                result_peg_4.addResult(result_peg_9);
                
                result_peg_4.setValue(result_peg_4.getLastValue())
                result_peg_3.addResult(result_peg_4);
        except PegError:
            pass
                
        result_peg_1.addResult(result_peg_3);
        
        result_peg_10 = Result(result_peg_1.getPosition())
        
        if '"' == stream.get(result_peg_10.getPosition(), 1):
            result_peg_10.nextPosition(1)
            result_peg_10.setValue('"')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_10);
        
        result_peg_11 = Result(result_peg_1.getPosition())
        
        try:
            save_peg_12 = result_peg_11.getPosition()
            
            if '{case}' == stream.get(result_peg_11.getPosition(), 6):
                result_peg_11.nextPosition(6)
                result_peg_11.setValue('{case}')
            else:
                raise PegError
            
        except PegError:
            result_peg_11 = Result(save_peg_12)
            result_peg_11.setValue(None)
        options = result_peg_11.getValues()
        
        result_peg_1.addResult(result_peg_11);
        
        result_peg_13 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = peg.PatternVerbatim(''.join(values[1]), options)
        result_peg_13.setValue(value)
        
        result_peg_1.addResult(result_peg_13);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_string, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    try:
        result_peg_14 = Result(position)
        result_peg_15 = Result(result_peg_14.getPosition())
        
        if '<quote>' == stream.get(result_peg_15.getPosition(), 7):
            result_peg_15.nextPosition(7)
            result_peg_15.setValue('<quote>')
        else:
            raise PegError
        
        result_peg_14.addResult(result_peg_15);
        
        result_peg_16 = Result(result_peg_14.getPosition())
        
        value = None
        values = result_peg_14.getValues()
        value = peg.PatternVerbatim('"')
        result_peg_16.setValue(value)
        
        result_peg_14.addResult(result_peg_16);
        
        result_peg_14.setValue(result_peg_14.getLastValue())
        stream.update(RULE_string, position, result_peg_14)
        return result_peg_14
    except PegError:
        pass
    stream.update(RULE_string, position, None)
    return None


def rule_modifier(stream, position):
    if stream.hasResult(RULE_modifier, position):
        return stream.result(RULE_modifier, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        if '*' == stream.get(result_peg_2.getPosition(), 1):
            result_peg_2.nextPosition(1)
            result_peg_2.setValue('*')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = lambda p: peg.PatternRepeatMany(p)
        result_peg_3.setValue(value)
        
        result_peg_1.addResult(result_peg_3);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_modifier, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    try:
        result_peg_4 = Result(position)
        result_peg_5 = Result(result_peg_4.getPosition())
        
        if '?' == stream.get(result_peg_5.getPosition(), 1):
            result_peg_5.nextPosition(1)
            result_peg_5.setValue('?')
        else:
            raise PegError
        
        result_peg_4.addResult(result_peg_5);
        
        result_peg_6 = Result(result_peg_4.getPosition())
        
        value = None
        values = result_peg_4.getValues()
        value = lambda p: peg.PatternMaybe(p)
        result_peg_6.setValue(value)
        
        result_peg_4.addResult(result_peg_6);
        
        result_peg_4.setValue(result_peg_4.getLastValue())
        stream.update(RULE_modifier, position, result_peg_4)
        return result_peg_4
    except PegError:
        pass
    try:
        result_peg_7 = Result(position)
        result_peg_8 = Result(result_peg_7.getPosition())
        
        if '+' == stream.get(result_peg_8.getPosition(), 1):
            result_peg_8.nextPosition(1)
            result_peg_8.setValue('+')
        else:
            raise PegError
        
        result_peg_7.addResult(result_peg_8);
        
        result_peg_9 = Result(result_peg_7.getPosition())
        
        value = None
        values = result_peg_7.getValues()
        value = lambda p: peg.PatternRepeatOnce(p)
        result_peg_9.setValue(value)
        
        result_peg_7.addResult(result_peg_9);
        
        result_peg_7.setValue(result_peg_7.getLastValue())
        stream.update(RULE_modifier, position, result_peg_7)
        return result_peg_7
    except PegError:
        pass
    stream.update(RULE_modifier, position, None)
    return None


def rule_x_word(stream, position):
    if stream.hasResult(RULE_x_word, position):
        return stream.result(RULE_x_word, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'word'
        result_peg_2 = rule_word(stream, result_peg_2.getPosition())
        if result_peg_2 == None:
            raise PegError
        name = result_peg_2.getValues()
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        try:
            save_peg_4 = result_peg_3.getPosition()
            
            # print "Trying rule " + 'parameters_rules'
            result_peg_3 = rule_parameters_rules(stream, result_peg_3.getPosition())
            if result_peg_3 == None:
                raise PegError
            
        except PegError:
            result_peg_3 = Result(save_peg_4)
            result_peg_3.setValue(None)
        rule_parameters = result_peg_3.getValues()
        
        result_peg_1.addResult(result_peg_3);
        
        result_peg_5 = Result(result_peg_1.getPosition())
        
        try:
            save_peg_6 = result_peg_5.getPosition()
            
            # print "Trying rule " + 'parameters_values'
            result_peg_5 = rule_parameters_values(stream, result_peg_5.getPosition())
            if result_peg_5 == None:
                raise PegError
            
        except PegError:
            result_peg_5 = Result(save_peg_6)
            result_peg_5.setValue(None)
        parameters = result_peg_5.getValues()
        
        result_peg_1.addResult(result_peg_5);
        
        result_peg_7 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = peg.PatternRule(name, rule_parameters, parameters)
        result_peg_7.setValue(value)
        
        result_peg_1.addResult(result_peg_7);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_x_word, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_x_word, position, None)
    return None


def rule_rule_parameters(stream, position):
    if stream.hasResult(RULE_rule_parameters, position):
        return stream.result(RULE_rule_parameters, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        if '[' == stream.get(result_peg_2.getPosition(), 1):
            result_peg_2.nextPosition(1)
            result_peg_2.setValue('[')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'spaces'
        result_peg_3 = rule_spaces(stream, result_peg_3.getPosition())
        if result_peg_3 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_3);
        
        result_peg_4 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'word'
        result_peg_4 = rule_word(stream, result_peg_4.getPosition())
        if result_peg_4 == None:
            raise PegError
        param1 = result_peg_4.getValues()
        
        result_peg_1.addResult(result_peg_4);
        
        result_peg_5 = Result(result_peg_1.getPosition())
        
        try:
            while True:
                result_peg_6 = Result(result_peg_5.getPosition());
                result_peg_7 = Result(result_peg_6.getPosition())
                
                # print "Trying rule " + 'spaces'
                result_peg_7 = rule_spaces(stream, result_peg_7.getPosition())
                if result_peg_7 == None:
                    raise PegError
                
                result_peg_6.addResult(result_peg_7);
                
                result_peg_8 = Result(result_peg_6.getPosition())
                
                if ',' == stream.get(result_peg_8.getPosition(), 1):
                    result_peg_8.nextPosition(1)
                    result_peg_8.setValue(',')
                else:
                    raise PegError
                
                result_peg_6.addResult(result_peg_8);
                
                result_peg_9 = Result(result_peg_6.getPosition())
                
                # print "Trying rule " + 'spaces'
                result_peg_9 = rule_spaces(stream, result_peg_9.getPosition())
                if result_peg_9 == None:
                    raise PegError
                
                result_peg_6.addResult(result_peg_9);
                
                result_peg_10 = Result(result_peg_6.getPosition())
                
                # print "Trying rule " + 'word'
                result_peg_10 = rule_word(stream, result_peg_10.getPosition())
                if result_peg_10 == None:
                    raise PegError
                exp = result_peg_10.getValues()
                
                result_peg_6.addResult(result_peg_10);
                
                result_peg_11 = Result(result_peg_6.getPosition())
                
                value = None
                values = result_peg_6.getValues()
                value = exp
                result_peg_11.setValue(value)
                
                result_peg_6.addResult(result_peg_11);
                
                result_peg_6.setValue(result_peg_6.getLastValue())
                result_peg_5.addResult(result_peg_6);
        except PegError:
            pass
        params = result_peg_5.getValues()
        
        result_peg_1.addResult(result_peg_5);
        
        result_peg_12 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'spaces'
        result_peg_12 = rule_spaces(stream, result_peg_12.getPosition())
        if result_peg_12 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_12);
        
        result_peg_13 = Result(result_peg_1.getPosition())
        
        if ']' == stream.get(result_peg_13.getPosition(), 1):
            result_peg_13.nextPosition(1)
            result_peg_13.setValue(']')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_13);
        
        result_peg_14 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = [param1] + params
        result_peg_14.setValue(value)
        
        result_peg_1.addResult(result_peg_14);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_rule_parameters, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_rule_parameters, position, None)
    return None


def rule_value_parameters(stream, position):
    if stream.hasResult(RULE_value_parameters, position):
        return stream.result(RULE_value_parameters, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        if '(' == stream.get(result_peg_2.getPosition(), 1):
            result_peg_2.nextPosition(1)
            result_peg_2.setValue('(')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'spaces'
        result_peg_3 = rule_spaces(stream, result_peg_3.getPosition())
        if result_peg_3 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_3);
        
        result_peg_4 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'word'
        result_peg_4 = rule_word(stream, result_peg_4.getPosition())
        if result_peg_4 == None:
            raise PegError
        param1 = result_peg_4.getValues()
        
        result_peg_1.addResult(result_peg_4);
        
        result_peg_5 = Result(result_peg_1.getPosition())
        
        try:
            while True:
                result_peg_6 = Result(result_peg_5.getPosition());
                result_peg_7 = Result(result_peg_6.getPosition())
                
                # print "Trying rule " + 'spaces'
                result_peg_7 = rule_spaces(stream, result_peg_7.getPosition())
                if result_peg_7 == None:
                    raise PegError
                
                result_peg_6.addResult(result_peg_7);
                
                result_peg_8 = Result(result_peg_6.getPosition())
                
                if ',' == stream.get(result_peg_8.getPosition(), 1):
                    result_peg_8.nextPosition(1)
                    result_peg_8.setValue(',')
                else:
                    raise PegError
                
                result_peg_6.addResult(result_peg_8);
                
                result_peg_9 = Result(result_peg_6.getPosition())
                
                # print "Trying rule " + 'spaces'
                result_peg_9 = rule_spaces(stream, result_peg_9.getPosition())
                if result_peg_9 == None:
                    raise PegError
                
                result_peg_6.addResult(result_peg_9);
                
                result_peg_10 = Result(result_peg_6.getPosition())
                
                # print "Trying rule " + 'word'
                result_peg_10 = rule_word(stream, result_peg_10.getPosition())
                if result_peg_10 == None:
                    raise PegError
                exp = result_peg_10.getValues()
                
                result_peg_6.addResult(result_peg_10);
                
                result_peg_11 = Result(result_peg_6.getPosition())
                
                value = None
                values = result_peg_6.getValues()
                value = exp
                result_peg_11.setValue(value)
                
                result_peg_6.addResult(result_peg_11);
                
                result_peg_6.setValue(result_peg_6.getLastValue())
                result_peg_5.addResult(result_peg_6);
        except PegError:
            pass
        params = result_peg_5.getValues()
        
        result_peg_1.addResult(result_peg_5);
        
        result_peg_12 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'spaces'
        result_peg_12 = rule_spaces(stream, result_peg_12.getPosition())
        if result_peg_12 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_12);
        
        result_peg_13 = Result(result_peg_1.getPosition())
        
        if ')' == stream.get(result_peg_13.getPosition(), 1):
            result_peg_13.nextPosition(1)
            result_peg_13.setValue(')')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_13);
        
        result_peg_14 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = [param1] + params
        result_peg_14.setValue(value)
        
        result_peg_1.addResult(result_peg_14);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_value_parameters, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_value_parameters, position, None)
    return None


def rule_parameters_rules(stream, position):
    if stream.hasResult(RULE_parameters_rules, position):
        return stream.result(RULE_parameters_rules, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        if '[' == stream.get(result_peg_2.getPosition(), 1):
            result_peg_2.nextPosition(1)
            result_peg_2.setValue('[')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'spaces'
        result_peg_3 = rule_spaces(stream, result_peg_3.getPosition())
        if result_peg_3 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_3);
        
        result_peg_4 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'word_or_at'
        result_peg_4 = rule_word_or_at(stream, result_peg_4.getPosition())
        if result_peg_4 == None:
            raise PegError
        param1 = result_peg_4.getValues()
        
        result_peg_1.addResult(result_peg_4);
        
        result_peg_5 = Result(result_peg_1.getPosition())
        
        try:
            while True:
                result_peg_6 = Result(result_peg_5.getPosition());
                result_peg_7 = Result(result_peg_6.getPosition())
                
                # print "Trying rule " + 'spaces'
                result_peg_7 = rule_spaces(stream, result_peg_7.getPosition())
                if result_peg_7 == None:
                    raise PegError
                
                result_peg_6.addResult(result_peg_7);
                
                result_peg_8 = Result(result_peg_6.getPosition())
                
                if ',' == stream.get(result_peg_8.getPosition(), 1):
                    result_peg_8.nextPosition(1)
                    result_peg_8.setValue(',')
                else:
                    raise PegError
                
                result_peg_6.addResult(result_peg_8);
                
                result_peg_9 = Result(result_peg_6.getPosition())
                
                # print "Trying rule " + 'spaces'
                result_peg_9 = rule_spaces(stream, result_peg_9.getPosition())
                if result_peg_9 == None:
                    raise PegError
                
                result_peg_6.addResult(result_peg_9);
                
                result_peg_10 = Result(result_peg_6.getPosition())
                
                # print "Trying rule " + 'word_or_at'
                result_peg_10 = rule_word_or_at(stream, result_peg_10.getPosition())
                if result_peg_10 == None:
                    raise PegError
                exp = result_peg_10.getValues()
                
                result_peg_6.addResult(result_peg_10);
                
                result_peg_11 = Result(result_peg_6.getPosition())
                
                value = None
                values = result_peg_6.getValues()
                value = exp
                result_peg_11.setValue(value)
                
                result_peg_6.addResult(result_peg_11);
                
                result_peg_6.setValue(result_peg_6.getLastValue())
                result_peg_5.addResult(result_peg_6);
        except PegError:
            pass
        params = result_peg_5.getValues()
        
        result_peg_1.addResult(result_peg_5);
        
        result_peg_12 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'spaces'
        result_peg_12 = rule_spaces(stream, result_peg_12.getPosition())
        if result_peg_12 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_12);
        
        result_peg_13 = Result(result_peg_1.getPosition())
        
        if ']' == stream.get(result_peg_13.getPosition(), 1):
            result_peg_13.nextPosition(1)
            result_peg_13.setValue(']')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_13);
        
        result_peg_14 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = [param1] + params
        result_peg_14.setValue(value)
        
        result_peg_1.addResult(result_peg_14);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_parameters_rules, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_parameters_rules, position, None)
    return None


def rule_parameters_values(stream, position):
    if stream.hasResult(RULE_parameters_values, position):
        return stream.result(RULE_parameters_values, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        if '(' == stream.get(result_peg_2.getPosition(), 1):
            result_peg_2.nextPosition(1)
            result_peg_2.setValue('(')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'spaces'
        result_peg_3 = rule_spaces(stream, result_peg_3.getPosition())
        if result_peg_3 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_3);
        
        result_peg_4 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'word_or_dollar'
        result_peg_4 = rule_word_or_dollar(stream, result_peg_4.getPosition())
        if result_peg_4 == None:
            raise PegError
        param1 = result_peg_4.getValues()
        
        result_peg_1.addResult(result_peg_4);
        
        result_peg_5 = Result(result_peg_1.getPosition())
        
        try:
            while True:
                result_peg_6 = Result(result_peg_5.getPosition());
                result_peg_7 = Result(result_peg_6.getPosition())
                
                # print "Trying rule " + 'spaces'
                result_peg_7 = rule_spaces(stream, result_peg_7.getPosition())
                if result_peg_7 == None:
                    raise PegError
                
                result_peg_6.addResult(result_peg_7);
                
                result_peg_8 = Result(result_peg_6.getPosition())
                
                if ',' == stream.get(result_peg_8.getPosition(), 1):
                    result_peg_8.nextPosition(1)
                    result_peg_8.setValue(',')
                else:
                    raise PegError
                
                result_peg_6.addResult(result_peg_8);
                
                result_peg_9 = Result(result_peg_6.getPosition())
                
                # print "Trying rule " + 'spaces'
                result_peg_9 = rule_spaces(stream, result_peg_9.getPosition())
                if result_peg_9 == None:
                    raise PegError
                
                result_peg_6.addResult(result_peg_9);
                
                result_peg_10 = Result(result_peg_6.getPosition())
                
                # print "Trying rule " + 'word_or_dollar'
                result_peg_10 = rule_word_or_dollar(stream, result_peg_10.getPosition())
                if result_peg_10 == None:
                    raise PegError
                exp = result_peg_10.getValues()
                
                result_peg_6.addResult(result_peg_10);
                
                result_peg_11 = Result(result_peg_6.getPosition())
                
                value = None
                values = result_peg_6.getValues()
                value = exp
                result_peg_11.setValue(value)
                
                result_peg_6.addResult(result_peg_11);
                
                result_peg_6.setValue(result_peg_6.getLastValue())
                result_peg_5.addResult(result_peg_6);
        except PegError:
            pass
        params = result_peg_5.getValues()
        
        result_peg_1.addResult(result_peg_5);
        
        result_peg_12 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'spaces'
        result_peg_12 = rule_spaces(stream, result_peg_12.getPosition())
        if result_peg_12 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_12);
        
        result_peg_13 = Result(result_peg_1.getPosition())
        
        if ')' == stream.get(result_peg_13.getPosition(), 1):
            result_peg_13.nextPosition(1)
            result_peg_13.setValue(')')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_13);
        
        result_peg_14 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = [param1] + params
        result_peg_14.setValue(value)
        
        result_peg_1.addResult(result_peg_14);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_parameters_values, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_parameters_values, position, None)
    return None


def rule_word_or_dollar(stream, position):
    if stream.hasResult(RULE_word_or_dollar, position):
        return stream.result(RULE_word_or_dollar, position)
    try:
        result_peg_1 = Result(position)
        # print "Trying rule " + 'word'
        result_peg_1 = rule_word(stream, result_peg_1.getPosition())
        if result_peg_1 == None:
            raise PegError
        stream.update(RULE_word_or_dollar, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    try:
        result_peg_2 = Result(position)
        # print "Trying rule " + 'dollar'
        result_peg_2 = rule_dollar(stream, result_peg_2.getPosition())
        if result_peg_2 == None:
            raise PegError
        stream.update(RULE_word_or_dollar, position, result_peg_2)
        return result_peg_2
    except PegError:
        pass
    stream.update(RULE_word_or_dollar, position, None)
    return None


def rule_word_or_at(stream, position):
    if stream.hasResult(RULE_word_or_at, position):
        return stream.result(RULE_word_or_at, position)
    try:
        result_peg_1 = Result(position)
        # print "Trying rule " + 'word'
        result_peg_1 = rule_word(stream, result_peg_1.getPosition())
        if result_peg_1 == None:
            raise PegError
        stream.update(RULE_word_or_at, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    try:
        result_peg_2 = Result(position)
        # print "Trying rule " + 'word_at'
        result_peg_2 = rule_word_at(stream, result_peg_2.getPosition())
        if result_peg_2 == None:
            raise PegError
        stream.update(RULE_word_or_at, position, result_peg_2)
        return result_peg_2
    except PegError:
        pass
    stream.update(RULE_word_or_at, position, None)
    return None


def rule_word_at(stream, position):
    if stream.hasResult(RULE_word_at, position):
        return stream.result(RULE_word_at, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        if '@' == stream.get(result_peg_2.getPosition(), 1):
            result_peg_2.nextPosition(1)
            result_peg_2.setValue('@')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'word'
        result_peg_3 = rule_word(stream, result_peg_3.getPosition())
        if result_peg_3 == None:
            raise PegError
        word = result_peg_3.getValues()
        
        result_peg_1.addResult(result_peg_3);
        
        result_peg_4 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = '@%s' % word
        result_peg_4.setValue(value)
        
        result_peg_1.addResult(result_peg_4);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_word_at, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_word_at, position, None)
    return None


def rule_dollar(stream, position):
    if stream.hasResult(RULE_dollar, position):
        return stream.result(RULE_dollar, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        if '$' == stream.get(result_peg_2.getPosition(), 1):
            result_peg_2.nextPosition(1)
            result_peg_2.setValue('$')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'number'
        result_peg_3 = rule_number(stream, result_peg_3.getPosition())
        if result_peg_3 == None:
            raise PegError
        number = result_peg_3.getValues()
        
        result_peg_1.addResult(result_peg_3);
        
        result_peg_4 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = "$%s" % number
        result_peg_4.setValue(value)
        
        result_peg_1.addResult(result_peg_4);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_dollar, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_dollar, position, None)
    return None


def rule_number(stream, position):
    if stream.hasResult(RULE_number, position):
        return stream.result(RULE_number, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        try:
            while True:
                result_peg_3 = Result(result_peg_2.getPosition());
                # print "Trying rule " + 'digit'
                result_peg_3 = rule_digit(stream, result_peg_3.getPosition())
                if result_peg_3 == None:
                    raise PegError
                result_peg_2.addResult(result_peg_3);
        except PegError:
            if result_peg_2.matches() == 0:
                raise PegError
                
        result_peg_1.addResult(result_peg_2);
        
        result_peg_4 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = ''.join(values[0])
        result_peg_4.setValue(value)
        
        result_peg_1.addResult(result_peg_4);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_number, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_number, position, None)
    return None


def rule_digit(stream, position):
    if stream.hasResult(RULE_digit, position):
        return stream.result(RULE_digit, position)
    try:
        result_peg_1 = Result(position)
        letter_peg_2 = stream.get(result_peg_1.getPosition())
        if letter_peg_2 in '0123456789':
            result_peg_1.nextPosition()
            result_peg_1.setValue(letter_peg_2)
        else:
            raise PegError
        stream.update(RULE_digit, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_digit, position, None)
    return None


def rule_hex_number(stream, position):
    if stream.hasResult(RULE_hex_number, position):
        return stream.result(RULE_hex_number, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        try:
            while True:
                result_peg_3 = Result(result_peg_2.getPosition());
                # print "Trying rule " + 'hex_digit'
                result_peg_3 = rule_hex_digit(stream, result_peg_3.getPosition())
                if result_peg_3 == None:
                    raise PegError
                result_peg_2.addResult(result_peg_3);
        except PegError:
            if result_peg_2.matches() == 0:
                raise PegError
                
        result_peg_1.addResult(result_peg_2);
        
        result_peg_4 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = ''.join(values[0])
        result_peg_4.setValue(value)
        
        result_peg_1.addResult(result_peg_4);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_hex_number, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_hex_number, position, None)
    return None


def rule_hex_digit(stream, position):
    if stream.hasResult(RULE_hex_digit, position):
        return stream.result(RULE_hex_digit, position)
    try:
        result_peg_1 = Result(position)
        letter_peg_2 = stream.get(result_peg_1.getPosition())
        if letter_peg_2 in '0123456789abcdefABCDEF':
            result_peg_1.nextPosition()
            result_peg_1.setValue(letter_peg_2)
        else:
            raise PegError
        stream.update(RULE_hex_digit, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_hex_digit, position, None)
    return None


def rule_start_symbol(stream, position):
    if stream.hasResult(RULE_start_symbol, position):
        return stream.result(RULE_start_symbol, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        if 'start-symbol:' == stream.get(result_peg_2.getPosition(), 13):
            result_peg_2.nextPosition(13)
            result_peg_2.setValue('start-symbol:')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        try:
            while True:
                result_peg_4 = Result(result_peg_3.getPosition());
                # print "Trying rule " + 'space'
                result_peg_4 = rule_space(stream, result_peg_4.getPosition())
                if result_peg_4 == None:
                    raise PegError
                result_peg_3.addResult(result_peg_4);
        except PegError:
            pass
                
        result_peg_1.addResult(result_peg_3);
        
        result_peg_5 = Result(result_peg_1.getPosition())
        
        # print "Trying rule " + 'word'
        result_peg_5 = rule_word(stream, result_peg_5.getPosition())
        if result_peg_5 == None:
            raise PegError
        
        result_peg_1.addResult(result_peg_5);
        
        result_peg_6 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = values[2]
        result_peg_6.setValue(value)
        
        result_peg_1.addResult(result_peg_6);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_start_symbol, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_start_symbol, position, None)
    return None


def rule_spaces(stream, position):
    if stream.hasResult(RULE_spaces, position):
        return stream.result(RULE_spaces, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        try:
            while True:
                result_peg_3 = Result(result_peg_2.getPosition());
                # print "Trying rule " + 'space'
                result_peg_3 = rule_space(stream, result_peg_3.getPosition())
                if result_peg_3 == None:
                    raise PegError
                result_peg_2.addResult(result_peg_3);
        except PegError:
            pass
                
        result_peg_1.addResult(result_peg_2);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_spaces, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_spaces, position, None)
    return None


def rule_space(stream, position):
    if stream.hasResult(RULE_space, position):
        return stream.result(RULE_space, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        if ' ' == stream.get(result_peg_2.getPosition(), 1):
            result_peg_2.nextPosition(1)
            result_peg_2.setValue(' ')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_space, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    try:
        result_peg_3 = Result(position)
        result_peg_4 = Result(result_peg_3.getPosition())
        
        if '\t' == stream.get(result_peg_4.getPosition(), 1):
            result_peg_4.nextPosition(1)
            result_peg_4.setValue('\t')
        else:
            raise PegError
        
        result_peg_3.addResult(result_peg_4);
        
        result_peg_3.setValue(result_peg_3.getLastValue())
        stream.update(RULE_space, position, result_peg_3)
        return result_peg_3
    except PegError:
        pass
    stream.update(RULE_space, position, None)
    return None


def rule_any_char(stream, position):
    if stream.hasResult(RULE_any_char, position):
        return stream.result(RULE_any_char, position)
    try:
        result_peg_1 = Result(position)
        letter_peg_2 = stream.get(result_peg_1.getPosition())
        if letter_peg_2 in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-':
            result_peg_1.nextPosition()
            result_peg_1.setValue(letter_peg_2)
        else:
            raise PegError
        stream.update(RULE_any_char, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_any_char, position, None)
    return None


def rule_any(stream, position):
    if stream.hasResult(RULE_any, position):
        return stream.result(RULE_any, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        if '.' == stream.get(result_peg_2.getPosition(), 1):
            result_peg_2.nextPosition(1)
            result_peg_2.setValue('.')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        value = None
        values = result_peg_1.getValues()
        value = peg.PatternAny()
        result_peg_3.setValue(value)
        
        result_peg_1.addResult(result_peg_3);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_any, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_any, position, None)
    return None


def rule_whitespace(stream, position):
    if stream.hasResult(RULE_whitespace, position):
        return stream.result(RULE_whitespace, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        try:
            while True:
                result_peg_3 = Result(result_peg_2.getPosition());
                save_peg_4 = result_peg_3.getPosition()
                
                result_peg_3 = Result(save_peg_4)
                letter_peg_5 = stream.get(result_peg_3.getPosition())
                if letter_peg_5 in ' \t\n':
                    result_peg_3.nextPosition()
                    result_peg_3.setValue(letter_peg_5)
                else:
                    
                    result_peg_3 = Result(save_peg_4)
                    # print "Trying rule " + 'comment'
                    result_peg_3 = rule_comment(stream, result_peg_3.getPosition())
                    if result_peg_3 == None:
                        raise PegError
                result_peg_2.addResult(result_peg_3);
        except PegError:
            pass
                
        result_peg_1.addResult(result_peg_2);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_whitespace, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_whitespace, position, None)
    return None


def rule_comment(stream, position):
    if stream.hasResult(RULE_comment, position):
        return stream.result(RULE_comment, position)
    try:
        result_peg_1 = Result(position)
        result_peg_2 = Result(result_peg_1.getPosition())
        
        if '#' == stream.get(result_peg_2.getPosition(), 1):
            result_peg_2.nextPosition(1)
            result_peg_2.setValue('#')
        else:
            raise PegError
        
        result_peg_1.addResult(result_peg_2);
        
        result_peg_3 = Result(result_peg_1.getPosition())
        
        try:
            while True:
                result_peg_4 = Result(result_peg_3.getPosition());
                result_peg_5 = Result(result_peg_4.getPosition())
                
                result_peg_6 = Result(result_peg_5.getPosition());
                try:
                    if '\n' == stream.get(result_peg_6.getPosition(), 1):
                        result_peg_6.nextPosition(1)
                        result_peg_6.setValue('\n')
                    else:
                        raise NotError
                    raise PegError
                except NotError:
                    result_peg_5.setValue(None)
                        
                result_peg_4.addResult(result_peg_5);
                
                result_peg_7 = Result(result_peg_4.getPosition())
                
                temp_peg_8 = stream.get(result_peg_7.getPosition())
                if temp_peg_8 != chr(0):
                    result_peg_7.setValue(temp_peg_8)
                    result_peg_7.nextPosition()
                else:
                    raise PegError
                
                result_peg_4.addResult(result_peg_7);
                
                result_peg_4.setValue(result_peg_4.getLastValue())
                result_peg_3.addResult(result_peg_4);
        except PegError:
            pass
                
        result_peg_1.addResult(result_peg_3);
        
        result_peg_1.setValue(result_peg_1.getLastValue())
        stream.update(RULE_comment, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_comment, position, None)
    return None


def rule_newlines_one(stream, position):
    if stream.hasResult(RULE_newlines_one, position):
        return stream.result(RULE_newlines_one, position)
    try:
        result_peg_1 = Result(position)
        try:
            while True:
                result_peg_2 = Result(result_peg_1.getPosition());
                if '\n' == stream.get(result_peg_2.getPosition(), 1):
                    result_peg_2.nextPosition(1)
                    result_peg_2.setValue('\n')
                else:
                    raise PegError
                result_peg_1.addResult(result_peg_2);
        except PegError:
            if result_peg_1.matches() == 0:
                raise PegError
        stream.update(RULE_newlines_one, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_newlines_one, position, None)
    return None


def rule_newlines(stream, position):
    if stream.hasResult(RULE_newlines, position):
        return stream.result(RULE_newlines, position)
    try:
        result_peg_1 = Result(position)
        try:
            while True:
                result_peg_2 = Result(result_peg_1.getPosition());
                if '\n' == stream.get(result_peg_2.getPosition(), 1):
                    result_peg_2.nextPosition(1)
                    result_peg_2.setValue('\n')
                else:
                    raise PegError
                result_peg_1.addResult(result_peg_2);
        except PegError:
            pass
        stream.update(RULE_newlines, position, result_peg_1)
        return result_peg_1
    except PegError:
        pass
    stream.update(RULE_newlines, position, None)
    return None


def doParse(stream):
    done = rule_start(stream, 0)
    if done == None:
        # print "Error parsing " + file
        raise Exception(stream.reportError())
    else:
        return done.getValues()

def parseFile(file):
    # print "Parsing " + file
    return doParse(Stream(filename = file))

def parseString(value):
    return doParse(Stream(input = value))

