from bs4 import BeautifulSoup
import requests


months = ["january","february","march","april","may","june","july","august","september","octoboer","october-2019","october-2020","november","december"]
year = 2023
url = "https://www.basketball-reference.com/leagues/NBA_"+str(year)+"_games-"

filename = str(year)+"regularseasononofdata.txt"

writeFile = open(filename,"w")
writeFile.close()
tempFile = "temp.txt"

for month in months:
    response = requests.get(url+month+".html")

    if response.status_code == 200:
        html_content = response.content
    else:
        print("Failed to retrieve content. Status code:", response.status_code)

    soup = BeautifulSoup(html_content, 'html.parser')

    with open(tempFile, 'w', encoding='utf-8') as file:
        file.write(str(soup))

    file.close()

    writeFile = open(filename,"a")

    l = 0
    f = open(tempFile,"r")
    start = 0



    for line in f.readlines()[6000:]:
        l+=1
        if '_game" csk="' in line:
            start = 1
        if 'global.nonempty_tables_nu' in line:
            writeFile.close()
            break
        if start == 1:
            s = line.split('_game" csk="')
            for i in s:
                i = i.split('"')[0]
                print(i+".html")

