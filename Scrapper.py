import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from tqdm import tqdm
#TODO, HAY TAGS <br> y <br/> que, para mi, son lo mismo, eventualmente, en preproc de data, se debe reemplazar <br/> por <br>

def parse_song(href: str):
    page = requests.get('https://www.letras.com' + href)

    #lyrics organized in <p>
    lyrics = BeautifulSoup(page.content, 'html.parser').find_all('div', "cnt-letra p402_premium")[0].find_all('p')
    lyrics_html = [str(i) for i in lyrics]
    #print(''.join(lyrics_html))
    lyrics_no_html = [re.sub('(<p>)|<p/>|</p>', '', re.sub('(<br>)|(<br/>)|</br>', ' ', str(i))) for i in lyrics]
    #print(''.join(lyrics_no_html)
    return ''.join(lyrics_no_html), ''.join(lyrics_html)

def main():
    URL = 'https://www.letras.com/mais-acessadas/reggaeton/'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    songs_list = soup.find_all('ol', 'top-list_mus cnt-list--col1-3')[0].find_all('li')

    titles = ['' for i in songs_list]
    lyrics_no_html = ['' for i in songs_list]
    lyrics_html = ['' for i in songs_list]

    for i,song in tqdm(enumerate(songs_list)):
        a = song.find_all('a')[0]
        href = a['href']
        title = a['title']
        #For each song, follow the song's link and parse it:

        titles[i] = title
        lyrics_no_html[i], lyrics_html[i] = parse_song(href)

    #Create DataFrame
    data = {'song_title': titles, 'lyrics_html':lyrics_html, 'lyrics_no_html': lyrics_no_html}

    df = pd.DataFrame(data)
    df.to_csv('song_export.csv', sep=';')

if __name__ == "__main__":
    main()

    #print(re.sub('<br>', ' ', "Tengo tantas ganas<br>Ay, de besa"))