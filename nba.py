import requests

from bs4 import BeautifulSoup


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
    print(pD)
    lineNum = -1
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            lineNum += 1
            if '<div class="section_heading"><span class="section_anchor" data-label="Team and League Schedules" data-no-inpage="1" id="inner_nav_bottom_link"></span><h2>Team and League Schedules</h2></div>' in line:
                break
            if '<th aria-label="Time" class="center" data-sstat="Time">Time</th>' in line:
                start = 1
            if '<th aria-label="Time" class="center" data-stat="Time">Time</th>' in line:
                pList = getStarters(filename,pD,lineNum)
                print(pList)
            if start == 1 and line != '</tr>\n' and line != '<tr>\n':
                if line.startswith("<td>") and line[4].isnumeric():
                    timeLine = line.strip("<td>").strip("</td>\n")
                    wFile.write(timeLine+"\n") 
                elif "enters" in line:
                    wFile.write("SUBSTITUIONNNNNNNNNNNNNNNN\n")
            pVar = line.split('<a href="/players/')
            if len(pVar) == 1:
                pVar = []
            else:
                pVar = pVar[1:]
            for i in range(len(pVar)):
                pVar[i] = pVar[i].split(">")[0][2:-6]
            
            if start == 1 and pVar != []:
                # wFile.write(line)
                pass
                #print(len(pVar),pVar)

def processRoster(filename):
    
    wFile = open("1111.txt","w")
    pD = {}
    start = 0
    with open(filename, 'r', encoding='utf-8') as file:
        start = 0
        prevTeam = ""
        team = [""]
        tc = -1
        for line in file:
            if '<!-- global.nonempty_tables_num: 3, table_count: 3 -->' in line:
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
       
        return pD
                # wFile.write(line)

def getStarters(filename,pd,lineNum):
    wFile = open("starters.txt","w")
    onCourt = {}
    num = 0
    start = 0
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            num += 1
            if num > lineNum:
                start = 1
            if start == 1 and line != '</tr>\n' and line != '<tr>\n':
                pVar = line.split('<a href="/players/')
                if len(pVar) == 1:
                    pVar = []
                else:
                    pVar = pVar[1:]

                for i in range(len(pVar)):
                    pVar[i] = pVar[i].split(">")[0][2:-6]

               
                

                if len(pVar) != 0:
                    for player in pVar:
                        onCourt[player] = pD[player]
                    if "enters" in line:
                        print("SUBSTITUIONNNNNNNNNNNNNNNN  ",end="")
                        del onCourt[pVar[1]]
                        onCourt[pVar[0]] = pD[pVar[0]]

                    if (len(onCourt) == 10):
                        # print(onCourt)
                        return onCourt
                

                    pass
           


url = "201606190GSW.html"
pbpFile = "pbp.txt"
roster = "roster.txt"
saveFile = "save.txt"

#getRequestContentPBP(url,pbpFile)
#getRequestContentRoster(url,roster)

pD = processRoster(roster)

#printfile(filename)
processGame(pbpFile,pD)



# {0: 'CLE', 'jamesle01': 0, 'irvinky01': 0, 'smithjr01': 0, 'thomptr01': 0, 'loveke01': 0, 'jefferi01': 0, 'shumpim01': 0, 'willima01': 0, 'dellama01': 0, 'fryech01': 0, 'jonesda02': 0, 'jonesja02': 0, 'mozgoti01': 0, 1: 'GSW', 'greendr01': 1, 'thompkl01': 1, 'curryst01': 1, 'barneha02': 1, 'ezelife01': 1, 'iguodan01': 1, 'livinsh01': 1, 'varejan01': 1, 'speigma01': 1, 'barbole01': 1, 'clarkia01': 1, 'mcadoja01': 1, 'rushbr01': 1}
# SUBSTITUIONNNNNNNNNNNNNNNN  
# {'ezelife01': 1, 'thomptr01': 0, 'jamesle01': 0, 'smithjr01': 0, 'jefferi01': 0, 'curryst01': 1, 'irvinky01': 0, 'thompkl01': 1, 'greendr01': 1, 'barneha02': 1}
# {'livinsh01': 1, 'greendr01': 1, 'jefferi01': 0, 'speigma01': 1, 'shumpim01': 0, 'thompkl01': 1, 'willima01': 0, 'jamesle01': 0, 'thomptr01': 0, 'iguodan01': 1}   
# {'ezelife01': 1, 'loveke01': 0, 'smithjr01': 0, 'greendr01': 1, 'thomptr01': 0, 'jamesle01': 0, 'thompkl01': 1, 'curryst01': 1, 'irvinky01': 0, 'barneha02': 1}    
# SUBSTITUIONNNNNNNNNNNNNNNN  SUBSTITUIONNNNNNNNNNNNNNNN  SUBSTITUIONNNNNNNNNNNNNNNN  SUBSTITUIONNNNNNNNNNNNNNNN  
# {'jamesle01': 0, 'iguodan01': 1, 'barneha02': 1, 'thompkl01': 1, 'jefferi01': 0, 'curryst01': 1, 'greendr01': 1, 'thomptr01': 0, 'smithjr01': 0, 'irvinky01': 0}