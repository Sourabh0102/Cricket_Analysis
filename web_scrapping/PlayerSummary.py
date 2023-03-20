import requests
from bs4 import BeautifulSoup
import pandas as pd

#making get request

r = requests.get('https://www.espncricinfo.com/series/icc-men-s-t20-world-cup-2022-23-1298134/squads')

soup = BeautifulSoup(r.content,'html.parser')
content = soup.find('div',class_='ds-mb-4')
url_start = 'https://stats.espncricinfo.com/'
links = content.find_all('a')
urls =[]
dataframe = []
for link in links:
    link = url_start+link.get('href')
    urls.append(link)
for id in urls:
    new_r = requests.get(id)
    new_soup = BeautifulSoup(new_r.content,'html.parser')
    s = new_soup.find('div',class_='ds-w-full ds-bg-fill-content-prime ds-overflow-hidden ds-rounded-xl ds-border ds-border-line')
    squad_name = new_soup.find('span',class_='ds-text-title-l ds-font-bold ds-text-typo').text
    player_anchors = s.find_all('a')
    player_links = []
    for anchor in player_anchors:
        anchor = url_start+anchor.get('href')
        player_links.append(anchor)
    print("Getting details of player from {}".format(squad_name))
    player_links = player_links[::2]
    count = 1
    for player_link in player_links:
        request = requests.get(player_link)
        bs = BeautifulSoup(request.content,'html.parser')
        data = bs.find('div',class_='ds-grid lg:ds-grid-cols-3 ds-grid-cols-2 ds-gap-4 ds-mb-8').find_all('p',class_='ds-text-tight-m ds-font-regular ds-uppercase ds-text-typo-mid3')
        name = dob = bat_style = bowl_style = role = ''
        for info in data:
            #print(bat_style)
            #print(info.text)
            if(info.text == 'Full Name'):
                name = info.findNext().text
                print("\t",name)
            if (info.text == 'Born'):
                dob = info.findNext().text
            if (info.text == 'Batting Style'):
                bat_style = info.findNext().text
            if (info.text == 'Bowling Style'):
                bowl_style = info.findNext().text
            if (info.text == 'Playing Role'):
                role = info.findNext().text





        # if(len(data) == 6):
        #     name = data[0].text
        #     print("\t{}.Collecting data of {} ".format(count,name))
        #     count+=1
        #     dob = data[1].text
        #     bat_style = data[3].text
        #     bowl_style = data[4].text
        #     role = data[5].text
        # else:
        #     name = data[0].text
        #     print("\t{}.Collecting data of {} ".format(count,name))
        #     count+=1
        #     dob = data[1].text
        #     bat_style = data[3].text
        #     bowl_style = data[4].text
        #     role = "NA"
        player_details = [squad_name,name,dob,bat_style,bowl_style,role]
        dataframe.append(player_details)
        #print("\t",dataframe)

df = pd.DataFrame(dataframe)
df.columns = ['Squad_Name','Name','DOB','Bat_Style','Bowl_Style','Role']
df.to_csv(r'C:\Users\ASUS\Desktop\Kaggle\Data Analysis\Cricket_Analysis\WebData\PlayerSummary.csv', index=False)

