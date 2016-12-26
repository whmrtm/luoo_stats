import requests
import re
import sqlite3
from bs4 import BeautifulSoup

# Helper function

def crawler(music_html):
	# parser
	soup = BeautifulSoup(music_html, 'html.parser')
	try:
		vol_number = soup.find('span', class_="vol-number").string
	except:
		print("No content")
		return
	vol_title = soup.find('span', class_="vol-title").string
	tags = soup.find_all('a', class_="vol-tag-item")

	trackitems = soup.find_all('li', class_="track-item")
	tracknames = soup.find_all('a', class_="trackname")
	track_artists = soup.find_all('span', class_="artist")



	song_ids = []
	songs = []
	artists = []

	for trackitem in trackitems:
		trackid = trackitem['id']
		trackid = trackid.replace("track", "")
		song_ids.append(trackid)

	song_match = re.compile('\d+. (.*)')
	for trackname in tracknames:
		name = trackname.string
		if name != None:
			name = song_match.match(name).group(1)
			songs.append(name)

	for artist in track_artists:
		artists.append(artist.string)

	# Insert into the database


	for i in range(len(song_ids)):
		data = [int(song_ids[i]), songs[i], \
		 artists[i], int(vol_number)];	
		cursor.execute("INSERT OR REPLACE INTO song (song_id, song_name, artist, vol_id) VALUES (?,?,?,?)", data)
	
	for i in range(len(tags)):
		t = [int(vol_number), vol_title, \
		tags[i].string]
		cursor.execute("INSERT INTO volume (vol_id, vol_title, tag) VALUES (?,?,?)", t)



# Connect to the database
conn = sqlite3.connect('luoo.db')
cursor = conn.cursor()

# A web crawler for my favorite music website Luoo

session_requests = requests.session()
luoo_url = "http://www.luoo.net/music/"

vol_num = 1
for vol_num in range(900):
	if vol_num != 576:
		response = session_requests.get(luoo_url+str(vol_num))
		if response.status_code != 200:
			print("Static code fault")
			break
		print("Fetching content from volume: " + str(vol_num))
		music_html = response.content
		crawler(music_html)

#  Test
# response = session_requests.get(luoo_url+str(863))
# crawler(response.content)

# Finish the insertion

conn.commit()
print("Data inserted")
conn.close()