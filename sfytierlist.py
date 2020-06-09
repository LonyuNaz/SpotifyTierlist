"""
---------------------Initiate packages--------------------------------
"""

import shelve
import numpy as np
import spotipy
import spotipy.util as util
import os

mycid = '32d2f622366e43778190832fa2bcd8c4'
mycsecret = 'de5e6987e58847608df22a2ba6827097'
myredirurl  = 'https://www.spotify.com/nl/account/overview/'
uname = 'nazbohlon'

"""
----------------------Open Shelf------------------------------------
"""

try:
    my_shelf = shelve.open(r'C:\Data\python scripts\sfytierlist\tmp\tierlistshelf.db')
    for key in my_shelf:
        globals()[key]=my_shelf[key]
    my_shelf.close()
except:
    pass

try:
    first
except:
    added_at = []
    scores = []
    tracks = []
    titles = []
    artists = []
    uniqueartists = []
    ratings = []
    lengths = []
    popfactor = []
    artists_id = []
    tracks_id = []
    
    danceness = []
    energyness = []
    keys = []
    loudness = []
    mode = []
    speechiness = []
    acousticness = []
    instrumentalness = []
    liveness = []
    valence = []
    tempo = []
    top5 = []
    
    
"""
---------------------Extract saved track data-----------------------
"""
scope = 'user-library-read'
token = util.prompt_for_user_token(uname,scope,client_id=mycid,client_secret=mycsecret,redirect_uri=myredirurl)


if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_saved_tracks(limit=50)
    for item in results['items']:
        added_at.append(item['added_at'])
        track = item['track']
        if [track['name'],track['artists'][0]['name']] not in tracks:
            tracks.append([track['name'],track['artists'][0]['name']])
            titles.append(track['name'])
            tracks_id.append(track['id'])
            artists.append(track['artists'][0]['name'])
            artists_id.append(track['artists'][0]['id'])
            if track['artists'][0]['name'] not in uniqueartists:
                uniqueartists.append(track['artists'][0]['name'])
                ratings.append([track['artists'][0]['name']])
            lengths.append(round(track['duration_ms']/1000))
            popfactor.append(track['popularity'])
            
            audio_features = sp.audio_features(tracks_id[-1])[0]
            danceness.append(audio_features['danceability'])
            energyness.append(audio_features['energy'])
            keys.append(audio_features['key'])
            loudness.append(audio_features['loudness'])
            mode.append(audio_features['mode'])
            speechiness.append(audio_features['speechiness'])
            acousticness.append(audio_features['acousticness'])
            instrumentalness.append(audio_features['instrumentalness'])
            liveness.append(audio_features['liveness'])
            valence.append(audio_features['valence'])
            tempo.append(audio_features['tempo'])
else:
    print("Can't get token for", uname)
    
    
""""
-----------------------Add scores---------------------
"""

startrating = len(scores)
for title in titles[startrating:]:
    index = titles.index(title)
    x = int(input('Please enter rating for: '+str(title)+', by: '+str(artists[index])+' --> '))
    if not isinstance(x, int):
        x = int(input('Please enter a number for: '+str(title)+', by: '+str(artists[index])+' --> '))
    if x < 0 or x > 5:
        x = input('Please enter a score between 0 and 5: ')
    scores.append(x)
    artist = tracks[index][1]
    artist_index = uniqueartists.index(artist)
    ratings[artist_index].append(x)
    
"""
-----------------------Edit tierlist--------------------
"""

tierlist = []
for i in range(len(ratings)):
    elo = round(len(ratings[i][1:])/4,3)+round(np.mean(ratings[i][1:]),3)
    name = ratings[i][0]
    tierlist.append([elo,name])

tierlist = sorted(tierlist)

top5.append(tierlist[-5:])

"""
-----------------------Edit audio features--------------------
"""

featscores  = {}
featscores['danceness'] = sum([scores[i]*danceness[i] for i in range(len(scores))])/sum(scores)
featscores['energyness'] = sum([scores[i]*energyness[i] for i in range(len(scores))])/sum(scores)
featscores['key'] = sum([scores[i]*keys[i] for i in range(len(scores))])/sum(scores)
featscores['loudness'] = sum([scores[i]*loudness[i] for i in range(len(scores))])/sum(scores)
featscores['mode'] = sum([scores[i]*mode[i] for i in range(len(scores))])/sum(scores)
featscores['speechiness'] = sum([scores[i]*speechiness[i] for i in range(len(scores))])/sum(scores)
featscores['acousticness'] = sum([scores[i]*acousticness[i] for i in range(len(scores))])/sum(scores)
featscores['instrumentalness'] = sum([scores[i]*instrumentalness[i] for i in range(len(scores))])/sum(scores)
featscores['liveness'] = sum([scores[i]*liveness[i] for i in range(len(scores))])/sum(scores)
featscores['valence'] = sum([scores[i]*valence[i] for i in range(len(scores))])/sum(scores)
featscores['tempo'] = sum([scores[i]*tempo[i] for i in range(len(scores))])/sum(scores)

"""
-----------------------Edit duration data-----------------
"""

dur = {}
dur['<2 mins'] = 0
dur['2 - 2.33 mins'] = 0
dur['2.33 - 2.67 mins'] = 0
dur['2.67 - 3 mins'] = 0
dur['3 - 3.33 mins'] = 0
dur['3.33 - 3.67 mins'] = 0
dur['3.67 - 4 mins'] = 0
dur['4 - 4.33 mins'] = 0
dur['4.33 - 4.67 mins'] = 0
dur['4.67 - 5 mins'] = 0
dur['>5 mins'] = 0

for time in lengths:
    if time < 120.5:
        dur['<2 mins'] += 1
    elif time < 140.5:
        dur['2 - 2.33 mins'] += 1
    elif time < 160.5:
        dur['2.33 - 2.67 mins']  += 1
    elif time < 180.5:
        dur['2.67 - 3 mins'] += 1
    elif time < 200.5:
        dur['3 - 3.33 mins'] += 1
    elif time < 220.5:
        dur['3.33 - 3.67 mins'] += 1
    elif time < 240.5:
        dur['3.67 - 4 mins'] += 1
    elif time < 260.5:
        dur['4 - 4.33 mins'] += 1
    elif time < 280.5:
        dur['4.33 - 4.67 mins'] += 1
    elif time < 300.5:
        dur['4.67 - 5 mins'] += 1
    else:
        dur['>5 mins'] +=1
        
"""
----------------------Edit popularity list---------------
"""

pop = {}
pop['Bedroom'] = 0
pop['Underground'] = 0
pop['Support'] = 0
pop['Known'] = 0
pop['Star'] = 0

for factor in popfactor:
    if factor < 20.5:
        pop['Bedroom'] += 1
    elif factor < 40.5:
        pop['Underground'] += 1
    elif factor < 60.5:
        pop['Support'] += 1
    elif factor < 80.5:
        pop['Known'] += 1
    else:
        pop['Star'] += 1
        
"""
------------------------Store data----------------------
"""

path = os.getcwd()
shelfpath = os.path.join(path,'tmp')
if not os.path.exists(shelfpath):
    os.makedirs(shelfpath)
shelfname = os.path.join(shelfpath,'tierlistshelf.db')


my_shelf = shelve.open(shelfname,'n') 

first = 1

toadd = ['first','added_at','tracks','ratings','popfactor','uniqueartists',
         'artists','lengths','titles','dur','pop','artists_id','tracks_id',
         'danceness','energyness','keys','loudness','mode','speechiness',
         'acousticness','instrumentalness','liveness','valence','tempo','top5','scores']

for key in toadd:
    try:
        my_shelf[key] = globals()[key]
    except TypeError:
        print('ERROR shelving: {0}'.format(key))
my_shelf.close()