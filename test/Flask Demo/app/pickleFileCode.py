with open("hashtable.pkl", "rb") as input_file:
    hashtable = pickle.load( input_file)
with open("songid.pkl", "rb") as input_file:
    song_dict = pickle.load(input_file)