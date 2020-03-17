import os

import pandas as pd
import requests
from bs4 import BeautifulSoup

Videos = []
Links = ['https://www.youtube.com/watch?v=l4lyfwdm4Pc',
         'https://www.youtube.com/watch?v=pKO9UjSeLew',
         'https://www.youtube.com/watch?v=kJQP7kiw5Fk']

def main() :
    global Videos
    global Links
    for i in Links :
     Videos.append(scrape(i))
    df = pd.DataFrame(Videos)
    df.to_csv('data.csv', encoding='utf-8', header=True ,index=False)
        
    
def scrape(link) :
    video = {}
    source = get_divs(link)
    video['Title'] = get_title(source)
    video['Link'] = link
    video['Channel'] = channel_info(source)['Channel_name']
    video['Channel_link'] = channel_info(source)['Channel_link']
    video['Channel_subscribers'] = channel_info(source)['Subscribers']
    video['Category'] = get_category(source)
    video['Views'] = get_views(source)
    video['Likes'] = get_likes(source)
    video['Related_vids']= get_related_videos(source)
    return video

def get_divs(link) :
    source = requests.get(link).text
    soup=BeautifulSoup(source,'lxml')
    div_s = soup.findAll('div')
    return div_s

def get_title(div_s) :
    title = div_s[1].find('span',class_='watch-title').text.strip()
    return title

def channel_info(div_s) :
    channel_name = div_s[1].find('a',class_="yt-uix-sessionlink spf-link").text.strip()
    channel_link = ('www.youtube.com'+div_s[1].find('a',class_="yt-uix-sessionlink spf-link").get('href'))
    subscribers = div_s[1].find('span',class_="yt-subscription-button-subscriber-count-branded-horizontal yt-subscriber-count").text.strip()
    if len(channel_name) ==0 :
        channel_name ='None'
        channel_link = 'None'
        subscribers = 'None'
    channel_info = dict(Channel_name = channel_name,
                        Channel_link = channel_link,
                        Subscribers = subscribers)
    return channel_info

def get_category(div_s) :
    category = div_s[1].findAll('a',class_="yt-uix-sessionlink spf-link")[1].text.strip()
    return category

def get_views(div_s) :
    view_count = div_s[1].find('div',class_= 'watch-view-count')
    view_count = view_count.text[:-11].replace(",", "")
    return view_count

def get_likes(div_s) :
    likes = div_s[1].find('button',class_="yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup like-button-renderer-like-button like-button-renderer-like-button-unclicked yt-uix-clickcard-target yt-uix-tooltip" ).text.strip()
    return likes

def get_dislikes(div_s) :
    dislikes = div_s[1].find('button',class_="yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup like-button-renderer-dislike-button like-button-renderer-dislike-button-unclicked yt-uix-clickcard-target yt-uix-tooltip" ).text.strip()
    return dislikes

def get_related_videos(div_s) :
    related_videos = div_s[1].findAll('a',class_='content-link spf-link yt-uix-sessionlink spf-link')
    title_related = []
    link_related = []
    for i in range(len(related_videos)):
        title_related.append(related_videos[i].get('title'))
        link_related.append(related_videos[i].get('href'))
    related_dictionary = dict(zip(title_related, link_related))
    return related_dictionary

if __name__== "__main__":
  main()