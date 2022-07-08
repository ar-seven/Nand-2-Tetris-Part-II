import re
import sys

keywords = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else',            'while', 'return']
symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~', '&lt;', '&gt;', '&amp;' , '&quot;'] 
ops = [ '+', '-', '*', '/', '&lt;', '&gt;', '=', '&amp;' , '&quot;' , '|', '[' , '(']
statements = [ 'if', 'while' , 'let', 'do' , 'return' ]
type = [ 'int' , 'boolean', 'char' ]

global file_descriptor
global xml_file 

def put_space(numspaces, newline) :
    space =""
    for i in range(0, numspaces):
        space += " "
    newline += space
    return newline
    
def is_identifier(token) :
    if token in keywords :
        ret = 0
    elif token in symbols :
        ret = 0
    elif token.isdigit() :
        ret = 0
    elif token == "\"" :
        ret = 0
    else :
        ret = 1
    return ret

def get_next_token() :
    line = file_descriptor.readline()
    token =""
    words = line.split(' ')
    while len(words) <= 1 and line != "" :
        line = file_descriptor.readline()
        words = line.split(' ')
    if line != "" and len(words) == 3:
        token = words[1]
    elif len(words) > 3 :
        token =' '.join(words[1:len(words)-1])
    return token
    
def parse(outputfile, outputfile2) :
    global file_descriptor
    file_descriptor=open(outputfile, "r")
    global xml_file 
    xml_file =open(outputfile2, 'w')
    compile_class()
    
def compile_class():
    newline = ""
    numspaces = 0
    token = get_next_token()
    if token == "class" :
        newline += "<class>\n"
        numspaces +=2
        newline = put_space(numspaces, newline)
        newline += "<keyword> class </keyword>\n"
        token = get_next_token()
        if is_identifier(token) == 1 :
            newline = put_space(numspaces, newline)
            newline += "<identifier> " + token + " </identifier>\n"
            token = get_next_token()
            if token == "{" :
                newline = put_space(numspaces, newline)
                newline += "<symbol> { </symbol>\n"
                xml_file.write(newline)
                token = get_next_token()
                while token == "static" or token == "field" :
                    compile_classVarDec(token, numspaces)
                    token = get_next_token()
                while token == "constructor" or token == "function" or token == "method" : 
                    compile_subroutineDec(token,numspaces)
                    token = get_next_token()
                if token == "}" :
                    newline = ""
                    newline = put_space(numspaces, newline)
                    newline += "<symbol> } </symbol>\n"
                    numspaces -= 2
                    newline = put_space(numspaces, newline)
                    newline += "</class>\n"
                    xml_file.write(newline)
                else:
                    print("\n Syntax Error : Expected class variable declaration or method declaration")
                    sys.exit()
            else:
                print("\n Syntax Error : Missing { in class declaration ")
                sys.exit()
        else:
            print("\n Syntax Error : Missing class name in class declaration ")
            sys.exit()
    else:
        print("\n Syntax Error : No class in file ")
        sys.exit()
    

def compile_classVarDec(token, numspaces):
    newline = ""
    newline = put_space(numspaces, newline)
    newline += "<classVarDec>\n"
    numspaces += 2
    if token == "field" or token =="static":
        newline = put_space(numspaces, newline)
        newline += "<keyword> " + token + " </keyword>\n"
        token=get_next_token()
        if token in type :
            newline = put_space(numspaces, newline)
            newline += "<keyword> " + token + " </keyword>\n"
        elif is_identifier(token) == 1 :
            newline = put_space(numspaces, newline)
            newline += "<identifier> " + token + " </identifier>\n"
        else:
            print("\n Syntax Error : Variable Type missing ")
            sys.exit()    
        token=get_next_token()
        count = 0
        while is_identifier(token) == 1 :
            count += 1
            newline = put_space(numspaces, newline)
            newline += "<identifier> " + token + " </identifier>\n"
            token=get_next_token()

            if token == "," :
                newline = put_space(numspaces, newline)
                newline += "<symbol> , </symbol>\n"
                token=get_next_token()
            elif token == ";" :
                newline = put_space(numspaces, newline)
                newline += "<symbol> ; </symbol>\n"
                break
            else:
                print("\n Syntax Error : ; or , missing at the end of varDec ")
                sys.exit()
        if count == 0 :
            print("\n Syntax Error : Missing varName for Field variable")
            sys.exit()
        if token == ';' :
            numspaces -= 2
            newline = put_space(numspaces, newline)
            newline += "</classVarDec>\n"

    xml_file.write(newline) 
    
def compile_subroutineDec(token,numspaces):
    newline = ""
    newline = put_space(numspaces, newline)
    newline += "<subroutineDec>\n"
    numspaces += 2
    if token == "constructor" or token == "function" or token == "method":
        newline = put_space(numspaces, newline)
        newline += "<keyword> " + token + " </keyword>\n"
        token = get_next_token()
        if token in type or token == "void":
            newline = put_space(numspaces, newline)
            newline += "<keyword> " + token + " </keyword>\n"
        elif is_identifier(token) == 1 :
            newline = put_space(numspaces, newline)
            newline += "<identifier> " + token + " </identifier>\n"
        else:
            print("\n Syntax Error : Function Type missing ")
            sys.exit()
        token=get_next_token()
        if is_identifier(token) == 1 : 
            newline = put_space(numspaces, newline)
            newline += "<identifier> " + token + " </identifier>\n"
        else:
            print("\n Syntax Error : Missing Function Name ")
            sys.exit()
        token = get_next_token()
        if token == "(" :
            newline = put_space(numspaces, newline)
            newline += "<symbol> ( </symbol>\n"
        else:
            print("\n Syntax Error : Missing ( for function declaration")
            sys.exit()
        token = get_next_token()
        newline = put_space(numspaces, newline)
        newline += "<parameterList>\n"
        numspaces +=2
        
        if token in type :
            newline = put_space(numspaces, newline)
            newline += "<keyword> " + token + " </keyword>\n"
            token = get_next_token()

            while is_identifier(token) == 1 :
                newline = put_space(numspaces, newline)
                newline += "<identifier> " + token + " </identifier>\n"
                token=get_next_token()

                if token == "," :
                    newline = put_space(numspaces, newline)
                    newline += "<symbol> , </symbol>\n"
                    token=get_next_token()

                    if token in type or token == "void":
                       newline = put_space(numspaces, newline) 
                       newline += "<keyword> " + token + " </keyword>\n"
                    else:
                        print("\n Syntax Error : Missing type in parameter list ")
                        sys.exit()
                    token=get_next_token()
                elif token == ")" :
                    break
                else:
                    print("\n Syntax Error : ; or , missing at the end of varDec ")
                    sys.exit()
        elif token != ')' :
            print("\n Syntax Error : Missing variable in parameter list ")
            sys.exit()

        if token == ')' :
            numspaces -= 2
            newline = put_space(numspaces, newline)
            newline += "</parameterList>\n"
            newline = put_space(numspaces, newline)
            newline += "<symbol> ) </symbol>\n"
            
        else :
            print(newline)
            print("\n Syntax Error : Missing ) at the end of parameter list ")
            sys.exit()
            
        newline = put_space(numspaces, newline)    
        newline += "<subroutineBody>\n"
        numspaces +=2 
        token = get_next_token()
        if token == "{" :
            newline = put_space(numspaces, newline)
            newline += "<symbol> { </symbol>\n"
        else:
            print("\n Syntax Error : Missing { at the start of subroutine body ")
            sys.exit()
        xml_file.write(newline)
        token = get_next_token()
        while token in statements or token == "var":
            if token == "var" :
                compile_varstatement(numspaces, token)
                token = get_next_token()
            else :
                token = compile_statements(token, numspaces)
            newline = "" 
            if token == "}" :
                break;
        if token == "}" :

            newline = put_space(numspaces, newline)
            newline += "<symbol> } </symbol>\n"
            numspaces -= 2
            newline = put_space(numspaces, newline)    
            newline += "</subroutineBody>\n"
        else:
            print(newline)
            print("\n Syntax Error : Missing } at the end of subroutine body ")
            sys.exit()  
            
    numspaces -= 2        
    newline = put_space(numspaces, newline)    
    newline += "</subroutineDec>\n" 
    xml_file.write(newline)
            
def compile_statements(token, numspaces) :
    newline = ""
    newline = put_space(numspaces, newline)
    newline += "<statements>\n"
    xml_file.write(newline)
    numspaces += 2
    while 1: 
        if token == "while" :
            compile_whilestatement(numspaces, token)
            token = get_next_token()
        elif token == "if" :
            token = compile_ifstatement(numspaces, token)
            
        elif token == "let" :
            compile_letstatement(numspaces, token)
            token = get_next_token()
        elif token == "do" :
            compile_dostatement(numspaces, token)
            token = get_next_token()
        elif token == "return" :
            compile_returnStatement(numspaces, token)
            token = get_next_token()
        else: 
            break; 
        
    newline = ""
    numspaces -= 2
    newline = put_space(numspaces, newline)      
    newline += "</statements>\n"  
    xml_file.write(newline)
    return token
    
def compile_expression(numspaces, token) :
    newline = ""
    prev_token = token
    token = get_next_token()
    if token == ")"  or token == ";" or token == "]":
        return token,newline
    newline = put_space(numspaces, newline)
    newline += "<expression>\n"
    numspaces += 2 
        
    while 1 :
        if len(token.split(' ')) > 1 :
            newline = put_space(numspaces, newline)
            newline += "<term>\n"
            numspaces += 2
            newline = put_space(numspaces, newline)
            newline += "<stringConstant> " + token + " </stringConstant>\n"
            numspaces -=2
            newline = put_space(numspaces, newline)
            newline += "</term>\n"
            prev_token = token
            token = get_next_token()
        if token == "(" :
            newline = put_space(numspaces, newline)
            newline += "<term>\n"
            numspaces += 2
            newline = put_space(numspaces, newline)
            newline += "<symbol> " + token + " </symbol>\n"
            xml_file.write(newline)
            newline = "" 
            token, newline = compile_expression(numspaces,token)
            xml_file.write(newline)
            newline ="" 
            if token == ")" :
                newline = put_space(numspaces, newline)
                newline += "<symbol> " + token + " </symbol>\n"
            else : 
                print("\n Syntax Error : Missing ) in expression after unary op")
                sys.exit()
            numspaces -=2
            newline = put_space(numspaces, newline)
            newline += "</term>\n"
            prev_token = token
            token = get_next_token()
        elif is_identifier(token) == 1 :
            newline = put_space(numspaces, newline)
            newline += "<term>\n"
            numspaces += 2
            newline = put_space(numspaces, newline)
            newline += "<identifier> " + token + " </identifier>\n"
            prev_token = token
            token = get_next_token()
            if token == "." :
                newline = put_space(numspaces, newline)
                newline += "<symbol> " + token + " </symbol>\n"
                token = get_next_token()
                if is_identifier(token) == 1 :
                    newline = put_space(numspaces, newline)
                    newline += "<identifier> " + token + " </identifier>\n"
                    prev_token = token
                    token = get_next_token()
                else :
                    print("\n Syntax Error : . should be followed by an identifier")
                    sys.exit()
                    
            if token == "(" :
                newline = put_space(numspaces, newline)
                newline += "<symbol> ( </symbol>\n"
                xml_file.write(newline)
                token = compile_expressionlist(numspaces)
                newline =""
                if token == ')' :
                    newline = put_space(numspaces, newline)
                    newline += "<symbol> ) </symbol>\n"
                else : 
                    print("\n Syntax Error : Missing ) in expressionlist")
                    sys.exit()
            elif token == "[":
                newline = put_space(numspaces, newline)
                newline += "<symbol> " + token + " </symbol>\n"
                prev_token = token
                token = get_next_token()
                if is_identifier(token) == 1 :
                    newline = put_space(numspaces, newline)
                    newline += "<expression>\n"
                    numspaces +=2
                    newline = put_space(numspaces, newline)
                    newline += "<term>\n"
                    numspaces += 2
                    newline = put_space(numspaces, newline)
                    newline += "<identifier> " + token + " </identifier>\n"
                    numspaces -=2
                    newline = put_space(numspaces, newline)
                    newline += "</term>\n"
                    numspaces -=2
                    newline = put_space(numspaces, newline)
                    newline += "</expression>\n"
                    prev_token = token
                    token = get_next_token()
                elif token.isdigit() :
                    newline = put_space(numspaces, newline)
                    newline += "<expression>\n"
                    numspaces +=2
                    newline = put_space(numspaces, newline)
                    newline += "<term>\n"
                    numspaces += 2
                    newline = put_space(numspaces, newline)
                    newline += "<integerConstant> " + token + " </integerConstant>\n"
                    numspaces -=2
                    newline = put_space(numspaces, newline)
                    newline += "</term>\n"
                    numspaces -=2
                    newline = put_space(numspaces, newline)
                    newline += "</expression>\n"
                    prev_token = token
                    token = get_next_token()
                    
                else : 
                    print("\n Syntax Error : An identifier must follow [")
                    sys.exit()
                if token == ']' :
                    newline = put_space(numspaces, newline)
                    newline += "<symbol> ] </symbol>\n"
                else : 
                    print("\n Syntax Error : Missing ] in array")
                    sys.exit()
                    
            numspaces -=2
            newline = put_space(numspaces, newline)
            newline += "</term>\n"
        elif token.isdigit() :
            newline = put_space(numspaces, newline)
            newline += "<term>\n"
            numspaces += 2
            newline = put_space(numspaces, newline)
            newline += "<integerConstant> " + token + " </integerConstant>\n"
            numspaces -=2
            newline = put_space(numspaces, newline)
            newline += "</term>\n"
            prev_token = token
            token = get_next_token()
        elif token == "~" or (token == '-' and prev_token in ops):
            print(prev_token)
            newline = put_space(numspaces, newline)
            newline += "<term>\n"
            numspaces += 2
            newline = put_space(numspaces, newline)
            newline += "<symbol> " + token + " </symbol>\n"
            prev_token = token
            token = get_next_token() 
            if is_identifier(token) == 1: 
                newline = put_space(numspaces, newline)
                newline += "<term>\n"
                numspaces += 2
                newline = put_space(numspaces, newline)
                newline += "<identifier> " + token + " </identifier>\n"
                numspaces -=2
                newline = put_space(numspaces, newline)
                newline += "</term>\n"
            elif token.isdigit() :
                newline = put_space(numspaces, newline)
                newline += "<term>\n"
                numspaces += 2
                newline = put_space(numspaces, newline)
                newline += "<integerConstant> " + token + " </integerConstant>\n"
                numspaces -=2
                newline = put_space(numspaces, newline)
                newline += "</term>\n"
            elif token == "(" :
                newline = put_space(numspaces, newline)
                newline += "<term>\n"
                numspaces += 2
                newline = put_space(numspaces, newline)
                newline += "<symbol> " + token + " </symbol>\n"
                xml_file.write(newline)
                newline = "" 
                token, newline = compile_expression(numspaces,token)
                xml_file.write(newline)
                newline = ""
                if token == ")" :
                    newline = put_space(numspaces, newline)
                    newline += "<symbol> " + token + " </symbol>\n"
                else : 
                    print("\n Syntax Error : Missing ) in expression after unary op")
                    sys.exit()
                numspaces -=2
                newline = put_space(numspaces, newline)
                newline += "</term>\n"
            else :
                print("\n Syntax Error : Unary op should be followed by an identifier or an integer")
                sys.exit()
            numspaces -=2
            newline = put_space(numspaces, newline)
            newline += "</term>\n"
            prev_token = token
            token = get_next_token()
        elif token == "true" or token =="false" :
            newline = put_space(numspaces, newline)
            newline += "<term>\n"
            numspaces += 2
            newline = put_space(numspaces, newline)
            newline += "<keyword> " + token + " </keyword>\n"
            numspaces -=2
            newline = put_space(numspaces, newline)
            newline += "</term>\n"
            prev_token = token
            token = get_next_token()
        elif token == "this" or token =="null":
            newline = put_space(numspaces, newline)
            newline += "<term>\n"
            numspaces += 2
            newline = put_space(numspaces, newline)
            newline += "<keyword> " + token + " </keyword>\n"
            numspaces -=2
            newline = put_space(numspaces, newline)
            newline += "</term>\n"
            prev_token = token
            token = get_next_token()
        elif token in ops :
            newline = put_space(numspaces, newline)
            newline += "<symbol> " + token + " </symbol>\n"
            prev_token = token
            token = get_next_token()
        elif token == "(" :
            newline = put_space(numspaces, newline)
            newline += "<term>\n"
            numspaces += 2
            newline = put_space(numspaces, newline)
            newline += "<symbol> " + token + " </symbol>\n"
            prev_token = token
            token = get_next_token()
            if token in ops : 
                newline = put_space(numspaces, newline)
                newline += "<expression>\n"
                numspaces +=2
                newline = put_space(numspaces, newline)
                newline += "<term>\n"
                numspaces += 2
                newline = put_space(numspaces, newline)
                newline += "<symbol> " + token + " </symbol>\n"
                prev_token = token
                token = get_next_token()
                if is_identifier(token) == 1 :
                    newline = put_space(numspaces, newline)
                    newline += "<term>\n"
                    numspaces += 2
                    newline = put_space(numspaces, newline)
                    newline += "<identifier> " + token + " </identifier>\n"
                    numspaces -=2
                    newline = put_space(numspaces, newline)
                    newline += "</term>\n"
                elif token.isdigit() :
                    newline = put_space(numspaces, newline)
                    newline += "<term>\n"
                    numspaces += 2
                    newline = put_space(numspaces, newline)
                    newline += "<integerConstant> " + token + " </integerConstant>\n"
                    numspaces -=2
                    newline = put_space(numspaces, newline)
                    newline += "</term>\n"
                else : 
                    print("\n Syntax Error : Unary Operator to be followed by a digit or identifier")
                    sys.exit()
                numspaces -=2
                newline = put_space(numspaces, newline)
                newline += "</term>\n"
                
            elif token == "(" :
                newline = put_space(numspaces, newline)
                newline += "<expression>\n"
                numspaces +=2
                newline = put_space(numspaces, newline)
                newline += "<term>\n"
                numspaces += 2
                newline = put_space(numspaces, newline)
                newline += "<symbol> " + token + " </symbol>\n"
                xml_file.write(newline)
                newline =""
                token, newline = compile_expression(numspaces,token)
                
                if token == ")" :
                    newline = put_space(numspaces, newline)
                    newline += "<symbol> " + token + " </symbol>\n"
                    numspaces -=2
                    newline = put_space(numspaces, newline)
                    newline += "</term>\n" 
                    xml_file.write(newline)
                    newline = ""
                    token = get_next_token()
                    continue 
            numspaces -=2
            newline = put_space(numspaces, newline)
            newline += "</expression>\n"
            prev_token = token
            token = get_next_token()
            if token == ")" :
                newline = put_space(numspaces, newline)
                newline += "<symbol> " + token + " </symbol>\n"
                numspaces -=2
                newline = put_space(numspaces, newline)
                newline += "</term>\n"
                break;
            else : 
                print("\n Syntax Error : Missing ) for unary expression")
                sys.exit()
        elif token == ")"  or token == ";" or token == "]" or ",":
            break
        else:
            print("\n Syntax Error : Missing term in expression")
            sys.exit()

    if token == ")" or token == ";" or token == "]" or token == ",":
        numspaces -=2
        newline = put_space(numspaces, newline)
        newline += "</expression>\n"
    else :
        print(token)
        print(newline)
        print("\n Syntax Error : Expression syntax error")
        sys.exit()
    return token,newline   

def compile_whilestatement(numspaces, token) :
    newline = ""
    newline = put_space(numspaces, newline)
    newline += "<whileStatement>\n"
    numspaces += 2
    newline = put_space(numspaces, newline)
    newline += "<keyword> " + token + " </keyword>\n"
    token = get_next_token()
    
    if token == "(" :
        newline = put_space(numspaces, newline)
        newline += "<symbol> ( </symbol>\n"
    else :
        print("\n Syntax Error : Missing ( in function declaration")
        sys.exit()
    xml_file.write(newline)
    token,newline = compile_expression(numspaces,token)
    
    if token == ")" :
        newline = put_space(numspaces, newline)
        newline += "<symbol> ) </symbol>\n" 
    else:
        print("\n Syntax Error : Missing ) in function declaration")
        sys.exit()
    token = get_next_token()
    if token == "{" :
        newline = put_space(numspaces, newline)
        newline += "<symbol> { </symbol>\n"
    else:
        print("\n Syntax Error : Missing { at the start of loop body")
        sys.exit()
    xml_file.write(newline)
    token = get_next_token()
    while token in statements or token == "var":
        if token == "var" :
            compile_varstatement(numspaces, token)
            token = get_next_token()
        else :
            token = compile_statements(token, numspaces)
        newline =""
    if token == "}" :
        newline = put_space(numspaces, newline)
        newline += "<symbol> } </symbol>\n"
        numspaces -= 2
        newline = put_space(numspaces, newline)    
        newline += "</whileStatement>\n"
    else:
        print("\n Syntax Error : Missing } at the end of loop body ")
        sys.exit()
    xml_file.write(newline)

    
def compile_ifstatement(numspaces, token) :
    newline = ""
    newline = put_space(numspaces, newline)
    newline += "<ifStatement>\n"
    numspaces += 2
    newline = put_space(numspaces, newline)
    newline += "<keyword> " + token + " </keyword>\n"
    token = get_next_token()
    
    if token == "(" :
        newline = put_space(numspaces, newline)
        newline += "<symbol> ( </symbol>\n"
    else :
        print("\n Syntax Error : Missing ( in if declaration")
        sys.exit()
    xml_file.write(newline)
    token, newline = compile_expression(numspaces, token)
    xml_file.write(newline)
    newline =""
    if token == ")" :
        newline = put_space(numspaces, newline)
        newline += "<symbol> ) </symbol>\n" 
    else:
        print("\n Syntax Error : Missing ) in if declaration")
        sys.exit()
    xml_file.write(newline)
    newline = ""
    token = get_next_token()
    
    if token in ops :
        newline = put_space(numspaces, newline)
        newline += "<symbol> ) </symbol>\n" 
        token = get_next_token()
    
    if token == "(" :
        newline = put_space(numspaces, newline)
        newline += "<symbol> ( </symbol>\n"
        xml_file.write(newline)
     
        
    if token == "{" :
        print (newline)
        newline = put_space(numspaces, newline)
        newline += "<symbol> { </symbol>\n"
    else:
        print("\n Syntax Error : Missing { at the start of if body")
        sys.exit()
    xml_file.write(newline)
    token = get_next_token()
    while token in statements or token == "var":
        if token == "var" :
            compile_varstatement(numspaces, token)
            token = get_next_token()
        else :
            token = compile_statements(token, numspaces)
        newline = ""
    if token == "}"  :
        newline = put_space(numspaces, newline)
        newline += "<symbol> } </symbol>\n"
        xml_file.write(newline)
        newline =""
        token = get_next_token()
        if token == "else" :
            compile_elsestatement(numspaces, token)
            token = get_next_token()
            newline =""
        numspaces -= 2
        newline = put_space(numspaces, newline)    
        newline += "</ifStatement>\n"
    else:
        print("\n Syntax Error : Missing } at the end of if body ")
        sys.exit()
    xml_file.write(newline)
    return token

def compile_elsestatement(numspaces, token) :
    newline = ""
    newline = put_space(numspaces, newline)
    newline += "<keyword> else </keyword>\n"
    token = get_next_token()
    if token == "{" :
        newline = put_space(numspaces, newline)
        newline += "<symbol> { </symbol>\n"
    else :
        print("\n Syntax Error : Missing { at the start of else body")
        sys.exit()
    
    xml_file.write(newline)
    token = get_next_token()
    while token in statements or token == "var":
        if token == "var" :
            compile_varstatement(numspaces, token)
            token = get_next_token()
        else :
            token = compile_statements(token, numspaces)
        newline = ""
    if token == "}"  :
        newline = put_space(numspaces, newline)
        newline += "<symbol> } </symbol>\n"
        
    xml_file.write(newline)    
    
def compile_letstatement(numspaces, token):
    newline = ""
    newline = put_space(numspaces, newline)
    newline += "<letStatement>\n"
    numspaces += 2
    newline = put_space(numspaces, newline)
    newline += "<keyword> " + token + " </keyword>\n"
    token = get_next_token()
    if is_identifier(token) == 1 :
        newline = put_space(numspaces, newline)
        newline += "<identifier> " + token + " </identifier>\n"
    else: 
        print("\n Syntax Error : Missing varName in let ")
        sys.exit()
    
    token = get_next_token()
    if token == "[" :
        newline = put_space(numspaces, newline)
        newline += "<symbol> " + token + " </symbol>\n"
        xml_file.write(newline)
        token, newline = compile_expression(numspaces, token)
        if token == "]" :
            newline = put_space(numspaces, newline)
            newline += "<symbol> " + token + " </symbol>\n"
            token = get_next_token()
        else :
            print("\n Syntax Error : Missing ] in let ")
            sys.exit()   
    
    if token == "=":
        newline = put_space(numspaces, newline)
        newline += "<symbol> = </symbol>\n" 
    else:
        print("\n Syntax Error : Missing = in let ")
        sys.exit()
    xml_file.write(newline)
    token, newline = compile_expression(numspaces,token)
    
    if token == ")" or token == "]":
        token = get_next_token()
    
    if token == ";" :
        newline = put_space(numspaces, newline)
        newline += "<symbol> ; </symbol>\n" 
    else:
        print("\n Syntax Error : Missing ; at the end of let")
        sys.exit()
        
    numspaces -= 2
    newline = put_space(numspaces, newline)
    newline += "</letStatement>\n"
    xml_file.write(newline)
    
    
def compile_varstatement(numspaces, token) :
    newline = ""
    newline = put_space(numspaces, newline)
    newline += "<varDec>\n"
    numspaces += 2
    newline = put_space(numspaces, newline)
    newline += "<keyword> " + token + " </keyword>\n"
    
    token = get_next_token()
    if token in type : 
        newline = put_space(numspaces, newline)
        newline += "<keyword> " + token + " </keyword>\n"
    elif is_identifier(token) == 1:
        newline = put_space(numspaces, newline)
        newline += "<identifier> " + token + " </identifier>\n"
    else: 
        print(token)
        print(newline)
        print("\n Syntax Error : Missing type for local variable")
        sys.exit()
    token = get_next_token()
    count = 0
    while is_identifier(token) == 1 :
        count += 1
        newline = put_space(numspaces, newline)
        newline += "<identifier> " + token + " </identifier>\n"
        token=get_next_token()
         
        if token == "," :
            newline = put_space(numspaces, newline)
            newline += "<symbol> , </symbol>\n"
            token=get_next_token()
        elif token == ";" :
            newline = put_space(numspaces, newline)
            newline += "<symbol> ; </symbol>\n"
            break
        else:
            print("\n Syntax Error : ; or , missing at the end of varDec ")
            sys.exit()
    if count == 0 :
        print("\n Syntax Error : Missing varName for local variable")
        sys.exit()
        
    if token == ';' :
        numspaces -= 2
        newline = put_space(numspaces, newline)
        newline += "</varDec>\n"
    
    xml_file.write(newline)
        
def compile_returnStatement(numspaces, token) :
    newline = ""
    newline = put_space(numspaces, newline)
    newline += "<returnStatement>\n"
    numspaces += 2
    newline = put_space(numspaces, newline)
    newline += "<keyword> " + token + " </keyword>\n"
    xml_file.write(newline)
    token,newline = compile_expression(numspaces,token)
    
    if token == ";" :
        newline = put_space(numspaces, newline)
        newline += "<symbol> ; </symbol>\n" 
    else:
        print("\n Syntax Error : Missing ; at the end of let")
        sys.exit()
        
    numspaces -= 2
    newline = put_space(numspaces, newline)
    newline += "</returnStatement>\n"
    xml_file.write(newline)
    
def compile_dostatement(numspaces, token) :
    newline = ""
    newline = put_space(numspaces, newline)
    newline += "<doStatement>\n"
    numspaces += 2
    newline = put_space(numspaces, newline)
    newline += "<keyword> " + token + " </keyword>\n"
    
    token = get_next_token()
    if is_identifier(token) == 1 :
        newline = put_space(numspaces, newline)
        newline += "<identifier> " + token + " </identifier>\n"
    else :
        print("\n Syntax Error : Missing classname for subroutine call")
        sys.exit()
    
    token = get_next_token()
    if token == "." :
        newline = put_space(numspaces, newline)
        newline += "<symbol> . </symbol>\n"
        token = get_next_token()
        if is_identifier(token) == 1: 
            newline = put_space(numspaces, newline)
            newline += "<identifier> " + token + " </identifier>\n"
            token = get_next_token()
        else:
            print("\n Syntax Error : Missing subroutine name for subroutine call")
            sys.exit()
                  
    if token == "(" :
        newline = put_space(numspaces, newline)
        newline += "<symbol> ( </symbol>\n"
        xml_file.write(newline)
        token = compile_expressionlist(numspaces)
        newline =""
    if token == ')' :
        newline = put_space(numspaces, newline)
        newline += "<symbol> ) </symbol>\n"
        
    else : 
        print("\n Syntax Error : Missing ) in expressionlist")
        sys.exit()
    
    token = get_next_token()
    if token ==';' :
        newline = put_space(numspaces, newline)
        newline += "<symbol> ; </symbol>\n"
        numspaces -= 2
        newline = put_space(numspaces, newline)
        newline += "</doStatement>\n"
    else :
        print("\n Syntax Error : Missing ; at the end of do statement")
        sys.exit()
    
    xml_file.write(newline)
        
        
def compile_expressionlist(numspaces) :
    newline = ""
    newline = put_space(numspaces, newline)
    newline += "<expressionList>\n"
    numspaces += 2
    token= ""
    xml_file.write(newline)
    
    while token != ")" : 
        newline =""
        token,newline = compile_expression(numspaces,token)
        if token == "," :
            newline = put_space(numspaces, newline)
            newline += "<symbol> , </symbol>\n"
        elif token == ")" :
            break
        else : 
            print("\n Syntax Error : Token should be , or )")
            sys.exit()
        xml_file.write(newline)
    
    if token == ')' :
        numspaces -= 2
        newline = put_space(numspaces, newline)
        newline += "</expressionList>\n"
    
    xml_file.write(newline)
    return token
    
    
      
    
    
    
    
            
        
        
            
       
        
        
        
            
    
    
        
        
            
            
            
    
        
                
        
        

    
        
    