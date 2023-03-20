import requests
from bs4 import BeautifulSoup
import pandas as pd

#making get request

r = requests.get('https://stats.espncricinfo.com/ci/engine/records/team/match_results.html?id=2022%2F23;trophy=89;type=season')
print(r)

soup = BeautifulSoup(r.content,'html.parser')
s = soup.find('table', class_= 'engineTable')

content = s.find_all('tr')
urls = {}
url_start = 'https://stats.espncricinfo.com/'
for row in content:
    columns = row.find_all('td')
    if (columns != []):
        id = columns[6].text
        urls[id] = url_start+columns[6].find('a').get('href')
print(urls)

dataframe = []
match_count = 1

for id in urls.keys():
    new_r = requests.get(urls[id])
    new_soup = BeautifulSoup(new_r.content,'html.parser')
    teams = new_soup.find_all('span','ds-text-tight-l ds-font-bold ds-text-typo hover:ds-text-typo-primary ds-block ds-truncate')
    batting_tables = new_soup.find_all('table',class_='ds-w-full ds-table ds-table-md ds-table-auto ci-scorecard-table')
    inning = 1
    print("Collecting Match {} inning {} data".format(match_count,inning))
    for batting_table in batting_tables:
        rows = batting_table.find('tbody').find_all('tr')
        count = 1
        for row in rows:
            column = row.find_all('td')
            if (column != []):
                if len(column)>1:
                    if(column[0].text == 'Extras'):
                        break
                    else:
                        match = teams[0].text + ' vs ' + teams[1].text
                        name = column[0].find('a').get('title')
                        pos = count
                        out = column[1].text
                        runs = column[2].text
                        balls = column[3].text
                        fours = column[5].text
                        sixes = column[6].text
                        sr = column[7].text
                        match_id = id
                        count=count+1
                        list_row = [match, name, pos, inning, out, runs, balls, fours, sixes, sr, match_id]
                        dataframe.append(list_row)
        print("Match {} inning {} data collected...".format(match_count, inning))
        inning += 1
        #print(dataframe)
    match_count += 1


df = pd.DataFrame(dataframe)
df.columns = ['Match','Name', 'Pos', 'Inning', 'Out', 'Runs', 'Balls', 'Fours', 'Sixes', 'S.R', 'Match_ID']
df.to_csv(r'C:\Users\ASUS\Desktop\Kaggle\Data Analysis\Cricket_Analysis\WebData\BattingSummary.csv', index=False)