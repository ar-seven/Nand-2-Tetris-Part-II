import sys
import os.path
import Tokenizer
import Parser

choice=sys.argv[1]

if choice=="-f":
    inputfile=sys.argv[2]
    if os.path.isfile(inputfile):
        size=len(inputfile)
        if inputfile[size-5:size] != ".jack":
            print("Wrong Format")
        else:
            print("Tokenizing & Parsing "+inputfile)
            inputname = inputfile.split('/')[-1]
            inputfolder = inputfile.rsplit('/', 1)[0]
            outputfile =  "T" + inputname.replace("jack", "xml")
            outputfile2 = inputname.replace("jack", "xml")
            Tokenizer.tokenize(inputfile, outputfile)
            Parser.parse(outputfile, outputfile2)
            os.remove(outputfile)
        
    else:
        print("File not found")
        sys.exit()

elif choice=="-d":
    input_directory= sys.argv[2]#"input directory"
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
else:
    print("Wrong Choice")
    sys.exit()


