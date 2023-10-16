import time
import requests

from bs4 import BeautifulSoup

class Player():

    def __init__(self,name):
        self.name = name
        self.min = 0
        self.pd = 0
        self.oPD = 0
        self.dPD = 0
        self.teammates = {}
        self.opponents = {}
        self.net = 0
        self.newNet = 0
        self.offNet = 0
        self.defNet = 0

globalStatD = {}


def getRequestContentPBP(url,filename):
    url = "https://www.basketball-reference.com/boxscores/pbp/"+url
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.content
    else:
        print("Failed to retrieve content. Status code:", response.status_code)

    soup = BeautifulSoup(html_content, 'html.parser')

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(str(soup))

def getRequestContentRoster(url,filename):
    url = "https://www.basketball-reference.com/boxscores/"+url
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.content
    else:
        print("Failed to retrieve content. Status code:", response.status_code)

    soup = BeautifulSoup(html_content, 'html.parser')

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(str(soup))

def printfile(fileName):
    num = 0
    try:
        # Open the file in read mode with the correct encoding
        with open(fileName, 'r', encoding='utf-8') as file:
            num = 0
            for line in file:
                try:
                    print(num, line,end="")
                except UnicodeEncodeError:
                    print(f"Line {num}: Line not printable")
                num += 1
    except UnicodeDecodeError as e:
        print(f"An error occurred while decoding the file: {e}")
    except IOError as e:
        print(f"An error occurred while reading the file: {e}")

def processGame(filename,pD):
    wFile = open("s2.txt","w")

    start = 0
    prevTime = 0
    pList = {}
    team1 = pD[0]
    team2 = pD[1]
    #print(pD)
    #print()
    lineNum = -1
    startTime = 0
    score = 0
    offScore = 0
    defScore = 0
    lastSubScore = 0
    lastSubOff = 0
    lastSubDef = 0
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            lineNum += 1
            if lineNum == 1230:
                #print("here")
                pass
            if '<div class="section_heading"><span class="section_anchor" data-label="Team and League Schedules" data-no-inpage="1" id="inner_nav_bottom_link"></span><h2>Team and League Schedules</h2></div>' in line:
                #printGlob(pD)
                break
            if '<th aria-label="Time" class="center" data-stat="Time">Time</th>' in line:
                start = 1
                pList = getStarters(filename,pD,lineNum)
                #pList = {"speigma01":1,"clarkia01":1,"ezelife01":1,"barbole01":1,"rushbr01":1,"jonesda02":0,"willima01":0,"mozgoti01":0,"fryech01":0,"jonesja02":0}
                #print(pList)
                startTime = -1
            if start == 1 and line != '</tr>\n' and line != '<tr>\n':
                isThere5Players = getTeamSum(pList,pD)
                if len(pList) != 10:
                    #print("not 10 players at line",lineNum)
                    pass

                if line.startswith("<td>") and line[4].isnumeric():
                    timeLine = line.strip("<td>").strip("</td>\n")
                    wFile.write(timeLine+"\n") 
                    if startTime == -1:
                        startTime = intTime(timeLine)
                    prevTime = intTime(timeLine)
                elif "enters" in line:
                    s = line.split('center">')[1].split("<")[0]

                    if getTeamSum(pList,pD) != 5:
                        #print("not 5 players for team 1 at line",lineNum)
                        pass
                    #print(line)
                    s = s.split('-')
                    time = startTime - prevTime
                    startTime = prevTime

                    newScore = int(s[0])-int(s[1])
                    newScoreOff = int(s[0])
                    newScoreDef = int(s[1])

                    #print(s[0]+'-'+s[1])

                    pd = newScore - lastSubScore
                    offPD = newScoreOff - lastSubOff
                    defPD = newScoreDef - lastSubDef

                    #print("oldScore:",score,"newScore:",newScore,"pd:",pd,time)
                    score = newScore
                    offScore = newScoreOff
                    defScore = newScoreDef


                    lastSubScore = newScore
                    lastSubOff = newScoreOff
                    lastSubDef = newScoreDef


                    getDataPoint(pD,pList,pd,time)
                    for p in pList:
                        if p not in globalStatD:
                            globalStatD[p] = Player(p)
                        globalStatD[p].min += time
                        if pD[p] == 0:
                        
                            globalStatD[p].pd += pd
                            globalStatD[p].oPD += offPD
                            globalStatD[p].dPD += defPD

                        else:
                        
                            globalStatD[p].pd -= pd
                            globalStatD[p].oPD += defPD
                            globalStatD[p].dPD += offPD


                        for p2 in pList:
                            if p != p2:
                                if pD[p] == pD[p2]:
                                    if p2 not in globalStatD[p].teammates:
                                        globalStatD[p].teammates[p2] = time
                                    else:
                                        globalStatD[p].teammates[p2] += time
                                else:
                                    if p2 not in globalStatD[p].opponents:
                                        globalStatD[p].opponents[p2] = time
                                    else:
                                        globalStatD[p].opponents[p2] += time
                        #getSumGlob(pD)

                    #printGlob(pD)

                    pVar = line.split('<a href="/players/')

                    pVar = pVar[1:]
                    
                    for i in range(len(pVar)):
                        pVar[i] = pVar[i].split(">")[0][2:-6]
                    #print("subs",pVar)
                    ins = pVar[0]
                    out = pVar[1]

                    del pList[out]
                    pList[ins] = pD[ins]
                    
                    score = newScore
                    offScore = newScoreOff
                    defScore = newScoreDef
                
                    

                elif ("center'>" in line or 'center">' in line) and "End of" not in line:
                    #print(line)
                    a = line.split('center">')
                    b = a[1]
                    c = b.split('<')
                    d = c[0]
                    #print(d)
                    s = d.split('-')


                    newScore = int(s[0])-int(s[1])
                    newScoreOff = int(s[0])
                    newScoreDef = int(s[1])


                    score = newScore
                    offScore = newScoreOff
                    defScore = newScoreDef
                    



                    wFile.write("SUBSTITUIONNNNNNNNNNNNNNNN\n")
                elif 'End of' in line:
                    #print("end of")
                    #print(score)
                    #print(line)
                    #print(startTime)
                    #newScore = int(s[0])-int(s[1])
                    #print(s[0]+'-'+s[1])

                    pd = score - lastSubScore
                    offPD = offScore - lastSubOff
                    defPD = defScore - lastSubDef

                    
                    #print(pd)
                    lastSubScore = newScore
                    lastSubOff = newScoreOff
                    lastSubDef = newScoreDef

                    getDataPoint(pD,pList,pd,startTime)

                    for p in pList:
                        if p not in globalStatD:
                            globalStatD[p] = Player(p)
                        globalStatD[p].min += startTime
                        if pD[p] == 0:
          
                            globalStatD[p].pd += pd
                            globalStatD[p].oPD += offPD
                            globalStatD[p].dPD += defPD
                        else:
                        
                            globalStatD[p].pd -= pd
                            globalStatD[p].oPD += defPD
                            globalStatD[p].dPD += offPD
                        for p2 in pList:
                            if p != p2:
                                if pD[p] == pD[p2]:
                                    if p2 not in globalStatD[p].teammates:
                                        globalStatD[p].teammates[p2] = startTime
                                    else:
                                        globalStatD[p].teammates[p2] += startTime
                                else:
                                    if p2 not in globalStatD[p].opponents:
                                        globalStatD[p].opponents[p2] = startTime
                                    else:
                                        globalStatD[p].opponents[p2] += startTime
                    #printGlob(pD)
                    score = newScore
                    offScore = newScoreOff
                    defScore = newScoreDef

                    pass
        

def processRoster(filename):
    pD = {}
    wFile = open("1111.txt","w")
    start = 0
    with open(filename, 'r', encoding='utf-8') as file:
        start = 0
        prevTeam = ""
        team = [""]
        tc = -1
        for line in file:
            if '<!-- global.nonempty_tables_num: 3, table_count: 3 -->' in line:
                return pD
                break
            if '<div class="table_wrapper" id="all_box-' in line:
                start = 1
            if start == 1:
                if 'div_box-' in line:
                    test = line.split("div_box-")[1][:3]
                    if line.split("div_box-")[1][:3] != team[-1]:
                        team.append(line.split("div_box-")[1][:3])
                        prevTeam = test
                        tc+=1
    
                        pD[tc] = prevTeam
                    wFile.write(test)
                    # print(team)
                if 'data-append-csv="' in line:
                    p = line.split('data-append-csv="')[1].split('"')[0]
                    if p not in pD:
                        pD[p] = tc
                    wFile.write(p+"\n")
                       # wFile.write(line)

def getStarters(filename,pD,lineNum):
    notStarters = {}
    wFile = open("starters.txt","w")
    onCourt = {}
    num = 0
    start = 0
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            num += 1
            if num == 246:
                #print("here")
                pass
            if start == 1 and line != '</tr>\n' and line != '<tr>\n':
                pVar = line.split('<a href="/players/')
                if len(pVar) == 1:
                    pVar = []
                else:
                    pVar = pVar[1:]

                for i in range(len(pVar)):
                    pVar[i] = pVar[i].split(">")[0][2:-6]

                #do something add to oncourt
                #enter game and not in on court = add to not starter
                # enter game and on court = dont add to start
                # leave game add to on court
               
                

                if len(pVar) != 0:
                    
                    if "enters" in line:
                        ##print("SUBSTITUIONNNNNNNNNNNNNNNN  ",end="")
                        if pVar[0] not in onCourt:
                            notStarters[pVar[0]] = 1
                        if pVar[1] not in notStarters:
                            onCourt[pVar[1]] = pD[pVar[1]]
                        #print(onCourt)
                    else:
                        for player in pVar:
                            if player not in notStarters:
                                onCourt[player] = pD[player]
                            #print(onCourt)

                    if (len(onCourt) == 10):
                        # print(onCourt)
                        return onCourt
                

                    pass
            if num == lineNum:
                start = 1
            #print(onCourt)
           
def intTime(s):
    s = s.split(":")
    return int(s[0])*60+float(s[1])

def getSumGlob(pD):
    team1Score = 0
    team2Score = 0
    for p in globalStatD:
        if pD[p] == 0:
            team1Score += globalStatD[p].pd
    print("team1 up by",team1Score)

def printGlob(pD):
    team1Score = 0
    team2Score = 0
    for p in globalStatD:
        if p in pD:
            if pD[p] == 0:
                team1Score += globalStatD[p].pd
            else:
                team2Score += globalStatD[p].pd
        print(p,globalStatD[p].min,globalStatD[p].pd)
    print("team1 up by",team1Score/5)

def getTeamSum(pList,pD):
    num = 0
    for p in pList:
        if pD[p] == 0:
            num += 1
    return num


def series(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            if line == "\n":
                continue
            url = line.strip("\n")
            if url in gamesDoneDict:
                #print("in already")
                continue
            pbpFile = "pbp.txt"
            roster = "roster.txt"
            saveFile = "save.txt"
            gamesDone.write(url+"\n")
            
            print(url)
            getRequestContentPBP(url,pbpFile)
            getRequestContentRoster(url,roster)

            pD = processRoster(roster)

            #printfile(filename)
            processGame(pbpFile,pD)

            time.sleep(5)

        for p in globalStatD:
            globalStatD[p].net = globalStatD[p].pd/(globalStatD[p].min/48/60)
            globalStatD[p].net = globalStatD[p].pd/(globalStatD[p].min/48/60)


        for i in range(1):
            updateValues()
            print("\n\n\n\n")

        


def getDataPoint(pD,pList,pd,startTime):
    pString = ""
    t = ""
    if startTime != 0:
        for p in pList:
            if pD[p] == 0:
                t = "1"
            else:
                t = "-1"
            pString += str(p)+":"+t+","
        pString += str(pd/(startTime/60)*48)+","+str(startTime)+"\n"
        saveFile.write(pString)
    
    


def updateValues():

    for p in globalStatD:
        #print("Player:",p,"Minutes:",round(globalStatD[p].min),"Net Rating:",round(globalStatD[p].pd),globalStatD[p].teammates,globalStatD[p].opponents)
        tPM = 0
        tMin = 0
        oPM = 0
        oMin = 0
        for t in globalStatD[p].teammates:
            tMin += globalStatD[p].teammates[t]
            tPM += globalStatD[t].net*globalStatD[p].teammates[t]
        for t in globalStatD[p].opponents:
            oMin += globalStatD[p].opponents[t]
            oPM += globalStatD[t].net*globalStatD[p].opponents[t]

        netrating = globalStatD[p].net
        tm = tPM/tMin/2#*4/5/2
        o = oPM/oMin/2#*5/5
        globalStatD[p].newNet = globalStatD[p].net-tm+o


        #print("Player:",p,"Minutes:",round(globalStatD[p].min),"+/-:",round(netrating,1),"Teamates:",round(tm,1),"Opps:",round(o,1),"SRS",round(globalStatD[p].newNet))#,round(globalStatD[p].oPD/(globalStatD[p].min/48/60),1),round(globalStatD[p].dPD/(globalStatD[p].min/48/60),1))#,globalStatD[p].teammates,globalStatD[p].opponents)
        print("Player:",p,"Minutes:",round(globalStatD[p].min//60),"+/-:",globalStatD[p].pd)#,round(globalStatD[p].oPD/(globalStatD[p].min/48/60),1),round(globalStatD[p].dPD/(globalStatD[p].min/48/60),1))#,globalStatD[p].teammates,globalStatD[p].opponents)


    for p in globalStatD:
        globalStatD[p].net = globalStatD[p].newNet

    
def getDoneGames():
    file = open("gamesDone.txt","r")
    d = set()
    for line in file:
        line = line.strip("\n")
        d.add(line)
    print(d)
    file.close()
    return d




gamesDoneDict = getDoneGames()
gamesDone = open("gamesDone.txt","a")
saveFile = open("saveFile.txt","a")
series("games.txt")

# {0: 'CLE', 'jamesle01': 0, 'irvinky01': 0, 'smithjr01': 0, 'thomptr01': 0, 'loveke01': 0, 'jefferi01': 0, 'shumpim01': 0, 'willima01': 0, 'dellama01': 0, 'fryech01': 0, 'jonesda02': 0, 'jonesja02': 0, 'mozgoti01': 0, 1: 'GSW', 'greendr01': 1, 'thompkl01': 1, 'curryst01': 1, 'barneha02': 1, 'ezelife01': 1, 'iguodan01': 1, 'livinsh01': 1, 'varejan01': 1, 'speigma01': 1, 'barbole01': 1, 'clarkia01': 1, 'mcadoja01': 1, 'rushbr01': 1}
# SUBSTITUIONNNNNNNNNNNNNNNN  
# {'ezelife01': 1, 'thomptr01': 0, 'jamesle01': 0, 'smithjr01': 0, 'jefferi01': 0, 'curryst01': 1, 'irvinky01': 0, 'thompkl01': 1, 'greendr01': 1, 'barneha02': 1}
# {'livinsh01': 1, 'greendr01': 1, 'jefferi01': 0, 'speigma01': 1, 'shumpim01': 0, 'thompkl01': 1, 'willima01': 0, 'jamesle01': 0, 'thomptr01': 0, 'iguodan01': 1}   
# {'ezelife01': 1, 'loveke01': 0, 'smithjr01': 0, 'greendr01': 1, 'thomptr01': 0, 'jamesle01': 0, 'thompkl01': 1, 'curryst01': 1, 'irvinky01': 0, 'barneha02': 1}    
# SUBSTITUIONNNNNNNNNNNNNNNN  SUBSTITUIONNNNNNNNNNNNNNNN  SUBSTITUIONNNNNNNNNNNNNNNN  SUBSTITUIONNNNNNNNNNNNNNNN  
# {'jamesle01': 0, 'iguodan01': 1, 'barneha02': 1, 'thompkl01': 1, 'jefferi01': 0, 'curryst01': 1, 'greendr01': 1, 'thomptr01': 0, 'smithjr01': 0, 'irvinky01': 0}