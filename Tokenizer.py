import re
import sys

def tokenize(inputfile, outputfile) :
    keywords = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean',
                'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else','while', 'return']
    symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ';',
               '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']
    file_descriptor = open(inputfile, "r")#file_descriptor is a file object which has lines as strings

    with open(outputfile, 'w') as xml_file:
        #initialize the xml file
        newline = ""
        newline += "<tokens>\n"
        xml_file.write(newline)

        #tokenize the file
        for line in file_descriptor:
            newline = ""
            if line[0] == " ":#if the line starts with a space, remove it
                line = line.strip()#remove the right and left space
                line, sep, tail = line.partition('//')#remove the comment
                #line has abstracted line of code
                #sep has //
                #tail has the comment
                line = line.strip()
            line = line.strip()
            #line has abstracted line of code  
            size = len(line)
            i = 0
            if (line[:2] != "//") and (line[:2] != "/*") and (line[:1] != "*") and (line != '\n') and (line[size-2:size] != "*/"):#if the line is not a comment or a comment is not closed yet or the line is empty
                words = re.split(
                    '(\W)|\+|\-|\*|\/|\||\&|\<|\>|\=|\~|\,|\;|\.|\s|\(|\)|\{|\}|\[|\]|\"',  line)
                    #\W (upper case W) matches any non-word character.
                    #\s -- (lowercase s) matches a single whitespace character
                #we have 
                numwords = len(words)
                while i < numwords:
                    if words[i] != ' ' and words[i]:
                        #handling keywords
                        if words[i] in keywords: newline += "<keyword> " + str(words[i]) + " </keyword>\n"
                        #handling symbols
                        elif words[i] in symbols:
                            if words[i] == "<":
                                newline += "<symbol> " + "&lt;" + " </symbol>\n"
                            elif words[i] == ">":
                                newline += "<symbol> " + "&gt;" + " </symbol>\n"
                            elif words[i] == "&":
                                newline += "<symbol> " + "&amp;" + " </symbol>\n"
                            else:
                                newline += "<symbol> " + str(words[i]) + " </symbol>\n"
                        #handling integer constants
                        elif words[i].isdigit():
                            newline += "<integerConstant> " + str(words[i]) + " </integerConstant>\n"
                        #handling string constants
                        elif words[i] == "\"":#if the word is a string constant
                            newline += "<stringConstant> "
                            i += 1
                            pos = i
                            while (words[pos] != "\""):#while the word is not a string constant
                                newline += words[pos] #['let', ' ', 'c', '=', '', '"', 'hello', ' ', 'world', '"', '']
                                pos += 1
                            newline += " </stringConstant>\n"
                            i = pos #at ending quotes
                            i += 1 #skipping empty
                        #handling identifiers
                        else:
                            newline += "<identifier> " + \
                                str(words[i]) + " </identifier>\n"
                    i += 1
                xml_file.write(newline)#write the line to the xml file
        xml_file.write("</tokens>\n")
    xml_file.close()
    file_descriptor.close()
                
                
                    
                    
                
                