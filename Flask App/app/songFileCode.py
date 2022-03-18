file = open('songs.txt','r')#list of song files ----> use      ls >allsongs
allsongs = file.readlines()
allsongs = [a[:-1] for a in allsongs]
numOfSongs = len(allsongs)