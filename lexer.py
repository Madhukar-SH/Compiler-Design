from re import *

commentStart = compile('/\*')
commentEnd = compile('\*/')
singleComment = compile('//')
quotes = compile('".*"')
identifiers = compile("[a-zA-Z_][a-zA-Z_0-9]*")

keywords = ["auto", "double", "int", "struct", "break", "else", "long", "switch", "case", "enum", "register", "typedef", "char", "extern", "return", "union", "const", "float", "short", "unsigned", "continue", "for", "signed", "void", "default", "goto", "sizeof", "volatile", "do", "if", "static", "while"]

symbolTable = {}
print("Welcome to Lexer")

flag=False
'''
def generateToken(line):
    words = line.split()
    for i in words:
        if i in keywords:
            if i not in symbolTable:
                
        '''
def readComment(line):
    while(line):
        if(commentEnd.match(line)):
            return
        line = input().strip()
        
line=input().strip()

while(line):
    if(quotes.match(line)):
        print(line)
        line = input().strip()
        continue
        
    elif(commentStart.match(line)):
        readComment(line)
        
    elif(singleComment.match(line)):
        line=input().strip()
        continue
        
    else:
        print(line)
        
    line=input().strip()
   
print("Thank you!");
