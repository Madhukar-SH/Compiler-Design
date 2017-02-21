#!/usr/bin/env python3

from re import *
import sys

class lexer:
    def __init__(self, file_name):
        self.file_name = file_name
        self.fp = open(self.file_name,'r')
        self.tokens = []
        self.symbolTable = {"auto":(1,"Keyword"), "double":(2,"Keyword"),
                            "int":(3,"Keyword"), "struct":(4,"Keyword"),
                            "break":(5,"Keyword"), "else":(6,"Keyword"),
                            "long":(7,"Keyword"), "switch":(8,"Keyword"),
                            "case":(9,"Keyword"), "enum":(10,"Keyword"),
                            "register":(11,"Keyword"),
                            "typedef":(12,"Keyword"), "char":(13,"Keyword"),
                            "extern":(14,"Keyword"), "return":(15,"Keyword"),
                            "union":(16,"Keyword"), "const":(17,"Keyword"),
                            "float":(18,"Keyword"), "short":(19,"Keyword"),
                            "unsigned":(20,"Keyword"),
                            "continue":(21,"Keyword"),"for":(22,"Keyword"),
                            "signed":(23,"Keyword"), "void":(24,"Keyword"),
                            "default":(25,"Keyword"), "goto":(26,"Keyword"),
                            "sizeof":(27,"Keyword"),
                            "volatile":(28,"Keyword"), "do":(29,"Keyword"),
                            "if":(30,"Keyword"), "static":(31,"Keyword"),
                            "while":(32,"Keyword"), "+":(33,"MathOp"),
                            "-":(34,"MathOp"),"*":(35,"MathOp"),
                            "/":(36,"MathOp"),"%":(37,"MathOp"),
                            "++":(38,"UnaryOp"),"--":(39,"UnaryOp"),
                            "==":(40,"RelOp"),"!=":(41,"RelOp"),
                            ">":(42,"RelOp"),"<":(43,"RelOp"),
                            ">=":(44,"RelOp"),"<=":(45,"RelOp"),
                            "=":(46,"AssignOp"),"+=":(47,"AssignOp"),
                            "-=":(48,"AssignOp"),"*=":(49,"AssignOp"),
                            "/=":(50,"AssignOp"),"%=":(51,"AssignOp"),
                            "(":(52,"RoundLpar"),")":(53,"RoundRpar"),
                            "[":(54,"SquareLpar"),"]":(55,"SquareRpar"),
                            "{":(56,"FlowerLpar"),"}":(57,"FlowerRpar"),
                            ";":(58,"Semicolon"),",":(59,"CommaOp"),
                            "main":(60,"Keyword"), "#include":(61, "Keyword"),
                            "stdio.h":(62, "Library"),
                            "math.h":(63, "Library"),
                            "string.h":(64, "Library"),
                            "stdlib.h":(65,"Library")}
        self.op = ["+","-","*","/","%","++","--","==","!=",">","<",">=","<=",
                   "=","+=","-=","*=","/=","%=","(",")","[","]","{","}",";",
                   ","," "]
        self.commentStart = compile('/\*')
        self.commentEnd = compile('\*/')
        self.singleComment = compile('//')
        self.quotes = compile('[".*"][\'.*\']')
        self.identifiers = compile("[a-zA-Z_][a-zA-Z_0-9]*")
        self.numbers = compile("[0-9]+[.0-9]?[0-9]*")
        self.flag = False
        self.symcount = 61

    def start(self):
        line = self.checkEmpty(self.fp.readline().strip())
            
        while(line):
            if(self.quotes.match(line)):
                #print(line)
                self.updateTable(line)
                line = self.checkEmpty(self.fp.readline().strip())
                continue
                
            elif(self.commentStart.search(line)):
                line=line.split("/*")
                self.updateTable(line[0])
                self.readComment(line[1])
                
            elif(self.singleComment.search(line)):
                line=line.split("//")
                self.updateTable(line[0])
                line = self.checkEmpty(self.fp.readline().strip())
                continue
                
            else:
                #print(line)
                #pass
                self.updateTable(line)
                
            line = self.checkEmpty(self.fp.readline().strip())

    def readComment(self, line):
        while(line):
            if(self.commentEnd.search(line)):
                line=line.split("*/")
                self.updateTable(line[1])
                return
            line = self.checkEmpty(self.fp.readline().strip())
            
    def checkEmpty(self, line):
        while(True):
            if(not line):
                line = self.fp.readline().strip()
            else:
                return line
          
    def symCheck(self, word):
        if(word in self.symbolTable):
            x = self.symbolTable[word]
            #print("Token: ",word,"\t",x[0],"\t",x[1])
            self.tokens.append((word, x[0], x[1]))
        else:
            self.symcount += 1
            if(self.quotes.match(word)):
                self.symbolTable[word]=(self.symcount,"String")
                #print("Token:",word,"\t",self.symcount,"\t","String")
                self.tokens.append((word, self.symcount, "String"))
                
            elif(self.identifiers.match(word)):
                self.symbolTable[word]=(self.symcount, "Identifier")
                #print("Token: ",word,"\t",self.symcount,"\t","Identifier")
                self.tokens.append((word, self.symcount, "Identifier"))
                
            elif(self.numbers.match(word)):
                self.symbolTable[word]=(self.symcount,"Number")
                #print("Token: ",word,"\t",self.symcount,"\t","Number")
                self.tokens.append((word, self.symcount, "Number"))
            else:
                self.symbolTable[word]=(self.symcount, "String")
                #print("Token: ",word,"\t",self.symcount,"\t","String")
                self.tokens.append((word, self.symcount, "String"))
                          
    def updateTable(self, line):
        start=0
        sstring=False
        dstring=False
        
        for i in range(len(line)):
                end = i
                if(line[i] in ['"',"'"]):
                    if(line[i]=='"'):
                        if(not sstring and not dstring):
                            dstring=True
                            start=end
                        elif(dstring and not sstring):
                            dstring=False
                            self.symCheck(line[start:end+1])
                            start=end+1
                            
                    elif(line[i]=="'"):
                        if(not sstring and not dstring):
                            sstring=True
                            start=end
                        elif(sstring and not dstring):
                            sstring=False
                            self.symCheck(line[start:end+1])
                            start=end+1
                            
                elif(not sstring and not dstring and line[i] in self.op):
                    if(not line[i]==" "):
                        self.symCheck(line[start:end+1])
                    start=end+1
                            
                elif(not sstring and not dstring and isinstance(line[i],(int,str))):
                    if(i<len(line)-1):
                        if(line[i+1] in self.op):
                            self.symCheck(line[start:end+1])
                            start=end+1
                        else:
                            continue
                    elif(i==len(line)-1):
                        self.symCheck(line[start:end+1])

    def get_symbol_table(self):
        return self.symbolTable
    
    def get_tokens(self):
        return self.tokens
if __name__ == "__main__":
    if(len(sys.argv)<2):
        print("Error: No input file")
    else:
        sys.exit(lexer(sys.argv[1]).start())
