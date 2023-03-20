import requests
from bs4 import BeautifulSoup
import pandas as pd

#making get request

r = requests.get('https://stats.espncricinfo.com/ci/engine/records/team/match_results.html?id=2022%2F23;trophy=89;type=season')
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
        matchid = columns[6].text
        list_row = [team1, team2, winner, margin, ground, matchdate, matchid]
        dataframe.append(list_row)
df = pd.DataFrame(dataframe)
df.columns = ['Team1', 'Team2', 'Winner', 'Margin', 'Ground', 'Matchdate','Match_ID']
df.to_csv(r'C:\Users\ASUS\Desktop\Kaggle\Data Analysis\Cricket_Analysis\WebData\Matches.csv', index=False)
