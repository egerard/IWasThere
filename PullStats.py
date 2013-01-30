#!/usr/bin/python

import urllib2 # for html gets
from BeautifulSoup import BeautifulSoup          # For processing HTML
import sys

def getData(url):
    req=urllib2.Request(url)
    response=urllib2.urlopen(req)
    return response.read()

def findGames(url,year,file):
    data = getData(url)
    soup = BeautifulSoup(data)
    tbodies = soup.findAll('tbody')
    
    if len(tbodies) < 1:
        return
    
    tbody = tbodies[0]
    
    team = getFullTeamName(soup)
    
    rows = tbody.findAll('tr')
    i = 0
    for row in rows:
        data = formatRow(row,year)
        if data != None:
            i = i+1
            s=', '.join(map(str,data))
            s=s+","+team
            file.write("%s\n" % s)
    return i

def getFullTeamName(soup):
    h1s=soup.findAll('h1')
    team=""
    if len(h1s) >= 1:
        h1=h1s[0]
        team=h1.text
    return team

def getTeams(data):
    soup = BeautifulSoup(data)
    franchises = soup.findAll('td')
    teams = []
    for team in  franchises:
        if team.has_key('class'):
            if team['class']==' franchise_names':
                teams.append(team.find('a')['href'])
    return teams

def getBoxScore(base, bs):
    url=base+bs
    data=getData(url)
    print data


def formatRow(row, year):
    tds = row.findAll('td')
    
    if len(tds) < 15:
        return
    
    rk=encode(tds[0])
    gm=encode(tds[1])
    date=encodeTag(tds[2], 'a')
    bs=encodeTagAttr(tds[3], 'a', 'href')
    tm=encode(tds[4])
    opp=encodeTag(tds[6], 'a')
    wl=encode(tds[7])
    r=encode(tds[8])
    ra=encode(tds[9])
    inn=tds[10]['csk']
    record=encode(tds[11])
    gb=encode(tds[12])
    win=encode(tds[13])
    loss=encode(tds[14])
    save=encode(tds[15])
    time=encode(tds[16])
    dn=encode(tds[17])
    att=encode(tds[18])
    strk=encode(tds[19])
    
    try:
        n = int(gm)
        data = [year, rk, gm, bs, tm, opp, wl, r, ra, inn, record, gb, win, loss, save, time, dn, att, strk, date]
        getBoxScore('http://www.baseball-reference.com',bs)
        #        print ', '.join(map(str,data))
        return data
    except ValueError:
        return "none"


def encode(td):
    return td.text

def encodeTag(td, tag):
    t = td.find(tag)
    if t==None:
        return ""
    else:
        return t.text

def encodeTagAttr(td, tag, attr):
    t = td.find(tag)
    if  t==None:
        return ""
    else:
        return t[attr]

def main(filename):
    f = open(filename, 'w')
    year = 2012
    
    teamsUrl="http://www.baseball-reference.com/teams/"
    teamsdata=getData(teamsUrl)
    teams=getTeams(teamsdata);
    
    while (year > 1970):
        for team in teams:
            filename=str(year)+"-schedule-scores.shtml"
            url="http://www.baseball-reference.com"+team+"/"+filename
            i = findGames(url, year,f)
            print "stored "+str(i)+" games for "+str(year)+" "+team
        year = year - 1

if (len(sys.argv) <= 1):
    print "invalid arguments: <output-file-name>"
else:
    main(sys.argv[1])


