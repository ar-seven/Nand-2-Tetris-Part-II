import sys
import os.path
import Tokenizer
import Parser

input_directory= sys.argv[1]#"input directory"
input_directory = input_directory.strip()#remove whitespace
if os.path.isdir(input_directory)== False:
    print("Directory Not Found, Check Path");
    sys.exit()

files=os.listdir(input_directory)#get list of files in directory
for i in files:
    if i[-5:] == ".jack":#if file is a .jack file
        inputfile=input_directory+"/"+i#get file name
        inputfile = inputfile.strip()
        print("Tokenizing & Parsing "+inputfile)
        inputname = inputfile.split('/')[-1]
        outputfile =  input_directory+"/T" + inputname.replace("jack", "xml")#get output file name(tokenized)
        outputfile2 = input_directory+"/"+ inputname.replace("jack", "xml")#get output file name(parsed)
        Tokenizer.tokenize(inputfile, outputfile)#tokenize file
        Parser.parse(outputfile, outputfile2)#parse file
        os.remove(outputfile)#remove tokenized file



