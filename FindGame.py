#!/usr/bin/python

import sys
import os
import re

import cgitb
cgitb.enable()

class PrettyView:
    
    data=[]
    
    def __init__(self, data):
        tmp=data.split(',')
        for line in tmp:
            PrettyView.data.append(line.strip())
    
    def summary(self):
        outcome=self.data[6]
        oppOutcome="W"
        if(outcome=="W"):
            oppOutcome="L"
        return self.data[21] + " "+self.data[0]+": "+self.data[7]+" "+self.data[4]+"("+outcome+") vs "+self.data[8]+" "+self.data[5]+"("+oppOutcome+")"
    
    def full(self):
        print ', '.join(map(str,self.data))

def main(args):
    
    games=args[1]
    team=args[2]
    month=args[3]
    day=args[4]
    year=args[5]
    
    result=getMatchingLines(games,team, month, day, year)
    
    for line in result:
        view=PrettyView(line)
        print view.summary()

def getMatchingLines(filename, team, month, day, year):
    f=open(filename)
    matches=[]
    date=month+" "+day+","+year
    for line in f:
        if team in line and date in line:
            matches.append(line)
    return matches

if (len(sys.argv) <= 5):
    print "invalid arguments: <games files> <team> <month> <day> <year>"
else:
    main(sys.argv)