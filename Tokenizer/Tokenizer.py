import re
def tokenize(inputfile, outputfile) :
    keywords = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else',            'while', 'return']
    symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~'] 
    file_descriptor=open(inputfile, "r")
    with open(outputfile, 'w') as xml_file:
        newline = ""
        newline += "<tokens>\n"
        xml_file.write(newline)
        for line in file_descriptor:
            newline = ""
            if line[0] == " ":
                line=line.strip()
                line, sep, tail = line.partition('//')
                line=line.strip()
            line=line.strip()
            size=len(line)
            i = 0
            if (line[:2] != "//") and (line[:2] != "/*") and (line[:1] !="*") and (line != '\n') and (line[size-2:size] !="*/"):
                words = re.split('(\W)|\+|\-|\*|\/|\||\&|\<|\>|\=|\~|\,|\;|\.|\s|\(|\)|\{|\}|\[|\]|\"',  line)                
                numwords = len(words) 
                while i < numwords:
                    if words[i] != ' ' and words[i]:
                        if words[i] in keywords :
                            newline += "<keyword> " + str(words[i]) + " </keyword>\n"
                        elif words[i] in symbols :
                            if words[i] == "<" :
                               newline += "<symbol> " + "&lt;" + " </symbol>\n" 
                            elif words[i] == ">" :
                               newline += "<symbol> " + "&gt;" + " </symbol>\n" 
                            elif words[i] == "&" :
                               newline += "<symbol> " + "&amp;" + " </symbol>\n" 
                            else :
                               newline += "<symbol> " + str(words[i]) + " </symbol>\n"
                        elif words[i].isdigit() :
                            newline += "<integerConstant> " + str(words[i]) + " </integerConstant>\n"
                        elif words[i] == "\"" :
                            newline += "<stringConstant> "
                            i += 1
                            pos = i
                            while (words[pos] != "\""):
                                newline += words[pos]
                                pos += 1
                            newline += " </stringConstant>\n" 
                            i = pos 
                            i += 1
                        else :
                            newline += "<identifier> " + str(words[i]) + " </identifier>\n"
                    i += 1 
                xml_file.write(newline)
        xml_file.write("</tokens>\n")
    xml_file.close()
    file_descriptor.close()

inputfile=input("Enter the name of the file to be tokenized: ")

outputfile=inputfile.split(".")[0]+".xml"
tokenize(inputfile, outputfile)                
                
                    
                    
                
                