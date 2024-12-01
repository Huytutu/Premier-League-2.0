from bs4 import BeautifulSoup
import pandas as pd

with open('./data/overview/Premier League Players - Overview.html', 'r', encoding='utf-8') as file:
    html_file = file.read()

soup = BeautifulSoup(html_file , 'html.parser')

items_player = soup.find_all(class_="player")

data = []
def make_link_stats(link : str):
    link = '/'.join(link.split("/")[:-1])
    return 'https:' + link + '/stats?co=1&se=719'
for item in items_player:
    name = item.find(class_='player__name').text
    country = item.find(class_= 'player__country').text
    position = item.find(class_= 'player__position').text
    link_profile_stats_2425 = make_link_stats(item.find(class_='player__name').get('href'))
    data.append([name,position,country, link_profile_stats_2425])

df = pd.DataFrame(data , columns=['name' , 'position' , 'country' ,'link_profile_stats_2425'])

df.to_csv('./data/Stats_csv/players.csv', index=False, encoding='utf8')


