import sqlite3


# Create  the database

conn = sqlite3.connect('luoo.db')

print("Connect to the database")

conn.execute('''CREATE TABLE volume
 	(vol_id		INT 	NOT NULL,
 	vol_title 	TEXT 	NOT NULL,
 	tag 		TEXT    NOT NULL);''')


conn.execute('''CREATE TABLE song
 	(song_id	INT 	PRIMARY KEY NOT NULL,
 	song_name 	TEXT 	NOT NULL,
	artist 		TEXT	NOT NULL,
	vol_id		INT 	NOT NULL,
	FOREIGN KEY(vol_id)		REFERENCES	volume(vol_id));''')


print("Create database")
