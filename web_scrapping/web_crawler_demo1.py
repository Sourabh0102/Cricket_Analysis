import requests
from bs4 import BeautifulSoup

#making get request

r = requests.get('https://stats.espncricinfo.com/ci/engine/records/team/match_results.html?class=3;id=2023;type=year')
print(r)

soup = BeautifulSoup(r.content,'html.parser')
s = soup.find('table', class_= 'engineTable')

content = s.find_all('tr')
dataframe = []
for row in content:
    columns = row.find_all('td')
    if(columns != []):
        team1 = columns[0].text
        team2 = columns[1].text
        winner = columns[2].text
        margin = columns[3].text
        ground = columns[4].text
        matchdate = columns[5].text
        #scorecard = columns[6].text
        list_row = [team1, team2, winner, margin, ground, matchdate]
        dataframe.append(list_row)
print(dataframe)