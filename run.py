import sys
import os.path
import Tokenizer
import Parser

inputfile= sys.argv[1]
inputfile = inputfile.strip()
if os.path.isfile(inputfile)== False:
    print("File Not Found, Check Path");
    sys.exit()
size=len(inputfile)
if inputfile[size-5:size] != ".jack":
    print("Wrong Format")
else:
    inputname = inputfile.split('/')[-1]
    inputfolder = inputfile.rsplit('/', 1)[0]
    outputfile =  "T" + inputname.replace("jack", "xml")
    outputfile2 = inputname.replace("jack", "xml")
    Tokenizer.tokenize(inputfile, outputfile)
    Parser.parse(outputfile, outputfile2)