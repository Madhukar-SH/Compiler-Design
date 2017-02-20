#!/usr/bin/env python3

from re import *
import sys

commentStart = compile('/\*')
commentEnd = compile('\*/')
singleComment = compile('//')

quotes = compile('[".*"][\'.*\']')
identifiers = compile("[a-zA-Z_][a-zA-Z_0-9]*")
numbers = compile("[0-9]+[.0-9]?[0-9]*")
'''
keywords = ["auto", "double", "int", "struct", "break", "else", "long", "switch", "case", "enum", "register", "typedef", "char", "extern", "return", "union", "const", "float", "short", "unsigned", "continue", "for", "signed", "void", "default", "goto", "sizeof", "volatile", "do", "if", "static", "while"]

mathop = ["+","-","*","/","%","++","--"]
relop = ["==","!=",">","<",">=","<="]
assignop = ["=","+=","-=","*=","/=","%="]'''

op = ["+","-","*","/","%","++","--","==","!=",">","<",">=","<=","=","+=","-=","*=","/=","%=","(",")","[","]","{","}",";",","," "]


symbolTable = {"auto":(1,"Keyword"), "double":(2,"Keyword"), "int":(3,"Keyword"), "struct":(4,"Keyword"), "break":(5,"Keyword"), "else":(6,"Keyword"), "long":(7,"Keyword"), "switch":(8,"Keyword"), "case":(9,"Keyword"), "enum":(10,"Keyword"), "register":(11,"Keyword"), "typedef":(12,"Keyword"), "char":(13,"Keyword"), "extern":(14,"Keyword"), "return":(15,"Keyword"), "union":(16,"Keyword"), "const":(17,"Keyword"), "float":(18,"Keyword"), "short":(19,"Keyword"), "unsigned":(20,"Keyword"), "continue":(21,"Keyword"), "for":(22,"Keyword"), "signed":(23,"Keyword"), "void":(24,"Keyword"), "default":(25,"Keyword"), "goto":(26,"Keyword"), "sizeof":(27,"Keyword"), "volatile":(28,"Keyword"), "do":(29,"Keyword"), "if":(30,"Keyword"), "static":(31,"Keyword"), "while":(32,"Keyword"),"+":(33,"MathOp"),"-":(34,"MathOp"),"*":(35,"MathOp"),"/":(36,"MathOp"),"%":(37,"MathOp"),"++":(38,"MathOp"),"--":(39,"MathOp"),"==":(40,"RelOp"),"!=":(41,"RelOp"),">":(42,"RelOp"),"<":(43,"RelOp"),">=":(44,"RelOp"),"<=":(45,"RelOp"),"=":(46,"AssignOp"),"+=":(47,"AssignOp"),"-=":(48,"AssignOp"),"*=":(49,"AssignOp"),"/=":(50,"AssignOp"),"%=":(51,"AssignOp"),"(":(52,"RoundLpar"),")":(53,"RoundRpar"),"[":(54,"SquareLpar"),"]":(55,"SquareRpar"),"{":(56,"FlowerLpar"),"}":(57,"FlowerRpar"),";":(58,"Semicolon"),",":(59,"CommaOp")}

flag = False

def readComment(line):
    while(line):
        if(commentEnd.match(line)):
            return
        line = checkEmpty(fp.readline().strip())
            
def checkEmpty(line):
    while(True):
        if(not line):
            line = fp.readline().strip()
        else:
            return line

def symCheck(word):
    stcount = 59
    if(word in symbolTable):
        x = symbolTable[word]
        print(word,x[0],x[1])
    else:
        stcount += 1
        if(quotes.match(word)):
            symbolTable[word]=(stcount,"String")
            print(word,stcount,"String")
            
        elif(identifiers.match(word)):
            symbolTable[word]=(stcount, "Identifeir")
            print(word,stcount,"Identifeir")
        
        elif(numbers.match(word)):
            symbolTable[word]=(stcount,"Number")
            print(word,stcount,"Number")
        
        else:
            symbolTable[word]=(stcount, "String")
            print(word,stcount,"String")
         
                          
def updateTable(line):
    start=0
    sstring=0
    dstring=0
    
    for i in range(len(line)):
            end = i
            if(line[i] in ['"',"'"]):
                if(line[i]=='"'):
                    if(not sstring and not dstring):
                        dstring=1
                        start=end
                    elif(dstring and not sstring):
                        dstring=0
                        symCheck(line[start:end+1])
                        start=end+1
                        
                elif(line[i]=="'"):
                    if(not sstring and not dstring):
                        sstring=1
                        start=end
                    elif(sstring and not dstring):
                        sstring=0
                        symCheck(line[start:end+1])
                        start=end+1
                        
            elif(not sstring and not dstring and line[i] in op):
                if(not line[i]==" "):
                    symCheck(line[start:end+1])
                start=end+1
                        
            elif(not sstring and not dstring and isinstance(line[i],(int,str))):
                if(i<len(line)-1):
                    if(line[i+1] in op):
                        symCheck(line[start:end+1])
                        start=end+1
                    else:
                        continue
                elif(i==len(line)-1):
                    symCheck(line[start:end+1])
                        
if(not sys.argv[1]):
    print("Error: No input file")
    
else:
    fp = open(sys.argv[1],'r')
    print("Welcome to Lexer")            
    line = checkEmpty(fp.readline().strip())
            
    while(line):
        if(quotes.match(line)):
            print(line)
            line = checkEmpty(fp.readline().strip())
            continue
            
        elif(commentStart.match(line)):
            readComment(line)
            
        elif(singleComment.match(line)):
            line = checkEmpty(fp.readline().strip())
            continue
            
        else:
            #print(line)
            #pass
            updateTable(line)
            
        line = checkEmpty(fp.readline().strip())
        
    print("Thank you!");
