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
    bowling_tables = new_soup.find_all('table',class_='ds-w-full ds-table ds-table-md ds-table-auto')
    inning = 1
    print("Collecting Match {} inning {} data".format(match_count, inning))
    for bowling_table in bowling_tables:
        rows = bowling_table.find('tbody').find_all('tr')
        for row in rows:
            column = row.find_all('td')
            if (column != []):
                if len(column) == 11:
                    match = teams[0].text + ' vs ' + teams[1].text
                    name = column[0].find('span').text
                    overs = column[1].text
                    maidens = column[2].text
                    runs = column[3].text
                    wickets = column[4].text
                    economy = column[5].text
                    dot_balls = column[6].text
                    fours = column[7].text
                    sixes = column[8].text
                    wides = column[9].text
                    no_balls = column[10].text
                    match_id = id
                    list_row = [match, name, overs, maidens, runs, wickets, economy, dot_balls, fours, sixes, wides, no_balls, match_id]
                    dataframe.append(list_row)
        print("Match {} inning {} data collected...".format(match_count, inning))
        inning += 1
        print(dataframe)
    match_count += 1

df = pd.DataFrame(dataframe)
df.columns = ['Match','Name', 'Overs', 'Maiden_Overs', 'Runs', 'Wickets', 'Economy', 'Dot Balls', 'Fours', 'Sixes', 'Wides','No_Balls','Match_ID']
df.to_csv(r'C:\Users\ASUS\Desktop\Kaggle\Data Analysis\Cricket_Analysis\WebData\BowlingSummary.csv', index=False)